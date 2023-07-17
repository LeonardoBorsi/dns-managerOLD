from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError
from django.urls import reverse

class Device(models.Model):
    ip_address = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=50)
    accepted = models.BooleanField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk) + " | " + str(self.ip_address) + " - " + str(self.name) + " / User: " + str(self.created_by.username)
    
    def get_absolute_url(self):
      return reverse("device_detail", kwargs={"pk": self.pk})
    
    def get_add_port_url(self):
      return  reverse("port_new", kwargs={"pk": self.pk})
    
class Port(models.Model):
    number = models.IntegerField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    accepted = models.BooleanField(null=True)

    def __str__(self):
        return str(self.pk) + " | " + str(self.number) + " (" + str(self.device.ip_address) + ")"

