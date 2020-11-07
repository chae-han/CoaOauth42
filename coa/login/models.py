from django.db import models

# Create your models here.
class Oauth42(models.Model):
    login = models.CharField(max_length=30, primary_key=True)
    access_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=True)

class Iscsi(models.Model):

    class IssueOption(models.TextChoices):
        ISCSI = 'IS'

    login = models.ForeignKey(Oauth42, on_delete=models.CASCADE)
    issue = models.CharField(max_length=2, choices=IssueOption.choices)
    updated_at = models.DateTimeField(auto_now=True)
