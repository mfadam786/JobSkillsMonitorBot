from django.db import models
from django.urls import reverse

class location(models.Model):
    area = models.TextField(max_length=100)

class listing(models.Model):
  
    job_type = models.TextField(max_length=100)
    company = models.TextField(max_length=100)
    job_title = models.TextField(max_length=100)
    job_url = models.URLField()
    date_listed = models.DateField()

    location = models.ForeignKey(location, on_delete=models.CASCADE)

