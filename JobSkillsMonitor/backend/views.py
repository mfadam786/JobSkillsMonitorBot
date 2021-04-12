from django.shortcuts import render
from .models import Listing
import pandas as pd
import matplotlib.pyplot as plt
import urllib, base64
import numpy as np
import io
import datetime

from re import search

# Create your views here.

def index(request):
    return render(request, 'backend/index.html')

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

def testPage(request):
    listings = Listing.objects.all().filter(
        job_role = "Management",
    ).values()

    print(len(listings))

    i = [0, 0, 0, 0]
    
    for job in listings:
        if (job['work_type'] == 'Part Time'):
            i[0]+=1
        elif (job['work_type'] == 'Full Time'):
            i[1]+=1
        elif (job['work_type'] == 'Contract/Temp'):
            i[2]+=1
        else:
            i[3]+=1

    work_type_count = { 'part_time' : i[0], 'full_time' : i[1], 'contract' : i[2], 'casual' : i[3] }
    
    print(work_type_count)

    plt.plot(i)

    fig = plt.gcf()

    #converting graph into string buffer and converting 64bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    fig.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'backend/test.html',{"data":uri})

def testPage1(request):
    listings = Listing.objects.all().filter(
        job_role = "Help Desk & IT Support",
    ).values()

    print(len(listings))

    i = [0, 0, 0, 0]
    
    for job in listings:
        if (job['work_type'] == 'Part Time'):
            i[0]+=1
        elif (job['work_type'] == 'Full Time'):
            i[1]+=1
        elif (job['work_type'] == 'Contract/Temp'):
            i[2]+=1
        else:
            i[3]+=1

    work_type_count = { 'part_time' : i[0], 'full_time' : i[1], 'contract' : i[2], 'casual' : i[3] }
    
    print(work_type_count)

    plt.rcdefaults()
    fig, ax = plt.subplots()

    people = work_type_count.keys()
    y_pos = np.arange(len(work_type_count))
    performance = work_type_count.values()
    error = np.random.rand(len(work_type_count))

    ax.barh(y_pos, performance, xerr=error, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(people)
    ax.invert_yaxis()
    ax.set_xlabel('Job Count')
    ax.set_title('Jobs based on their work type')

    #converting graph into string buffer and converting 64bit code into image
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    langs = ['part_time', 'full_time', 'contract', 'casual']
    students = i
    ax.bar(langs,students)

    fig.savefig(buf, format="png")
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return render(request, 'backend/test.html',{"data":uri})

def pie_chart(request):
    display = False
    labels = []
    data = []

    listings = Listing.objects.all().filter(job_role="Help Desk & IT Support")[:5].values()
    
    def getTopProgLanguages():
        csv_data = pd.read_csv('../scaper/data/fixed_langs.csv', index_col=0)

        targets = ['fixed']

        langs = np.array(csv_data[targets])
        print(langs)
        for lang in langs:
            for listing in listings:
                print(listing['data'])
                # for sentences in listing['data']:
                #     # print(sentences)
                

    getTopProgLanguages()
        
    i = [0, 0, 0, 0]
    
    for job in listings:
        if len(listings) > 0:
            display = True

        if (job['work_type'] == 'Full Time'):
            i[0]+=1
        elif (job['work_type'] == 'Part Time'):
            i[1]+=1
        elif (job['work_type'] == 'Contract/Temp'):
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

    return render(request, 'backend/pie_chart.html', context)