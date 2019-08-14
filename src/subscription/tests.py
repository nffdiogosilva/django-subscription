from datetime import date
from decimal import Decimal
from unittest import mock

from django.test import TestCase

from mixer.backend.django import mixer

from .exceptions import CustomerAddWebsitePermissionDenied
from .models import Customer, Plan, Website


class CustomerTestCase(TestCase):
    def setUp(self):
        self.customer = mixer.blend(Customer)
        self.default_plan = mixer.blend(Plan)
        self.old_plan = mixer.blend(Plan)
        self.new_plan = mixer.blend(Plan)

    def test_customer_can_subscribe_plan(self):
        """Test a customer is eligible to subscribe to a plan"""

        # First assert that the current customer doesn't have any plan associated with it.
        self.assertIsNone(self.customer.subscription)

        plan = mixer.blend(Plan)
        subscribed_plan = Customer.with_subscriptions.subscribe_plan(self.customer, plan)
        # Assert that the created plan is the same as the subscribed plan
        self.assertEqual(plan.pk, subscribed_plan.pk)

        # Assert that the subscribed plan is the same as the plan associated with the customer
        self.assertEqual(self.customer.subscription.pk, subscribed_plan.pk)

    def test_customer_can_change_plan(self):
        """Test a customer is eligible to change between plans"""

        # Trying to change a plan to a customer that doesn't yet have a plan should raise an exception
        with self.assertRaises(ValueError):
            Customer.with_subscriptions.change_plan(self.customer, self.new_plan)

        # Add a plan to a user
        Customer.with_subscriptions.subscribe_plan(self.customer, self.old_plan)
        self.assertEqual(self.customer.subscription, self.old_plan)

        # Trying to change to the same plan should raise an exception
        with self.assertRaises(ValueError):
            Customer.with_subscriptions.change_plan(self.customer, self.old_plan)

        # Assert, at last, that a customer can change a plan to a new one
        self.assertTrue(Customer.with_subscriptions.change_plan(self.customer, self.new_plan))

    def test_customer_renewal_date_has_one_year_time_value(self):
        """Test that the subscription renewal date has a one year timestamp"""

        # assert different years (test from 2000 until 2020)
        years = range(1999, 2021)
        today = date.today()
        for year in years:
            # For more information about mocking a date object,
            # please read: https://docs.python.org/3/library/unittest.mock-examples.html#partial-mocking
            with mock.patch('subscription.models.date') as mock_date:
                mock_date.today.return_value = date(year, today.month, today.day)
                mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

                # Check, that the user has not yet a subscription or a renewal_date
                self.assertIsNone(self.customer.subscription)
                self.assertIsNone(self.customer.sub_renewal_date)
                Customer.with_subscriptions.subscribe_plan(self.customer, self.default_plan)

                expected_renewal_date = date(year + 1, today.month, today.day)
                self.assertEqual(self.customer.sub_renewal_date, expected_renewal_date)

                # reset customer subscription and subscription renewal_date for next test
                self.customer.subscription = None
                self.customer.save()

    # TODO: test what happens when the renewal date is surpassed (the subscription should be canceled)

    def test_customer_website_crud_operations(self):
        """Test Website object crud operations, made by Customer object"""
        customer = mixer.blend(Customer, subscription=mixer.blend(Plan, plan_type='infinite'))
        website = mixer.blend(Website, customer=None)

        # Adding operation
        customer.websites.add(website)
        self.assertTrue(customer.websites.filter(pk=website.pk).exists())

        # Update operation
        website_old_url = website.url
        customer.websites.filter(pk=website.pk).update(url='https://foo.bar')
        self.assertNotEqual(website_old_url, customer.websites.get(pk=website.pk).url)

        # Remove operation
        customer.websites.remove(website)
        self.assertFalse(customer.websites.filter(pk=website.pk).exists())


class PlanTestCase(TestCase):
    def setUp(self):
        self.customer = mixer.blend(Customer)

        self.single_plan = mixer.blend(Plan, plan_type='single')
        self.plus_plan = mixer.blend(Plan, plan_type='plus')
        self.infinite_plan = mixer.blend(Plan, plan_type='infinite')

        self.website1 = mixer.blend(Website, customer=None)
        self.website2 = mixer.blend(Website, customer=None)
        self.website3 = mixer.blend(Website, customer=None)
        self.website4 = mixer.blend(Website, customer=None)

    def test_total_allowed_based_on_plan(self):
        """Test that the total websites allowed attribute is always saved based on the plan type"""

        self.assertEqual(self.single_plan.total_websites_allowed, 1)

        # Try to change it manually and assert it again
        self.single_plan.total_websites_allowed = 100
        self.single_plan.save()
        self.assertEqual(self.single_plan.total_websites_allowed, 1)

        self.assertEqual(self.plus_plan.total_websites_allowed, 3)
        # Try to change it manually and assert it again
        self.plus_plan.total_websites_allowed = 100
        self.plus_plan.save()
        self.assertEqual(self.plus_plan.total_websites_allowed, 3)

        self.assertEqual(self.infinite_plan.total_websites_allowed, 0)
        # Try to change it manually and assert it again
        self.infinite_plan.total_websites_allowed = 100
        self.infinite_plan.save()
        self.assertEqual(self.infinite_plan.total_websites_allowed, 0)

    # TODO: test also that the plan type is only one of those three (or create a Plan_type Model, this way you can add different plans in the future)

    def test_plan_type_single_allow_only_one_website(self):
        """Test that the plan with type single can only have one website"""

        Customer.with_subscriptions.subscribe_plan(self.customer, self.single_plan)

        # Allows adding one website, with no issue.
        # Please refer to the django documentation, to understand why bulk argument is being set to False:
        # https://docs.djangoproject.com/en/2.2/ref/models/relations/#django.db.models.fields.related.RelatedManager.add
        self.customer.websites.add(self.website1, bulk=False)
        self.assertEqual(self.customer.websites.count(), 1)

        # The 2nd one is expected to raise an Exception
        with self.assertRaises(CustomerAddWebsitePermissionDenied):
            self.customer.websites.add(self.website2, bulk=False)

    def test_plan_type_plus_allow_3_websites(self):
        """Test that the plan with type plus can only have max 3 websites"""

        Customer.with_subscriptions.subscribe_plan(self.customer, self.plus_plan)

        # Allows adding, with no issue, 3 websites.
        self.customer.websites.add(self.website1, self.website2, self.website3, bulk=False)
        self.assertEqual(self.customer.websites.count(), 3)

        # The 4th one is expected to raise an Exception
        with self.assertRaises(CustomerAddWebsitePermissionDenied):
            self.customer.websites.add(self.website4, bulk=False)

    def test_plan_type_infinite_allow_unlimited_websites(self):
        """Test that the plan with type infinite can have multiple websites"""

        Customer.with_subscriptions.subscribe_plan(self.customer, self.infinite_plan)

        # Can change this value to tests if you can add even more websites
        TOTAL_WEBSITES = 100
        websites = mixer.cycle(TOTAL_WEBSITES).blend(Website, customer=None)
        # Adding 100 websites, with no issue.
        self.customer.websites.add(*websites, bulk=False)
        self.assertEqual(self.customer.websites.count(), TOTAL_WEBSITES)
