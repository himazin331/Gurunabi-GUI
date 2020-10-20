import requests
import json

import config

class GurunabiAPI():
    def __init__(self):
        self.url = "https://api.gnavi.co.jp/RestSearchAPI/v3/" # API URL
        self.params = {} # パラメータ
        self.params['keyid'] = config.API_KEY # API Key
        self.place = config.PLACE # 地域
        self.category = config.CATEGORY # カテゴリ
        # パラメータ名
        self.param_name = ["lunch", "breakfast", "takeout", "delivery", "no_smoking", "private_room",
                            "midnight", "until_morning", "bottomless_cup", "outret", "card", "e_money",
                            "parking", "web_reserve"]

    def callAPI(self, rbv, search_word, placel, catel, ckb_exp):

        self.params['hit_per_page'] = 50

        # 検索方式
        if rbv == 0: # フリーワード検索
            self.params['freeword'] = search_word
        elif rbv == 1: # 店名検索
            self.params['name'] = search_word
        elif rbv == 2: # 住所検索
            self.params['address'] = search_word

        # 都道府県
        self.params['pref'] = self.place[placel[0].get()]['placecode']
        # エリアL
        self.params['areacode_l'] = self.place[placel[0].get()]['areaL'][placel[1].get()]['areaLcode']
        # エリアM
        if "None" not in self.place[placel[0].get()]['areaL'][placel[1].get()]['areaM'][placel[2].get()]:
            self.params['areacode_m'] = self.place[placel[0].get()]['areaL'][placel[1].get()]['areaM'][placel[2].get()]

        try:
            # 大カテゴリ
            if "None" not in self.category[catel[0].get()]['categoryL_code']:
                self.params['category_l'] = self.category[catel[0].get()]['categoryL_code']
                # 小カテゴリ
                if "None" not in self.category[catel[0].get()]['categoryS'][catel[1].get()]:
                    self.params['category_s'] = self.category[catel[0].get()]['categoryS'][catel[1].get()]
        except KeyError:
            pass

        # 条件指定
        for i in range(14):
            if ckb_exp[i].get():
                self.params[self.param_name[i]] = 1

        # リクエスト
        result = requests.get(self.url, self.params)
        result = result.json() # json整形

        return result