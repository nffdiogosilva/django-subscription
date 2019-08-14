from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utils import get_year_total_days
from .exceptions import CustomerAddWebsitePermissionDenied


class SubscriptionManager(models.Manager):
    """
    Manager to handle the Customer subscriptions.
    """

    def get_queryset(self):
        """Override get queryset to return only the customers with current subscriptions."""
        return super().get_queryset().exclude(subscription=None)

    def subscribe_plan(self, customer, plan):
        """Method responsible of associating a plan to a customer object."""
        if customer.subscription:
            raise ValueError('User already subscribed to a plan ({})'.format(customer.subscription))

        customer.subscription = plan
        customer.save()

        return customer.subscription

    def change_plan(self, customer, new_plan):
        """Method responsible of substituting the customer current subscription with another."""
        if not customer.subscription:
            raise ValueError('There\'s no subscription plan to update')
        if customer.subscription == new_plan:
            raise ValueError('This plan ({}) is already associated with this customer ({})'.format(new_plan, customer))

        # reset the renewal date since a new plan will be added
        customer.sub_renewal_date = None
        customer.subscription = new_plan
        customer.save()

        return True


class Customer(AbstractUser):
    # I can get the name field already with the first_name and last_name fields in the AbstractUser,
    # therefore this field it's commented, just referenced to respect project requirements.
    # name = models.CharField(_('name'), max_length=255)
    subscription = models.ForeignKey('Plan', on_delete=models.SET_NULL, null=True, blank=True)
    # readonly field (could make it 'editable=False', but I want to access it through ModelAdmin)
    sub_renewal_date = models.DateField(_('renewal date'), null=True, blank=True)

    objects = UserManager()
    with_subscriptions = SubscriptionManager()

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        ordering = ('-date_joined',)

    def __str__(self):
        return 'Customer: {}'.format(self.username)

    def save(self, *args, **kwargs):
        self.sub_renewal_date = self.set_renewal_date()
        super().save(*args, **kwargs)

    def can_add_website(self):
        if not self.subscription:
            raise models.ObjectDoesNotExist('Customer Subscription doesn\'t exist')

        allows_infinite = self.subscription.total_websites_allowed == 0
        return allows_infinite or self.websites.count() + 1 <= self.subscription.total_websites_allowed

    def get_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_total_websites_allowed(self):
        if self.subscription:
            return self.subscription.total_websites_allowed

    def set_renewal_date(self):
        """Calculates the renewal subscription date based if the user has an active subscription or not"""
        renewal_date = None

        # If there's a subscription and not renewal_date then calculate it now.
        if self.subscription and not self.sub_renewal_date:
            today = date.today()

            sub_ttl_days = getattr(settings, 'SUBSCRIPTION_TTL_DAYS', get_year_total_days(today.year + 1))
            renewal_date = today + timedelta(days=sub_ttl_days)

        return renewal_date


class Plan(models.Model):
    PLAN_TYPE_CHOICES = (('single', _('single')), ('plus', _('plus')), ('infinite', _('unlimited')))

    name = models.CharField(_('name'), max_length=255)
    price = models.DecimalField(_('price'), max_digits=6, decimal_places=2)

    # Instead of creating a PlanType model, where I could add more plan types in the future,
    # I left it as only a char field with hardcoded choices.
    plan_type = models.CharField(_('plan type'), max_length=60, choices=PLAN_TYPE_CHOICES, default='single')
    # readonly field (could make it 'editable=False', but I want to access it through ModelAdmin)
    total_websites_allowed = models.PositiveIntegerField(
        _('websites allowed'), default=1, help_text=_('For unlimited plans, 0 is inserted')
    )

    class Meta:
        verbose_name = _('plan')
        verbose_name_plural = _('plans')
        ordering = ('-name',)

    def __str__(self):
        return 'Plan: {}'.format(self.get_plan_type_display())

    def get_total_websites_allowed_based_on_type(self):
        total = None

        if self.plan_type == 'single':
            total = 1
        if self.plan_type == 'plus':
            total = 3
        if self.plan_type == 'infinite':
            total = 0

        return total

    def save(self, *args, **kwargs):
        self.total_websites_allowed = self.get_total_websites_allowed_based_on_type()
        super().save(*args, **kwargs)


class Website(models.Model):
    url = models.URLField(_('url'))
    # Why overriding the related_name? It's mainly for redability reasons,
    # but I go by the default django convention (i.e: default related_name="website_set") if that's the convention you guys use.
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, related_name='websites')

    class Meta:
        verbose_name = _('website')
        verbose_name_plural = _('websites')

    def __str__(self):
        return 'Website: {}'.format(self.url)

    def save(self, *args, **kwargs):
        if self.customer and not self.customer.can_add_website():
            raise CustomerAddWebsitePermissionDenied(
                'Customer can\'t add more websites. Total allowed: {}'.format(
                    self.customer.get_total_websites_allowed()
                )
            )

        super().save(*args, **kwargs)
