from index import app
from flask import render_template
import os
import requests

api_key = os.getenv('REGULATIONS_GOV_API_KEY')

def fetch_regulations(agency_names):
    url =  'https://api.regulations.gov/v4/documents?filter[searchTerm]=CMS-1808-P'
    headers = {'Authorization': f'Bearer {api_key}'}
    params = {
        'filter[agencyNames]': ','.join(agency_names),
        'sort': 'commentEndDate:desc',
        'page[size]': 10
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    agencies_of_interest = ['HHS', 'ONC', 'CMS', 'FDA', 'CDC', 'OCR', 'SAMSHA', 'FTC', 'White House']
    user_interests = ['Healthcare Reform']
    regulations_data = fetch_regulations(agencies_of_interest)
    
    regulations = []
    if regulations_data:
        for item in regulations_data.get('data', []):
            bill_name = item.get('attributes', {}).get('title', 'N/A')
            comment_end_date = item.get('attributes', {}).get('commentEndDate', 'N/A')
            highlight = any(interest.lower() in bill_name.lower() for interest in user_interests)
            regulations.append({
                'bill_name': bill_name,
                'comment_period_end': comment_end_date,
                'highlight': highlight
            })
    
    return render_template(
        'home.html',
        app_title='Dashboard',
        regulations=regulations
    )
