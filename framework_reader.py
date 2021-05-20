import pandas as pd
import numpy as np
import sys, os
from backend.models import Frameworks



csv_data = pd.read_csv('../scaper/data/cleaned/frameworks.csv')

targers = ['linenums', 'framework']

data = np.array(csv_data[targers])

for column in data:
    line_number = column[0]
    framework = column[1]
    print(framework)
    framework_obj = Frameworks(framework=framework)
    framework_obj.save()

all_entries = Frameworks.objects.all()
print(all_entries)