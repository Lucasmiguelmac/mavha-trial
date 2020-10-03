from django.db import models
from account.models import User
from hashid_field import HashidAutoField


class Listing(models.Model):
    """
    Model to represent listings instances intended to be booked.
    """
    id                  = HashidAutoField(primary_key=True)
    owner               = models.ForeignKey(User, on_delete=models.CASCADE)
    name                = models.CharField(max_length=130)
    slug                = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    description         = models.TextField(null=False, blank=False)
    adults              = models.IntegerField(default=1, null=False, blank=False)
    children            = models.IntegerField(default=1, null=False, blank=False)
    pets_allowed        = models.BooleanField(default=False)
    base_price          = models.DecimalField(default=0, null=False, blank=False, decimal_places=2, max_digits=9)
    cleaning_fee        = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=9)
    image_url           = models.URLField(null=True, blank=False)
    weekly_discount     = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=9)
    monthly_discount    = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=9)

    def __str__(self) -> str:
        return self.slug


class SpecialPrice(models.Model):
    """
    Price object intended to differentiate from base price on special dates.
    """
    id      = HashidAutoField(primary_key=True)
    listing = models.ForeignKey(Listing, related_name='special_prices', on_delete=models.CASCADE)
    date    = models.DateField(null=False, blank=False, verbose_name='date')
    price   = models.DecimalField(blank=False, null=True, decimal_places=2, max_digits=8)

    def __str__(self) -> str:
        return f'{self.price} - {self.date}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id', 'date'], name='One special price per date')
        ]