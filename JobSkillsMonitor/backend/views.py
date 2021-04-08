from django.shortcuts import render
from .models import Listing
import pandas as pd
import numpy as np
import datetime

from django.views import generic
# Create your views here.

def index(request):
    return render(request, 'backend/index.html')

def search(request):
    template_name = 'backend/results.html'

    job_title = request.POST['job_title']

    if (job_title == ''):
        return render(request, 'backend/index.html')
    else:

        listing_table = Listing.objects

        for word in job_title.split(' '):
            job_listing = listing_table.all().filter(job_title__icontains=word).values()
            
        job_count = len(job_listing)
        
        context = { 'job_listing' : job_listing, 'searched_job' : job_title, 'job_count' : job_count }

        return render(request, template_name, context)

def store_data(request):

    csv_data = pd.read_csv('../scaper/data/scraped.csv', index_col=0)

    targets = ['date_listed', 'employer', 'job_hours', 'job_subsection', 'main_content', 'main_location', 'sub_location', 'title']

    data = np.array(csv_data[targets])

    i = 0

    for column in data:
        date_listed = datetime.datetime.strptime(column[0], '%d-%b-%y').strftime('%Y-%m-%d')
        employer = column[1]
        work_type = column[2]
        job_role = column[3]
        content = column[4]
        region = column[5]
        sub_region = column[6]
        title = column[7]
        
        listing = Listing.objects.filter(
            date_listed = date_listed,
            employer = employer,
            work_type = work_type,
            job_role = job_role,
            data = content,
            region = region,
            sub_region = sub_region,
            job_title = title
        ).first()

        if listing is None:
            listing = Listing(
                date_listed = date_listed,
                employer = employer,
                work_type = work_type,
                job_role = job_role,
                data = content,
                region = region,
                sub_region = sub_region,
                job_title = title
            )
            listing.save()
        else:
            print('Listing already exists')

        i += 1

    print('Listings:')
    print(Listing.objects.all())

    print(i)
    return render(request, 'backend/test.html')