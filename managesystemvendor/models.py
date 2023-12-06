from django.db import models
from django.utils import timezone
from datetime import datetime


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.CharField(max_length=10)
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    # Performance Metrics
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    order_date = models.DateField()
    delivery_date = models.DateTimeField(default=timezone.now())
    items = models.TextField()  # You might want to consider a more structured approach for items
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(default=datetime.now)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Purchase Order #{self.po_number} for {self.vendor.name}"
    def is_delivered_on_time(self):
        return self.status == 'completed' and self.delivery_date <= timezone.now()
    def has_quality_rating(self):
        return self.quality_rating is not None
    def response_time(self):
        if self.acknowledgment_date and self.issue_date:
            return (self.acknowledgment_date - self.issue_date).total_seconds() / 60  # return in minutes


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"