import requests
import lxml.html

def get_seek_pages():


    end_of_pages = False
    START_URL = "https://www.seek.co.nz/jobs-in-information-communication-technology?page=1"

    urls = [START_URL, ]

    url = START_URL


    while not end_of_pages:

        res = requests.get(url)

        if res.ok:
            doc = lxml.html.fromstring(res.content)
            next_url = doc.xpath("//a[text()='Next']")
            if next_url:
                url = f"https://www.seek.co.nz{next_url[0].values()[0]}"
                print(url)

                urls.append(url)
                break
            else:
                end_of_pages = True

        else:
            raise ValueError(f"Error parsing url {url}")

    return urls


print(get_seek_pages())



