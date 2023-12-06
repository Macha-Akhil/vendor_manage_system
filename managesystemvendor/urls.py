from django.urls import path,include
from .views import hello_world
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet,PurchaseOrderViewSet,VendorPerformanceView,AcknowledgePurchaseOrderView

app_name = 'managesystemvendor'

router = DefaultRouter()
router.register(r'api/vendors', VendorViewSet, basename='vendor')
router.register(r'api/purchase_orders', PurchaseOrderViewSet, basename='purchase_order')

urlpatterns = [
    path('', include(router.urls)),
    path('api/vendors/<int:pk>/performance/', VendorPerformanceView.as_view(), name='vendor_performance'),
    path('api/purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),
    path('hello/', hello_world, name='hello_world'),
]