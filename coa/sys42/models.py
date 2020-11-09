from django.db import models
from login.models import Oauth42

# Create your models here.
class Iscsi(models.Model):

    class IssueOption(models.TextChoices):
        ISCSI = 'IS'

    login = models.ForeignKey(Oauth42, on_delete=models.CASCADE)
    issue = models.CharField(max_length=2, choices=IssueOption.choices)
    updated_at = models.DateTimeField(auto_now=True)
