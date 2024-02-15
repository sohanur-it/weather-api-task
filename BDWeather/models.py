from django.db import models

# Create your models here.

class District(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    lat = models.CharField(max_length=255, blank=True, null=True)
    long = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class DistTemp(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    date_time = models.DateTimeField(blank=True, null=True)
    temp = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.temp}_{self.district.name}_{self.date_time.date()}"
