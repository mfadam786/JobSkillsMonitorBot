from django.shortcuts import render
from .models import Listing
import pandas as pd
import numpy as np
import datetime
import requests
import json
from requests.structures import CaseInsensitiveDict
from django.views import generic
# Create your views here.

def index(request):
    return render(request, 'backend/index.html')

def test_maps_regions(request):


    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    regions = Listing.objects.values_list('region').distinct()
    urls = []

    region_count = {}


    for region in regions:
        urls.append("https://api.mapbox.com/geocoding/v5/mapbox.places/" + str(region) + ".json?access_token=pk.eyJ1Ijoic21pdGNyNyIsImEiOiJja210eDR2anIwdzR2MnBuczY0ejd5bm96In0.2cXKqmqTnjjUiJEvXS4GGw&types=region&limit=1")

    r = requests.get(urls[0], headers=headers)
    json_dict = r.json()

    for url in urls[1:]:
        
        r = requests.get(url, headers=headers)
        json_dict['features'].append(r.json()['features'][0])
        
    geoJson = json.dumps(json_dict)


    regions = Listing.objects.values_list('region', flat=True)
    for region in list(regions):

        if region in region_count:
            region_count[region] += 1
        else:
            region_count[region] =  1
  
    

    return render(request, 'backend/map_test.html', {'geojson': geoJson, 'region_count': json.dumps(region_count)})

def test_maps_sub_regions(request):


    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    regions = Listing.objects.values_list('region').distinct()
    urls = []

    region_count = {}


    for region in regions:
        urls.append("https://api.mapbox.com/geocoding/v5/mapbox.places/" + str(region) + ".json?access_token=pk.eyJ1Ijoic21pdGNyNyIsImEiOiJja210eDR2anIwdzR2MnBuczY0ejd5bm96In0.2cXKqmqTnjjUiJEvXS4GGw&types=region&limit=1")

    r = requests.get(urls[0], headers=headers)
    json_dict = r.json()

    for url in urls[1:]:
        
        r = requests.get(url, headers=headers)
        json_dict['features'].append(r.json()['features'][0])
        
    geoJson = json.dumps(json_dict)


    sub_regions = Listing.objects.values_list('sub_region', flat=True).distinct()
    for region in list(sub_regions):
        print(region)
        if region in region_count:
            region_count[region] += 1
        else:
            region_count[region] =  1
  
    

    return render(request, 'backend/map_test.html', {'geojson': geoJson, 'region_count': json.dumps(region_count)})


  
def results(request):
    return render(request, 'backend/results.html')

def search(request):
    template_name = 'backend/results.html'

    job_title = request.POST['job_title']

    job_listings = []
    jobs = []

    if (job_title == ''):
        return render(request, 'backend/index.html')
    else:

        listing_table = Listing.objects

        for word in job_title.split(' '):
            jobs += listing_table.all().filter(job_title__icontains=word).values()
            
        for job in jobs:
            if job not in job_listings:
                job_listings.append(job)

        job_count = len(job_listings)
        
        context = { 'job_listing' : job_listings, 'searched_job' : job_title, 'job_count' : job_count }

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