from django.db import models
from django.utils.translation import gettext_lazy as _

from api.common.models import BaseModelGeneric, File


class Category(BaseModelGeneric):
    display_name = models.CharField(max_length=150)
    short_name = models.SlugField(max_length=300)
    thumbnail = models.ForeignKey(File, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Product(BaseModelGeneric):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=300)
    price = models.DecimalField(decimal_places=2, max_digits=19)
    is_available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)  # all stocks
    stock_available = models.PositiveIntegerField(
        default=0)  # stock remaining
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ForeignKey(File, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class ProductMedia(BaseModelGeneric):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("ProductMedia")
        verbose_name_plural = _("ProductMedias")


class FlashSale(BaseModelGeneric):
    event_name = models.CharField(max_length=200)
    start_event = models.DateTimeField()
    end_event = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("FlashSale")
        verbose_name_plural = _("FlashSales")


class ProductFlashSale(BaseModelGeneric):
    flash_sale = models.ForeignKey(FlashSale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    stock = models.IntegerField(default=1)

    class Meta:
        verbose_name = _("ProductFlashSale")
        verbose_name_plural = _("ProductFlashSales")
