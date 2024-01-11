import time
import json

import requests

base_url = 'https://velox.horse/velox/api/horses/{}/'

with open('to_remove1.json') as f:
    horses = json.loads(f.read())
    ids_remove = list(horses.values())
    flattened_list = []
    for horse_ids in ids_remove:
        for horse_id in horse_ids:
            flattened_list.append(horse_id)

    c = 0
    t = len(flattened_list)
    for horse_id in flattened_list:
        url = base_url.format(horse_id)
        r = requests.delete(url)
        if r.status_code != 204:
            print(r.status_code, r.text, horse_id)
        time.sleep(0.05)
        c += 1
        if not c % 50:
            print(f'{c} out of {t}')


