import json
import random
import requests
import requests.exceptions
from collections import deque
import re
import csv
import time


keywords = []

with open('collegeList.csv', 'rb') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		keywords.append(row['institution'])

SEARCH_URL   = "http://ajax.googleapis.com/ajax/services/search/web"

colleges = []



def main():

    for kw in keywords[223:300]:
        # get search results for this keyword
        time.sleep(random.choice([10,20,30]))
        print kw
        resp = requests.get(SEARCH_URL, params={'v':'1.0', 'q':kw + "undergraduate+admissions+contact+us"})
        data = json.loads(resp.content)
        results = data['responseData']['results']

        # reduce to [(title,url), ...]
        pages = [(res['url']) for res in results]

        url = pages[0]
        try:
        	response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        	continue
        # find all emails
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))

        best_emails = []
        # parse out the bad emails only go for ones with admissions
        for email in new_emails:
        	if "admi" in email:
        		best_emails.append(email)

        urlDict = {"college" : kw,
        			"admissions_URL" : url,
        			"emails" : best_emails}
        if len(best_emails) == 0:
	        urlDict = {"college" : kw,
	        			"admissions_URL" : url,
	        			"emails" : list(new_emails)}
		
	writeWithDict(urlDict)
        # add dictionary to list of colleges 
        # colleges.append(urlDict)


def writeWithDict(urlDict):
	# print "we got called"
    with open('names3.csv', 'a') as csvfile:
    	writer = csv.writer(csvfile)
	    # for iCollege in colleges:
	writer.writerow([urlDict['college'], urlDict['admissions_URL'], urlDict['emails']])



if __name__=="__main__":
    main()



