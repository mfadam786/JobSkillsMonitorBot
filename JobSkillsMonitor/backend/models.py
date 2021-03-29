from django.db import models
from django.urls import reverse
from django.utils import timezone

class Listing(models.Model):    
    date_listed = models.DateField(default=timezone.now()) #dd-mm-yyyy
    employer = models.TextField(max_length=100, default="")
    company = models.TextField(max_length=100, default="")
    work_type = models.TextField(max_length=15, default="")
    job_role = models.TextField(max_length=50, default="")
    data = models.TextField(default="")

    region = models.TextField(max_length=50, default="")

    sub_region = models.TextField(max_length=50, default="")

    job_title = models.TextField(max_length=100, default="")

