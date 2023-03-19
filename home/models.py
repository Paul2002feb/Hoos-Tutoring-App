from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class TutoringUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_tutor = models.BooleanField(default=False)
    full_name = models.CharField(max_length=50)
    MAJOR_CHOICES = [
        ('ECE', 'Electrical/Computer Engineering'),
        ('BME', 'Biomedical Engineering'),
        ('CS', 'Computer Science'),
        ('HIS', 'History'),
        ('PSY', 'Psychology'),
        ('PSY', 'Psychology')
    ]
    def get_classes_default():
        return list()
    major = models.CharField(max_length=3, choices=MAJOR_CHOICES)
    classes = ArrayField(models.CharField(max_length=20, default="NA"), default=get_classes_default)
    pay_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0)

class TutorRequest(models.Model):
    is_verified = models.BooleanField(default=False)
    request_user = models.CharField(max_length=50)
    request_tutor = models.CharField(max_length=50)
    request_time = models.DateTimeField()