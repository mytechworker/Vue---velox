
import requests

BASE_URL = 'https://velox.horse/velox/api/horses/'

url = BASE_URL
while url:
    print(f'fetching url: {url}')
    resp = requests.get(url).json()
    results = resp['results']
    url = resp['next']
    for item in results:
        data = {}
        active = item['active']
        elite = item['elite']
        status = item['status']

        if active == 'yes':
            active = 'Yes'
            data['active'] = active
        if elite == 'yes':
            elite = 'Yes'
            data['elite'] = elite
        if status == '':
            status = 'Unnamed'
            data['status'] = status
        if data:
            horse_url = f"{BASE_URL}{item['id']}/"
            r = requests.patch(horse_url, json=data)
            print(r.status_code, data)
