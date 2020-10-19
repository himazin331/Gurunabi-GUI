import requests
import json

import config

import pprint

def main():
    url = "https://api.gnavi.co.jp/RestSearchAPI/v3/"

    params={}
    params["keyid"] = config.API_KEY

    params["name"] = "ピザ"


    result = requests.get(url, params)
    result = result.json()

    #pprint.pprint(result)

    print(result['rest'][0]['address'])


    print(result['rest'][0]['name_kana'])


    print(result['rest'][0]['code']['areaname'])


    print(result['rest'][0]['code']['category_name_l'][:2])

if __name__ == '__main__':
    main()