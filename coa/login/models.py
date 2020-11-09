from django.db import models

# Create your models here.
class Oauth42(models.Model):
    login = models.CharField(max_length=30, primary_key=True)
    access_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)
