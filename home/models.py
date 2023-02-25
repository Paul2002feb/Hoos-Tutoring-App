from django.db import models
from django.contrib.auth.models import User

class TutoringUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)