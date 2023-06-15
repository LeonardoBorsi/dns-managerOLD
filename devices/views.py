from django.views.generic import ListView, DetailView  # new
from django.views.generic.edit import UpdateView, DeleteView, CreateView  # new
from django.urls import reverse_lazy  # new
from .models import Device

class DeviceListView(ListView):
    model = Device
    template_name = "device/device_list.html"

class DeviceDetailView(DetailView):
    model = Device
    template_name = "device/device_detail.html"

class DeviceCreateView(CreateView):
    model = Device
    template_name = "device/device_new.html"
    fields = (
        "ip_address",
        "name",
    )

class DeviceUpdateView(UpdateView):
    model = Device
    fields = (
        "ip_address",
        "name",
    )
    template_name = "device/device_edit.html"

class DeviceDeleteView(DeleteView):
    model = Device
    template_name = "device/device_delete.html"
    success_url = reverse_lazy("device_list")