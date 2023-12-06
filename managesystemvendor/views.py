from django.shortcuts import render
# Create your views here.
from rest_framework.generics import UpdateAPIView
from django.db.models import Avg
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets,generics,status
from rest_framework.response import Response
from .models import Vendor,PurchaseOrder
from .serializers import VendorSerializer,PurchaseOrderSerializer
from .serializers import VendorPerformanceSerializer

def hello_world(request):
    return HttpResponse("Hello, World!")

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

        # Check if the status is changing to 'completed'
        if 'status' in serializer.validated_data and serializer.validated_data['status'] == 'completed':
            self.update_on_time_delivery_rate(instance)

        # Check if a quality rating is provided
        if 'quality_rating' in serializer.validated_data and serializer.validated_data['quality_rating'] is not None:
            self.update_quality_rating_avg(instance)

        # Check if acknowledgment_date is provided
        if 'acknowledgment_date' in serializer.validated_data and serializer.validated_data['acknowledgment_date'] is not None:
            self.update_average_response_time(instance)

        # Recalculate and update fulfilment rate
        self.update_fulfillment_rate(instance)

    def update_on_time_delivery_rate(self, instance):
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_orders = [order for order in completed_orders if order.is_delivered_on_time()]
        on_time_delivery_rate = len(on_time_orders) / len(completed_orders) * 100 if completed_orders else 0.0
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()

    def update_quality_rating_avg(self, instance):
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, quality_rating__isnull=False)
        quality_rating_avg = completed_orders.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
        vendor.quality_rating_avg = quality_rating_avg
        vendor.save()

    def update_average_response_time(self, instance):
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        response_times = [order.response_time() for order in completed_orders]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0.0
        vendor.average_response_time = avg_response_time
        vendor.save()

    def update_fulfillment_rate(self, instance):
        vendor = instance.vendor
        all_orders = PurchaseOrder.objects.filter(vendor=vendor)
        successful_orders = all_orders.filter(status='completed', quality_rating__isnull=True)
        fulfillment_rate = len(successful_orders) / len(all_orders) * 100 if all_orders else 0.0
        vendor.fulfillment_rate = fulfillment_rate
        vendor.save()

class VendorPerformanceView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, id=kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class AcknowledgePurchaseOrderView(UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def post(self, request, *args, **kwargs):
        # Your logic to acknowledge the purchase order
        instance = self.get_object()

        # Your logic to update acknowledgment_date
        instance.acknowledgment_date = timezone.now()
        instance.save()

        # Additional logic for recalculating average_response_time
        self.update_average_response_time(instance)

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update_average_response_time(self, instance):
        vendor = instance.vendor
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
        response_times = [order.response_time() for order in completed_orders]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0.0
        vendor.average_response_time = avg_response_time
        vendor.save()