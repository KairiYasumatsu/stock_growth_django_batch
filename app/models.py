from django.db import models
from django.utils import timezone

# Create your models here.
class Symbols(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'symbols'

class StockInfo(models.Model):
    stock_info_id = models.BigAutoField(primary_key=True)
    short_name = models.CharField(max_length=255)
    long_name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    full_tiime_employees = models.IntegerField()
    long_bussiness_summary = models.TextField()
    city = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    web_site = models.TextField()
    logo_url = models.TextField()
    industry = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    exchange_time_zone = models.CharField(max_length=255)
    quote_type = models.CharField(max_length=255)
    market = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_info'

class StockPrice(models.Model):
    stock_price_id = models.BigAutoField(primary_key=True)
    stock_info_id = models.PositiveIntegerField()
    previous_close = models.DecimalField(max_digits=9, decimal_places=2)
    open = models.DecimalField(max_digits=9, decimal_places=2)
    day_low = models.DecimalField(max_digits=9, decimal_places=2)
    day_high = models.DecimalField(max_digits=9, decimal_places=2)
    day_diff = models.DecimalField(max_digits=9, decimal_places=2)
    volume = models.DecimalField(max_digits=15, decimal_places=0)
    ask = models.DecimalField(max_digits=9, decimal_places=2)
    bid = models.DecimalField(max_digits=9, decimal_places=2)
    two_hundred_day_average = models.DecimalField(max_digits=9, decimal_places=2)
    fifty_day_average = models.DecimalField(max_digits=9, decimal_places=2)
    average_volume_10days = models.DecimalField(max_digits=15, decimal_places=0)
    average_volume = models.DecimalField(db_column='average_volume', max_digits=15, decimal_places=0)  # Field name made lowercase.
    price_to_sales_trailling_12months = models.DecimalField(max_digits=9, decimal_places=2)
    enterprise_value = models.DecimalField(max_digits=15, decimal_places=0)
    enterprise_to_revenue = models.DecimalField(max_digits=9, decimal_places=2)
    enterprise_to_ebitda = models.DecimalField(max_digits=9, decimal_places=2)
    number_52week_change = models.DecimalField(db_column='number_52week_change', max_digits=9, decimal_places=2)  # Field renamed because it wasn't a valid Python identifier.
    last_fiscal_year_end = models.DecimalField(max_digits=15, decimal_places=0)
    net_income_to_common = models.DecimalField(max_digits=15, decimal_places=0)
    most_recent_quarter = models.DecimalField(max_digits=15, decimal_places=0)
    created_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True, default=timezone.now)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_price'        