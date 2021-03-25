import requests
import lxml.html

def get_seek_pages():

    end_of_pages = False
    START_URL = "https://www.seek.co.nz/jobs-in-information-communication-technology?page=1"

    urls = []
    url = START_URL

    while not end_of_pages:

        res = requests.get(url)

        if res.ok:
            doc = lxml.html.fromstring(res.content)

            results_div = doc.xpath("//*[@id='app']/div/div[4]/div/div[2]/section/div[2]/div/div[2]/div[1]/div/div[2]/div/div[2]")
            links = doc.xpath("//a[starts-with(@href, '/job/')]")
            for l in links:
                urls.append(l.values()[0].split("?")[0])
            next_url = doc.xpath("//a[text()='Next']")
            if next_url:
                url = f"https://www.seek.co.nz{next_url[0].values()[0]}"
                #print(url)
              #  urls.append(url)



            else:
                end_of_pages = True

        else:
            raise ValueError(f"Error parsing url {url}")

    return list(map(lambda x: f"https://www.seek.co.nz{x}", urls))



print(len(get_seek_pages()))


