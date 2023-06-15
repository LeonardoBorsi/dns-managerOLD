from django.urls import path
from .views import (
    DeviceListView,
    DeviceDetailView,
    DeviceCreateView,
    DeviceUpdateView,
    DeviceDeleteView
)

urlpatterns = [
    path("", DeviceListView.as_view(), name="device_list"),
    path("new/", DeviceCreateView.as_view(), name="device_new"),
    path("<int:pk>/", DeviceDetailView.as_view(), name="device_detail"),
    path("<int:pk>/edit/", DeviceUpdateView.as_view(), name="device_edit"),
    path("<int:pk>/delete/", DeviceDeleteView.as_view(), name="device_delete"),
]
