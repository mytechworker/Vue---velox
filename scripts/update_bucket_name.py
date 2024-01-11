
import time
import requests

HOST = 'https://velox-ezvwl7dg6a-uc.a.run.app'
# HOST = 'http://localhost:8000'
API_URL = f'{HOST}/velox/api/measures/'

NEW_BUCKET_NAME = 'velox-biomechanics-data'

url = API_URL
while url:
    resp_data = requests.get(url).json()
    measures = resp_data['results']
    url = resp_data['next']
    print(url)
    for mes in measures:
        mes_id = mes.pop('id')
        measure_url = API_URL + str(mes_id) + '/'
        mes['gcs_bucket'] = NEW_BUCKET_NAME
        mes['biomechanics_video_score'] = None
        mes['biomechanics_video_probability'] = None

        r = requests.put(measure_url, json=mes)
        print(mes_id)
        time.sleep(0.1)

