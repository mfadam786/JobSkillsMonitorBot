from django.shortcuts import render
from .models import location, listing
import pandas as pd

# Create your views here.

def index(request):
    return render(request, 'backend/index.html')

def store_data(request):

    csv_data = pd.read_csv('../scaper/data/scraped.csv')
    
    print(csv_data.values)

    

    return render(request, 'backend/test.html')
    