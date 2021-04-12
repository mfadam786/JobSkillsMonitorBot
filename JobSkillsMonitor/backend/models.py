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


class Languages(models.Model):
    language = models.TextField(max_length=100, default="")

class Job_Types(models.Model):
    job_type = models.TextField(max_length=100, default="")


class Job_Type_Language_Count(models.Model):

    language = models.ForeignKey("Languages", on_delete=models.CASCADE)
    job_type = models.ForeignKey("Job_Types", on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
