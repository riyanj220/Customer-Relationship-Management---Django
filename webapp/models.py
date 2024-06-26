from django.db import models
from django.conf import settings

class Record(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=50)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + "   " + self.last_name