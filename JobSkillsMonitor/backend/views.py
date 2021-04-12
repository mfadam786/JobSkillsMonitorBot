from django.shortcuts import render
from .models import Listing, Languages, Job_Types, Job_Type_Language_Count
import pandas as pd
import numpy as np
import datetime
import requests
import json
from requests.structures import CaseInsensitiveDict
from django.views import generic

# tsne stuff
import sklearn
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
import io
import urllib, base64

from pathlib import Path
import glob
import os

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


def get_job_locations(request, listings):

    regions = []
    region_count = {}
    


    for job in listings:
        if job['region'] not in regions:
            regions.append(job['region'])
            print(job['region'])

        if job['region'] in region_count:
            region_count[job['region']] += 1
        else:
            region_count[job['region']] =  1


    for region in list(regions):
        if region in region_count:
            region_count[region] += 1
        else:
            region_count[region] =  1
  
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    urls = []



    for region in regions:
        urls.append("https://api.mapbox.com/geocoding/v5/mapbox.places/" + str(region) + ".json?access_token=pk.eyJ1Ijoic21pdGNyNyIsImEiOiJja210eDR2anIwdzR2MnBuczY0ejd5bm96In0.2cXKqmqTnjjUiJEvXS4GGw&types=region&limit=1")

    r = requests.get(urls[0], headers=headers)
    json_dict = r.json()

    for url in urls[1:]:
        
        r = requests.get(url, headers=headers)
        json_dict['features'].append(r.json()['features'][0])
        
    geoJson = json.dumps(json_dict)


    regions = Listing.objects.values_list('region', flat=True)

    output = {'geoJson': geoJson, 'region_count': json.dumps(region_count)}
    
    return output
  
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
        location_data = get_job_locations(request, job_listings)
        context = { 'job_listing' : job_listings, 'searched_job' : job_title, 'job_count' : job_count, 'geojson': location_data['geoJson'], 'region_count': location_data['region_count'] }

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

def tsne_search(request):
    template_name = 'backend/tsne_results.html'

    model = Word2Vec.load("../scaper/models/word2vec_sg.model")

    q = request.POST['tsne_q']

    word = q

    context = {}



    if word in model.wv.vocab:
        arr = np.empty((0, 100), dtype='f')
        word_labels = [word]

        close_words = model.similar_by_word(word)
        arr = np.append(arr, np.array([model[word]]), axis=0)
        for wrd_score in close_words:
            wrd_vector = model[wrd_score[0]]
            word_labels.append(wrd_score[0])
            arr = np.append(arr, np.array([wrd_vector]), axis=0)

        tsne = TSNE(n_components=2, random_state=42)
        np.set_printoptions(suppress=True)
        Y = tsne.fit_transform(arr)
        x_coords = Y[:, 0]
        y_coords = Y[:, 1]
        plt.scatter(x_coords, y_coords)
        for label, x, y in zip(word_labels, x_coords, y_coords):
            plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
            plt.xlim(x_coords.min() + 0.00005, x_coords.max() + 0.00005)
            plt.ylim(y_coords.min() + 0.00005, y_coords.max() + 0.00005)

        fig = plt.gcf()
        buff = io.BytesIO()
        fig.savefig(buff, format="png")

        buff.seek(0)
        string = base64.b64encode(buff.read())

        context["image"]= 'data:image/png;base64,' + urllib.parse.quote(string)

        plt.clf()

    else:
        context["error"] = "error that word is not in the vocabulary"

    if q:
        context["q"] = q

    return render(request, template_name, context)


def load_lang_counts(request):
    p = Path('../scaper/data/subsections')
    csv_files = list(p.glob('*.csv'))

    for csv_file in csv_files:
        filename = os.path.split(csv_file)
        
        job_type = filename[1].split('_')[0]

        new_job_type = Job_Types.objects.filter(job_type = job_type).first()

        if new_job_type is None:
            new_job_type = Job_Types(job_type = job_type)
            new_job_type.save()
        else:
            print('Job type already exists')

        csv_data = pd.read_csv(csv_file, index_col=0)

        targets = ['lang', 'count']

        data = np.array(csv_data[targets])

        print(data)

        for column in data:
            lang = column[0]
            count = column[1]

            new_language = Languages.objects.filter(language = lang).first()

            if new_language is None:
                new_language = Languages(language = lang)
                new_language.save()
            else:
                print('Language already exists')
        
            new_lang_count = Job_Type_Language_Count.objects.filter(language = new_language, job_type = new_job_type, count = count).first()
            
            if new_lang_count is None:
                new_lang_count = Job_Type_Language_Count(language = new_language, job_type = new_job_type, count = count)
                new_lang_count.save()
            else:
                print('Language count data already exists')

        return render(request, 'backend/index.html')