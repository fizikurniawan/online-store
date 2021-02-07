from django.utils.translation import gettext_lazy as _

BILL_STATUS_CHOICES = (
    ('created', _('Created')),
    ('checking', _('Checking Admin')),
    ('pending', _('Pending')),
    ('success', _('Success')),
    ('expired', _('Expired')),
)

PAYMENT_METHOD_CHOICES = (
    ('transfer', _('Transfer'))
)