from django.db import models
from django.urls import reverse

class Device(models.Model):
    ip_address = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:   # displayed row name in admin
        return str(self.pk) + " " + str(self.ip_address) + " " + str(self.name)
    
    def get_absolute_url(self):
      return reverse("device_detail", kwargs={"pk": self.pk})

