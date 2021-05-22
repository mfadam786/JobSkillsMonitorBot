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


class Job_Pay(models.Model):
    job_title = models.TextField(max_length=100, default="")
    pay = models.IntegerField(default=0)
    lower_pay = models.IntegerField(default=0)
    upper_pay = models.IntegerField(default=0)

class Job_Language_Count(models.Model):
    language = models.TextField(max_length=50, default="")
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)

class Job_Language_Count_Completed(models.Model):
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    language = models.TextField(max_length=50, default="")
    count = models.IntegerField(default=0)

class Frameworks(models.Model):
    framework = models.TextField(max_length=100, default="")


class Frameword_Listing_Count(models.Model):
    listing = models.ForeignKey("Listing", on_delete=models.CASCADE)
    framework = models.ForeignKey("Frameworks", on_delete=models.CASCADE)

class SoftSkills(models.Model):
    softskill = models.TextField(max_length=100, default="")

class SoftSkills_Listing_Count(models.Model):
    listings = models.ForeignKey("Listing", on_delete=models.CASCADE)
    softskill = models.ForeignKey("SoftSkills", on_delete=models.CASCADE) 
