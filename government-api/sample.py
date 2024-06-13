# bring in libraries for API calls
import requests
import json

#get DATAGOV_API_KEY key from environment
import os
api_key = os.getenv('DATAGOV_API_KEY')

# testing grabbing stuff from the regulations API
# you can find API docs at: https://open.gsa.gov/api/regulationsgov/

url = "https://api.regulations.gov/v4/documents?filter[searchTerm]=CMS-1808-P"

# make request, with api_key in the headers as x-api-key
r = requests.get(url, headers={'x-api-key': api_key})
data = r.json()

print(data)


