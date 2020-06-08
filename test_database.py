from models.DataRepository import DataRepository
import os
import json

with open('data/blacklist.json', 'r') as fp:
    blacklisted_categories = json.load(fp)

for category in blacklisted_categories['categories']:
    try:
        DataRepository.create_category(category, '', 1)
    except Exception as ex:
        print(ex)
