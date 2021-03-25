from django.db import models
from django.urls import reverse
from django.utils import timezone

class location(models.Model):
    name = models.TextField(unique=True, max_length=100, default="")

class listing(models.Model):    
    date_listed = models.DateField(default=timezone.now())
    employer = models.TextField(max_length=100, default="")
    company = models.TextField(max_length=100, default="")
    work_type = models.TextField(max_length=15, default="")
    job_role = models.TextField(max_length=50, default="")
    data = models.TextField(default="")

    region = models.ForeignKey('location', on_delete=models.CASCADE, default="")

    city = models.TextField(max_length=50, default="")

    job_title = models.TextField(max_length=100, default="")
    
    # job_type = models.TextField(max_length=100)

