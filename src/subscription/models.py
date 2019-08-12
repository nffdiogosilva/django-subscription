import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .utils import get_year_total_days

# With this, I can get exactly the total days in the
# current year or override the value in the settings module.
SUBSCRIPTION_TTL_DAYS = getattr(settings, 'SUBSCRIPTION_TTL_DAYS', get_year_total_days())


class Customer(AbstractUser):
    # I can get the name field already with the first_name and last_name fields in the AbstractUser,
    # therefore this field it's commented, just created to respect project requirements.
    # name = models.CharField(_('name'), max_length=255)
    sub_renewal_date = models.DateField(_('renewal date'), null=True, editable=False)
    subscription = models.OneToOneField('Plan', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')
        ordering = ('-date_joined',)

    def __str__(self):
        return 'Customer: {} Plan: {}'.format(self.get_name(), self.subscription)

    def save(self, *args, **kwargs):
        # If no plan is associated with customer, than reset the renewal date to None.
        if not self.subscription:
            self.sub_renewal_date = None
        # If there's a subscription and renewal_date hasn't yet been calculated, do it now.
        elif not self.sub_renewal_date:
            self.sub_renewal_date = datetime.date.now() + datetime.timedelta(days=SUBSCRIPTION_TTL_DAYS)

        super(Customer, self).save(*args, **kwargs)

    def get_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Plan(models.Model):
    name = models.CharField(_('name'), max_length=255)
    price = models.DecimalField(_('price'), max_digits=6, decimal_places=2)
    total_websites_allowed = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _('plan')
        verbose_name_plural = _('plans')
        ordering = ('-name',)

    def __str__(self):
        return 'Plan: {}'


class Website(models.Model):
    url = models.URLField(_('url'))
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True, related_name='websites')

    class Meta:
        verbose_name = _('website')
        verbose_name_plural = _('websites')

    def __str__(self):
        return 'Website: {}'.format(self.url)
