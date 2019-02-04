import requests
import lxml.html as lh
import pandas as pd
import json

url='http://www.iitg.ac.in/acad/acadCal/Acad_Calendar_2018.htm'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')


i=0
jsn = {}
for T in tr_elements[1:-2]:
    if len(T) != 2:
        if i is 1:
            break
        else:
            i+=1
            continue
    u = T[1]
    t = T[0]
    event=t.text_content()[4:-2]
    date=u.text_content().split(',')[0].split('\n')[-1][2:]
    if len(date.split(' ')) is 3:
        jsn[date]=event

with open('result.json', 'w') as outfile:
    json.dump(jsn, outfile)
