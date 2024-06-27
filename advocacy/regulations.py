from dotenv import load_dotenv
import json
import os
import requests

load_dotenv()

REGULATIONS_API_KEY = os.environ.get("REGULATIONS_API_KEY")
url = "https://api.regulations.gov/v4/comments/CMS-2024-0131-0001"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Api-Key": f"{REGULATIONS_API_KEY}"}
# GET the comment return - to activate this endpoint, we would use a POST with the comment
response = requests.get(url, headers=headers)
# return data.attributes.docketId
print (response.json()["data"]["attributes"]["docketId"])
