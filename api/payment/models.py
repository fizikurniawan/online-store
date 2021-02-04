from django.db import models
from django.contrib.auth.models import User

from api.common.models import BaseModelGeneric
from api.product.models import Product

from libs.constant import BILL_STATUS_CHOICES


class Cart(BaseModelGeneric):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)


class CheckOut(BaseModelGeneric):
    class Meta:
        verbose_name = _("CheckOut")
        verbose_name_plural = _("CheckOuts")


class Invoice(BaseModelGeneric):
    number = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(choices=BILL_STATUS_CHOICES)

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")


class InvoiceItem(BaseModelGeneric):
    pass
