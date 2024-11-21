import requests
import re
import hashlib
import json
from lxml import etree

def get_content(url):
    name = hashlib.md5(url.encode('utf-8')).hexdigest()
    try:
        with open(name, 'r', newline='', encoding="utf-8") as f:
            content = f.read()
            return content
    except:
        response = requests.get(
            url,
            headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0 (Edition std-1)'
            }
        )
        with open(name, 'w', newline='', encoding="utf-8") as f:
            f.write(response.text)
        return response.text

if __name__ == '__main__':
    text = get_content('https://www.lejobadequat.com/emplois')
    pattern = r'<h3 class="jobCard_title m-0">(.+)\<\/h3>'
    job_match = re.findall(pattern, text)
    #print(job_match, type(job_match))

    tree = etree.HTML(text)
    xpath = '//article/a/@href'
    url_match = tree.xpath(xpath)
    #print(url_match, type(url_match))

    all_match = [{'title': job, 'url': url} for job, url in zip(job_match, url_match)]
    #print(all_match, type(all_match))

    all_match = json.dumps(all_match)
    obj = json.loads(all_match)
    json_formatted_str = json.dumps(obj, indent=4)

    with open('job_name.txt', 'w', newline='', encoding="utf-8") as f:
        f.write(json_formatted_str)
