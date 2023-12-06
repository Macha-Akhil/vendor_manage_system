# vendor_manage_system | Django Developer project | Vendor Management System with Performance Metrics
#Objective:

Develop a Vendor Management System using Django and Django REST Framework. This
system will handle vendor profiles, track purchase orders, and calculate vendor performance
metrics

#API Endpoints:

● POST /api/vendors/: Create a new vendor.

● GET /api/vendors/: List all vendors.

● GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.

● PUT /api/vendors/{vendor_id}/: Update a vendor's details.

● DELETE /api/vendors/{vendor_id}/: Delete a vendor.

#API Endpoints:

● POST /api/purchase_orders/: Create a purchase order.

● GET /api/purchase_orders/: List all purchase orders with an option to filter by
vendor.

● GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.

● PUT /api/purchase_orders/{po_id}/: Update a purchase order.

● DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.

#API Endpoints:

● GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance
metrics.

#API Endpoint Implementation :

--> Vendor Performance Endpoint (GET /api/vendors/{vendor_id}/performance):

● Retrieves the calculated performance metrics for a specific vendor.Should return data including on_time_delivery_rate, quality_rating_avg,average_response_time, and fulfillment_rate.

● Update Acknowledgment Endpoint:

● While not explicitly detailed in the previous sections, consider an endpoint like,

--> POST /api/purchase_orders/{po_id}/acknowledge for vendors to acknowledge POs.

● This endpoint will update acknowledgment_date and trigger the recalculation
of average_response_time.
