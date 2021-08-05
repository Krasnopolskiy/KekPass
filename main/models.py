from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class KekPass(models.Model):
    host = models.CharField(max_length=255, default='')
    password = models.CharField(max_length=255, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
