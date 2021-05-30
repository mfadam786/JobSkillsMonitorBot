from django.shortcuts import render
from .models import Listing, Languages, Job_Types, Job_Type_Language_Count, Job_Pay, Job_Language_Count, Job_Language_Count_Completed, Frameword_Listing_Count, SoftSkills_Listing_Count
import pandas as pd
import numpy as np
import datetime
import requests
import json
from requests.structures import CaseInsensitiveDict
from django.views import generic
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import Count

# tsne stuff
import sklearn
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
import io
import urllib, base64

from collections import Counter
from pathlib import Path
import glob
import os

# Create your views here.

def index(request):
    return render(request, 'backend/index.html')

def test_maps_regions(request):

    languages = Languages.objects.all().values()
    # print(languages)
    
    # results = Listing.objects.annotate(search=SearchVector('data')).filter(search='Web developer').annotate(search=SearchVector('data')).filter(search='C#')

    # print(len(results))
    # print(results[0].data)
    # print(results.objects.annotate(search=SearchVector('data')).filter(search='Web developer'))
    # for result in results:
    count = {}
    for l in languages[:10]:
        result = Listing.objects.annotate(search=SearchVector('data')).filter(search='Web developer').annotate(search=SearchVector('data')).filter(search=l['language'])

    
    return render(request, 'backend/test.html', {'count': count})

def get_job_locations(request, listings):

    regions = []
    region_count = {}
    


    for job in listings:
        if job.region not in regions:
            regions.append(job.region)

        if job.region in region_count:
            region_count[job.region] += 1
        else:
            region_count[job.region] =  1


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


def get_language_count(request, listings):
    language_count = {}
    for listing in listings[:50]:
        temp = Job_Language_Count_Completed.objects.filter(id=listing.id)
        for t in temp:
            if t.language in language_count:
                language_count[t.language] += 1
            else:
                language_count[t.language] = 1
    print(language_count)
    return(language_count)


def get_frameworks(request, listings) :

    frameworks = [] 
    for l in listings[:10]:
        frameworks_obj = Frameword_Listing_Count.objects.filter(listing=l)

        for f in frameworks_obj:
            frameworks.append(f.framework.framework)
            
    frameworks_counted = Counter(frameworks)
    
    new_shortened_frameworks_counted_list = dict(list(frameworks_counted.items())[:10])

    return(new_shortened_frameworks_counted_list)

def get_softskills(request, listings) :
    
    softskills = [] 
    for l in listings[:10]:
        softskills_obj = SoftSkills_Listing_Count.objects.filter(listings=l)

        for s in softskills_obj:
            softskills.append(s.softskill.softskill)
            
    softskills_counted = Counter(softskills)
    
    new_shortened_softskills_counted_list = dict(list(softskills_counted.items())[:10])

    return(new_shortened_softskills_counted_list)



def search(request):
    def getWorkTypeData(listings):
        display = False
        labels = []
        data = []
         
        i = [0, 0, 0, 0]
        
        for job in listings:
            if len(listings) > 0:
                display = True

            if (job.work_type == 'Full Time'):
                i[0]+=1
            elif (job.work_type == 'Part Time'):
                i[1]+=1
            elif (job.work_type == 'Contract/Temp'):
                i[2]+=1
            else:
                i[3]+=1

        work_type_count = { 'Full Time' : i[0], 'Part Time' : i[1], 'Contract/Temp' : i[2], 'Casual/Vacation' : i[3] }
        
        for key, value in work_type_count.items():
            labels.append(key)
            data.append(value)

        context = {
            'labels' : labels,
            'data' : data,
            'display' : display
        }

        return context

    def getRegionJobCountData(listings):
        display = False
        labels = []
        data = []
        
        regions = []
        regional_job_count = {}

        i = []
        
        for job in listings:
            if len(listings) > 0:
                display = True

            if job.region not in regions:
                regions.append(job.region)

            if job.region in regional_job_count:
                regional_job_count[job.region] += 1
            else:
                regional_job_count[job.region] =  1
        
        for key, value in regional_job_count.items():
            labels.append(key)
            data.append(value)

        context = {
            'labels' : labels,
            'data' : data,
            'display' : display
        }
        
        return context

    template_name = 'backend/results.html'

    job_title = request.POST['job_title']

    job_listings = []
    jobs = []

    if (job_title == ''):
        return render(request, 'backend/index.html')
    else:
        
        for word in job_title.split(' '):
            jobs += Listing.objects.annotate(search=SearchVector('job_title')).filter(search=word)
            jobs += Listing.objects.annotate(search=SearchVector('job_title')).filter(search=word).annotate(search=SearchVector('data')).filter(search='C#')

            
        for job in jobs:
            if job not in job_listings:
                job_listings.append(job)


        job_count = len(job_listings)
        location_data = get_job_locations(request, job_listings)


        work_type_data = getWorkTypeData(job_listings)

        regional_job_count = getRegionJobCountData(job_listings)
        
        seek_search_parameter = ""
        indeed_search_parameter = ""

        for word in job_title.split():
            seek_search_parameter += word + "-"
            indeed_search_parameter += word + "+"

        seek_url = "https://www.seek.co.nz/" + seek_search_parameter + "jobs"
        indeed_url = "https://nz.indeed.com/jobs?q=" + indeed_search_parameter + "&l="

        lang_count = get_language_count(request, job_listings)

        lang_count = {k:lang_count[k] for k in lang_count}
        job_pay = Job_Pay.objects.annotate(search=SearchVector('job_title')).filter(search='web')


        frameworks = get_frameworks(request, job_listings)
        softskills = get_softskills(request, job_listings)



        context = {
            'frameworks': frameworks,
            'softskills': softskills,
            'job_listing': job_listings,
            'searched_job': job_title,
            'job_count': job_count,
            'geojson': location_data['geoJson'],
            'region_count': location_data['region_count'],
            'work_type_data_labels': work_type_data['labels'],
            'work_type_data': work_type_data['data'],
            'work_type_data_display': work_type_data['display'],
            'regional_job_count_data_labels': regional_job_count['labels'],
            'regional_job_count_data': regional_job_count['data'],
            'regional_job_count_data_display': regional_job_count['display'],
            'seek_url': seek_url,
            'indeed_url': indeed_url,
            'job_pay': job_pay[0],
            'lang_count': lang_count
        }

        model = Word2Vec.load("../scaper/models/word2vec_bi_manual_cb.model")

        q = job_title

        if len(q.split(" ")) > 1:
            word = "_".join(q.split(" "))
        else:
            word = q



        if word in model.wv.key_to_index.keys():
            arr = np.empty((0, 100), dtype='f')
            word_labels = [word]

            close_words = model.wv.most_similar(word)
            arr = np.append(arr, np.array([model.wv[word]]), axis=0)
            for wrd_score in close_words:
                wrd_vector = model.wv[wrd_score[0]]
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

            context["image"] = 'data:image/png;base64,' + urllib.parse.quote(string)

            plt.clf()

        else:
            context["error"] = "error that word is not in the vocabulary"

        if q:
            context["q"] = q
        



        return render(request, template_name, context)

def tsne_search(request):
    template_name = 'backend/tsne_results.html'

    model = Word2Vec.load("../scaper/models/word2vec_bi.model")

    q = request.POST['tsne_q']

    if len(q.split(" ")) > 1:
        word = "_".join(q.split(" "))
    else:
        word = q

    context = {}


    if word in model.wv.vocab:
        arr = np.empty((0, 50), dtype='f')
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