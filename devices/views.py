from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.db.models import Case, When, IntegerField
from .models import Device, Port
from django.contrib.auth.mixins import LoginRequiredMixin

def devices(request):
    if request.user.is_superuser:
        return DeviceListView.as_view()(request)
    else:
        return UserDeviceListView.as_view()(request)

class DeviceListView(ListView):
    model = Device
    template_name = "device/device_list.html"
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            null_accepted=Case(
                When(accepted__isnull=True, then=0),
                When(accepted__in=[True, False], then=1),
                output_field=IntegerField(),
                default=2,
            )
        ).order_by('null_accepted')
        return queryset

class UserDeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = "device/device_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=self.request.user).annotate(
            null_accepted=Case(
                When(accepted__isnull=True, then=0),
                When(accepted__in=[True, False], then=1),
                output_field=IntegerField(),
                default=2,
            )
        ).order_by('null_accepted')
        return queryset
   

class DeviceDetailView(DetailView):
    model = Device
    template_name = "device/device_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = self.get_object()
        ports = Port.objects.filter(device=device)
        context['ports'] = ports
        return context
    
    def set_port_accepted(self, port_id, accepted):
        port = get_object_or_404(Port, pk=port_id)
        port.accepted = accepted
        port.save()
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Check if 'accept_button' or 'reject_button' in request.POST
        if 'accept_button' in request.POST:
            self.object.accepted = True
            self.object.save()
        elif 'reject_button' in request.POST:
            self.object.accepted = False
            self.object.save()

        # Check if 'accept_port_button' or 'reject_port_button' in request.POST
        port_id = request.POST.get('port_id')
        if 'accept_port_button' in request.POST:
            self.set_port_accepted(port_id, True)
        elif 'reject_port_button' in request.POST:
            self.set_port_accepted(port_id, False)

        return HttpResponseRedirect(self.request.path)
    
    #def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'accept_button' in request.POST:
            self.object.accepted = True
            self.object.save()
            return redirect(self.object.get_absolute_url())
        if 'reject_button' in request.POST:
            self.object.accepted = False
            self.object.save()
            return redirect(self.object.get_absolute_url())
        return super().post(request, *args, **kwargs)
        

class DeviceCreateView(CreateView):
    model = Device
    template_name = "device/device_new.html"
    fields = (
        "ip_address",
        "name",
    )
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

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

class PortCreateView(CreateView):
    model = Port
    fields = ['number']
    template_name = 'device/port/port_new.html'

    def form_valid(self, form):
        device = get_object_or_404(Device, pk=self.kwargs['pk'])
        form.instance.device = device
        return super().form_valid(form)

    def get_success_url(self):
        device_id = self.kwargs['pk']
        return reverse_lazy('device_detail', kwargs={'pk': device_id})
    
class PortUpdateView(UpdateView):
  model = Port
  fields = ["number"]
  template_name = "device/port/port_edit.html"

  def get_object(self, queryset=None):
        port_pk = self.kwargs.get('port_pk')
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=port_pk)

  def get_queryset(self):
      queryset = super().get_queryset()
      device_id = self.kwargs.get('pk')
      return queryset.filter(device_id=device_id)
  
  def get_success_url(self):
        device_id = self.kwargs.get('pk')
        return reverse_lazy('device_detail', kwargs={'pk': device_id})

class PortDeleteView(DeleteView):
    model = Port
    template_name = "device/port/port_delete.html"

    def get_object(self, queryset=None):
        port_pk = self.kwargs.get('port_pk')
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=port_pk)

    def get_success_url(self):
        device_id = self.kwargs.get('pk')
        return reverse_lazy('device_detail', kwargs={'pk': device_id})

