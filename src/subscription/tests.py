from django.test import TestCase

# from mixer.backend.django import mixer

from .models import Customer, Plan, Website


class CustomerTestCase(TestCase):
    def setUp(self):
        pass

    def test_customer_can_buy_plan(self):
        """Test a customer is eligible to buy a plan"""
        raise NotImplementedError

    def test_customer_can_change_plans(self):
        """Test a customer is eligible to change between plans"""
        raise NotImplementedError

    def test_customer_can_add_website(self):
        """Test a customer is eligible to add a website"""
        raise NotImplementedError

    def test_customer_can_remove_website(self):
        """Test a customer is eligible to remove a website"""
        raise NotImplementedError

    def test_customer_can_update_website(self):
        """Test a customer is eligible to update a website"""
        raise NotImplementedError

    def test_customer_renewal_date_has_one_year_time_value(self):
        """Test that the subscription renewal date has a one year timestamp"""
        raise NotImplementedError


class PlanTestCase(TestCase):
    def setUp(self):
        pass

    def test_plan_type_single_allow_only_one_website(self):
        """Test that the plan with type single can only have one website"""
        raise NotImplementedError

    def test_plan_type_plus_allow_3_websites(self):
        """Test that the plan with type plus can only have max 3 websites"""
        raise NotImplementedError

    def test_plan_type_infinite_allow_unlimited_websites(self):
        """Test that the plan with type infinite can have multiple websites"""
        raise NotImplementedError
