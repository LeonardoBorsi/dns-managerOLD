from django.urls import path
from .views import (
    devices,
    DeviceDetailView,
    DeviceCreateView,
    DeviceUpdateView,
    DeviceDeleteView,
    PortCreateView,
    PortUpdateView,
    PortDeleteView,
)

urlpatterns = [
    path("", devices, name="device_list"),
    path("new/", DeviceCreateView.as_view(), name="device_new"),
    path("<int:pk>/", DeviceDetailView.as_view(), name="device_detail"),
    path("<int:pk>/edit/", DeviceUpdateView.as_view(), name="device_edit"),
    path("<int:pk>/delete/", DeviceDeleteView.as_view(), name="device_delete"),
    path("<int:pk>/new-port/", PortCreateView.as_view(), name="port_new"),
    path("<int:pk>/<int:port_pk>/edit-port/", PortUpdateView.as_view(), name='port_edit'),
    path("<int:pk>/<int:port_pk>/delete-port/", PortDeleteView.as_view(), name='port_delete'),
]
