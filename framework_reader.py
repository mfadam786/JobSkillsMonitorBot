import pandas as pd
import numpy as np
import sys, os
from backend.models import SoftSkills, SoftSkills_Listing_Count, Frameword_Listing_Count, Frameworks, Listing, Languages


def 
# csv_data = pd.read_csv('../scaper/data/cleaned/frameworks.csv')

# targers = ['linenums', 'framework']

# data = np.array(csv_data[targers])

# for column in data:
#     line_number = column[0]
#     framework = column[1]
#     print(framework)
#     framework_obj = Frameworks(framework=framework)
#     framework_obj.save()

# all_entries = Frameworks.objects.all()
# print(all_entries)


# csv_data = pd.read_csv('../scaper/data/cleaned/soft_skills.csv')

# targers = ['softskills']

# data = np.array(csv_data[targers])

# for column in data:
#     softskill = column[0]
#     print(softskill)
#     softskill_obj = SoftSkills(softskill=softskill)
#     softskill_obj.save()

# all_entries = SoftSkills.objects.all()
# print(all_entries)


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


def load_lang_counts(request):
    p = Path('../scaper/data/subsections')
    csv_files = list(p.glob('*.csv'))

    # print(csv_files)
    for csv_file in csv_files:
        filename = os.path.split(csv_file)
        
        job_type = filename[1].split('_')[0]

        print(job_type)

        new_job_type = Job_Types.objects.filter(job_type = job_type).first()

        print(new_job_type)
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
            if(count > 0):
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
        print('=========================================')
    return render(request, 'backend/index.html')





language_count = {}
for listing in listings[:50]:
    temp = Job_Language_Count_Completed.objects.filter(id=listing.id)
    for t in temp:
        if t.language in language_count:
            language_count[t.language] += 1
        else:
            language_count[t.language] = 1


print('|----------------| Starting |----------------|')

framework_count = Frameword_Listing_Count.objects.filter(framework=1)[:10]
print(framework_count)

print('|----------------| Ending |----------------|')
