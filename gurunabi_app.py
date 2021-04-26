# GUI系
import tkinter as tk
from tkinter import ttk

import gurunabi  # バック
import config

import configparser as cp

import os
import errno

import textwrap
import webbrowser


class Window():
    # * 初期設定
    def __init__(self):
        # メインウィンドウ
        self.win = tk.Tk()

        # * 値定義
        # エリア情報
        self.place = config.PLACE
        self.pref_list = list(self.place.keys())  # 都道府県リスト
        # 検索キーワード
        self.search_word = tk.StringVar()
        # 検索方式
        self.rbv = tk.IntVar(None, 0)  # デフォルト -> フリーワード検索
        # 都道府県,エリアL,エリアM
        self.cbv_place = []
        for i in range(3):
            self.cbv_place.append(tk.StringVar())

        # * 高度な検索

        # 高度な検索設定情報読み込み
        self.exp_ini = cp.ConfigParser()
        if os.path.exists("./exp.ini"):
            self.exp_ini.read("./exp.ini", encoding="utf-8")  # 読み込み
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "./exp.ini")

        # * 値定義
        # カテゴリ情報
        self.category = config.CATEGORY
        self.categoryL_list = list(self.category.keys())
        # 大カテゴリ,小カテゴリ
        self.cbv_cate = []
        for i in range(2):
            self.cbv_cate.append(tk.StringVar())

        # ランチ営業有無,朝食有無,テイクアウト可否,デリバリー可否
        # 禁煙席有無,個室有無,深夜営業,翌朝営業
        # 飲み放題有無,電源有無,カード決済可否,電子マネー決済可否
        # 駐車場有無,Web予約可否
        # 値定義
        self.ckv_exp = []
        for i in range(14):
            self.ckv_exp.append(tk.BooleanVar())
        # 条件ラベル
        self.exp_label = ["ckv_lunch", "ckv_breakfast", "ckv_takeout", "ckv_delivery", "ckv_nosmoking", "ckv_privateroom",
                            "ckv_midnight", "ckv_untilmorning", "ckv_bottomlesscup", "ckv_outret", "ckv_card", "ckv_emoney",
                            "ckv_parking", "ckv_webreserve"]

        self.flg = 0
        self.iidf = ""

    # * 検索ウィンドウ
    def searchWindow(self):
        # 検索フォーム入力値検証
        def validate_search(P):
            if P == "":
                search_submit['state'] = "disabled"  # submit無効
            else:
                search_submit['state'] = "normal"  # submit有効
            return True

        # ウィンドウ設定
        self.win.title("ぐるぐるぐるナビ(笑)((激寒")  # ウィンドウタイトル
        self.win.resizable(False, False)  # ウィンドウリサイズ無効化
        val_search = self.win.register(validate_search)  # 入力値検証 コールバック登録

        # 検索方式選定
        search_method_frame = ttk.Frame(self.win, padding=8)
        # 検索方式ラベルフレーム
        search_method_labelf = ttk.Labelframe(search_method_frame, text="検索方式", style='My.TLabelframe')
        # 検索方式ラジオボタン
        search_method_rb1 = ttk.Radiobutton(search_method_labelf, text="フリーワード検索", value=0, variable=self.rbv)
        search_method_rb2 = ttk.Radiobutton(search_method_labelf, text="店名検索", value=1, variable=self.rbv)
        search_method_rb3 = ttk.Radiobutton(search_method_labelf, text="住所検索", value=2, variable=self.rbv)

        # 検索地域選定
        search_place_frame = ttk.Frame(self.win, padding=8)
        # 検索地域ラベルフレーム
        search_place_labelf = ttk.Labelframe(search_place_frame, text="検索地域", style='My.TLabelframe', padding=8)
        # 検索地域ラベル(都道府県)
        search_place_pref_label = ttk.Label(search_place_labelf, text="都道府県", padding=(5, 2))
        # 検索地域コンボボックス(都道府県)
        search_place_pref_cb = ttk.Combobox(search_place_labelf, state="readonly", textvariable=self.cbv_place[0], values=self.pref_list)
        search_place_pref_cb.set(self.pref_list[7])  # デフォルト -> 東京都

        # 都道府県に応じてエリアL,エリアM反映
        def changeareaL():
            search_place_areaL_cb.config(values=list(self.place[self.cbv_place[0].get()]['areaL'].keys()))
            search_place_areaL_cb.set(list(self.place[self.cbv_place[0].get()]['areaL'].keys())[0])

            search_place_areaM_cb.config(values=list(self.place[self.cbv_place[0].get()]['areaL'][self.cbv_place[1].get()]['areaM'].keys()))
            search_place_areaM_cb.set(list(self.place[self.cbv_place[0].get()]['areaL'][self.cbv_place[1].get()]['areaM'].keys())[0])
        search_place_pref_cb.bind(
            '<<ComboboxSelected>>',
            lambda e: changeareaL()
        )

        # 検索地域ラベル(エリアL)
        search_place_areaL_label = ttk.Label(search_place_labelf, text="エリアL", padding=(5, 2))
        # 検索地域コンボボックス(エリアL)
        self.cbv_place[1].set(list(self.place[self.cbv_place[0].get()]['areaL'].keys())[0])
        search_place_areaL_cb = ttk.Combobox(search_place_labelf, state="readonly", textvariable=self.cbv_place[1],
                                                values=list(self.place[self.cbv_place[0].get()]['areaL'].keys()))

        # エリアLに応じてエリアM反映
        def changeareaM():
            search_place_areaM_cb.config(values=list(self.place[self.cbv_place[0].get()]['areaL'][self.cbv_place[1].get()]['areaM'].keys()))
            search_place_areaM_cb.set(list(self.place[self.cbv_place[0].get()]['areaL'][self.cbv_place[1].get()]['areaM'].keys())[0])
        search_place_areaL_cb.bind(
            '<<ComboboxSelected>>',
            lambda e: changeareaM()
        )

        # 検索地域ラベル(エリアM)
        search_place_areaM_label = ttk.Label(search_place_labelf, text="エリアM", padding=(5, 2))
        # 検索地域コンボボックス(エリアM)
        self.cbv_place[2].set(list(self.place[self.cbv_place[0].get()]['areaL'][self.cbv_place[1].get()]['areaM'].keys())[0])
        search_place_areaM_cb = ttk.Combobox(search_place_labelf, state="readonly", textvariable=self.cbv_place[2],
                                                value=list(self.place[self.cbv_place[0].get()]['areaL'][self.cbv_place[1].get()]['areaM'].keys()))

        # 高度検索フレーム
        expanded_search_frame = ttk.Frame(self.win, padding=8)
        expanded_search_button = ttk.Button(
            expanded_search_frame,
            text="高度な検索",
            command=self.expanded_search
        )

        # 検索フレーム
        search_frame = ttk.Frame(self.win, padding=8)
        # 検索フォームラベル
        search_label = ttk.Label(search_frame, text="検索ワード", padding=(5, 2))
        # 検索フォーム
        search_form = ttk.Entry(search_frame, width=80, textvariable=self.search_word, validatecommand=(val_search, '%P'), validate='all')
        # 検索ボタン
        search_submit = ttk.Button(
            search_frame,
            state="disabled",
            text="検索",
            command=self.backcallAPI
        )

        # 検索フォーム配置
        search_frame.grid(row=0, column=0)
        search_label.grid(row=0, column=0)
        search_form.grid(row=0, column=1)
        search_submit.grid(row=0, column=2, padx=10)
        # 検索方式ラジオボタン配置
        search_method_frame.grid(row=1, column=0, sticky=tk.W)
        search_method_labelf.grid(row=0, column=0)
        search_method_rb1.grid(row=0, column=0, sticky=tk.W)
        search_method_rb2.grid(row=1, column=0, sticky=tk.W)
        search_method_rb3.grid(row=2, column=0, sticky=tk.W)
        # 検索地域コンボボックス配置
        search_place_frame.place(x=130, y=41)
        search_place_labelf.grid(row=0, column=0)
        search_place_pref_label.grid(row=0, column=0, sticky=tk.W)
        search_place_pref_cb.grid(row=0, column=1)
        search_place_areaL_label.grid(row=1, column=0, sticky=tk.W)
        search_place_areaL_cb.grid(row=1, column=1)
        search_place_areaM_label.grid(row=1, column=2, sticky=tk.W)
        search_place_areaM_cb.grid(row=1, column=3)
        # 高度検索ボタン配置
        expanded_search_frame.grid(row=0, column=2)
        expanded_search_button.grid(row=0, column=0)
        
        # プログラム終了イベント呼び出し
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)
        # 表示
        self.win.mainloop()

    # * APIコール
    def backcallAPI(self):
        g = gurunabi.GurunabiAPI()
        self.result = g.callAPI(self.rbv.get(), self.search_word.get(), self.cbv_place, self.cbv_cate, self.ckv_exp)

        # 検索結果ウィンドウへ
        self.resultWindow()

    # * 高度な検索
    def expanded_search(self):
        # 高度な検索適用
        def expanded_submit():
            self.exp_ini.set('category', 'categoryL', str(self.categoryL_list.index(self.cbv_cate[0].get())))
            self.exp_ini.set('category', 'categoryS', str(list(self.category[self.cbv_cate[0].get()]['categoryS'].keys())
                                                            .index(self.cbv_cate[1].get())))

            # 条件記録
            for i in range(14):
                self.exp_ini.set('terms', self.exp_label[i], str(self.ckv_exp[i].get()))
            with open("./exp.ini", 'w') as f:
                self.exp_ini.write(f)
            exp_win.destroy()  # ウィンドウ閉じる

        # 高度な検索ウィンドウ
        exp_win = tk.Toplevel(self.win)
        exp_win.grab_set()  # 親ウィンドウ操作無効化
        exp_win.title("高度な検索")  # ウィンドウタイトル
        exp_win.resizable(False, False)  # ウィンドウリサイズ無効化

        # カテゴリ指定
        cate_ini = self.exp_ini['category']
        category_frame = ttk.Frame(exp_win, padding=8)
        category_labelf = ttk.LabelFrame(category_frame, text="カテゴリ", padding=8)

        # 大カテゴリラベル
        categoryL_label = ttk.Label(category_labelf, text="大カテゴリ", padding=(5, 2))
        # 大カテゴリコンボボックス
        categoryL_cb = ttk.Combobox(category_labelf, state="readonly", textvariable=self.cbv_cate[0], values=self.categoryL_list)
        categoryL_cb.set(self.categoryL_list[int(cate_ini.get('categoryL'))])

        # 大カテゴリに応じて小カテゴリ反映
        def changecateL():
            categoryS_cb.config(values=list(self.category[self.cbv_cate[0].get()]['categoryS'].keys()))
            categoryS_cb.set(list(self.category[self.cbv_cate[0].get()]['categoryS'].keys())[0])
        categoryL_cb.bind(
            '<<ComboboxSelected>>',
            lambda e: changecateL()
        )

        # 小カテゴリラベル
        categoryS_label = ttk.Label(category_labelf, text="小カテゴリ", padding=(5, 2))
        # 小カテゴリコンボボックス
        categoryS_cb = ttk.Combobox(category_labelf, state="readonly", textvariable=self.cbv_cate[1],
                                    values=list(self.category[self.cbv_cate[0].get()]['categoryS'].keys()))
        categoryS_cb.set(list(self.category[self.cbv_cate[0].get()]['categoryS'].keys())[int(cate_ini.get('categoryS'))])

        # 条件指定
        terms_ini = self.exp_ini['terms']
        terms_frame = ttk.Frame(exp_win, padding=8)
        terms_labelf = ttk.LabelFrame(terms_frame, text="条件指定", padding=8)

        # 値定義
        for i in range(14):
            self.ckv_exp[i].set(terms_ini.get(self.exp_label[i]))

        # 条件指定チェックボックス
        # ランチ営業有
        terms_lunch = ttk.Checkbutton(terms_labelf, text="ランチ営業有", variable=self.ckv_exp[0])
        # 朝食有
        terms_breakfast = ttk.Checkbutton(terms_labelf, text="朝食有", variable=self.ckv_exp[1])
        # テイクアウト可
        terms_takeout = ttk.Checkbutton(terms_labelf, text="テイクアウト可", variable=self.ckv_exp[2])
        # デリバリー可
        terms_delivery = ttk.Checkbutton(terms_labelf, text="デリバリー可", variable=self.ckv_exp[3])
        # 禁煙席有
        terms_nosmoking = ttk.Checkbutton(terms_labelf, text="禁煙席有", variable=self.ckv_exp[4])
        # 個室有
        terms_privateroom = ttk.Checkbutton(terms_labelf, text="個室有", variable=self.ckv_exp[5])
        # 深夜営業
        terms_midnight = ttk.Checkbutton(terms_labelf, text="深夜営業", variable=self.ckv_exp[6])
        # 翌朝営業
        terms_untilmorning = ttk.Checkbutton(terms_labelf, text="翌朝営業", variable=self.ckv_exp[7])
        # 飲み放題有
        terms_bottomlesscup = ttk.Checkbutton(terms_labelf, text="飲み放題有", variable=self.ckv_exp[8])
        # 電源有
        terms_outret = ttk.Checkbutton(terms_labelf, text="電源有", variable=self.ckv_exp[9])
        # カード決済可
        terms_card = ttk.Checkbutton(terms_labelf, text="カード決済可", variable=self.ckv_exp[10])
        # 電子マネー決済可
        terms_emoney = ttk.Checkbutton(terms_labelf, text="電子マネー決済可", variable=self.ckv_exp[11])
        # 駐車場有
        terms_parking = ttk.Checkbutton(terms_labelf, text="駐車場有", variable=self.ckv_exp[12])
        # Web予約可
        terms_webreserve = ttk.Checkbutton(terms_labelf, text="Web予約可", variable=self.ckv_exp[13])

        # 適用ボタン
        exp_submit_frame = ttk.Frame(exp_win, padding=8)
        exp_submit = ttk.Button(
            exp_submit_frame,
            text="適用",
            command=expanded_submit
        )

        # カテゴリ配置
        category_frame.grid(row=0, column=0)
        category_labelf.grid(row=0, column=0)
        categoryL_label.grid(row=0, column=0)
        categoryL_cb.grid(row=0, column=1)
        categoryS_label.grid(row=1, column=0)
        categoryS_cb.grid(row=1, column=1)
        # 条件チェックボックス配置
        terms_frame.grid(row=0, column=1, sticky=tk.W + tk.E)
        terms_labelf.grid(row=0, column=0, sticky=tk.W + tk.E)
        terms_lunch.grid(row=0, column=0, sticky=tk.W + tk.E)
        terms_breakfast.grid(row=0, column=1, sticky=tk.W + tk.E)
        terms_takeout.grid(row=0, column=2, sticky=tk.W + tk.E)
        terms_delivery.grid(row=0, column=3, sticky=tk.W + tk.E)
        terms_nosmoking.grid(row=1, column=0, sticky=tk.W + tk.E)
        terms_privateroom.grid(row=1, column=1, sticky=tk.W + tk.E)
        terms_midnight.grid(row=1, column=2, sticky=tk.W + tk.E)
        terms_untilmorning.grid(row=1, column=3, sticky=tk.W + tk.E)
        terms_bottomlesscup.grid(row=2, column=0, sticky=tk.W + tk.E)
        terms_outret.grid(row=2, column=1, sticky=tk.W + tk.E)
        terms_card.grid(row=2, column=2, sticky=tk.W + tk.E)
        terms_emoney.grid(row=2, column=3, sticky=tk.W + tk.E)
        terms_parking.grid(row=3, column=0, sticky=tk.W + tk.E)
        terms_webreserve.grid(row=3, column=1, sticky=tk.W + tk.E)
        # 適用ボタン配置
        exp_submit_frame.grid(row=1, column=2)
        exp_submit.grid(row=0, column=0)

        exp_win.mainloop()  # ウィンドウ表示

    # * 検索結果
    def resultWindow(self):
        # 検索結果ウィンドウ
        result_win = tk.Toplevel(self.win)
        result_win.title("検索結果")  # ウィンドウタイトル
        result_win.grab_set()  # 親ウィンドウ操作無効化
        result_win.resizable(False, False)  # ウィンドウリサイズ無効化

        result_frame = ttk.Frame(result_win, width=100, padding=8)
        if 'error' in self.result:
            # 見つからなかった
            if self.result['error'][0]['code'] == 404:
                result_label = ttk.Label(result_frame, text="指定された条件の店舗は存在しませんでした。", padding=(5, 2))
                result_frame.grid(row=0, column=0, sticky=tk.W)
                result_label.grid(row=0, column=0, sticky=tk.W)
            else:  # その他のエラー
                from tkinter import messagebox
                messagebox.showerror("エラー: " + str(self.result['error'][0]['code']), self.result['error'][0]['message'])
                result_win.destroy()
        else:
            # ツリービュー
            self.tree = ttk.Treeview(result_frame, height=6, columns=(1, 2, 3, 4), show="headings")

            # 行の高さ変更
            style = ttk.Style(result_frame)
            style.configure("Treeview", rowheight=90)

            # 項目
            self.tree.heading(1, text="店舗名", anchor=tk.W)
            self.tree.heading(2, text="住所/TEL", anchor=tk.W)
            self.tree.heading(3, text="営業時間/休業日", anchor=tk.W)
            self.tree.heading(4, text="PR文", anchor=tk.W)

            # カラム設定
            self.tree.column(1, width=300, minwidth=300, stretch=tk.NO)
            self.tree.column(2, width=400, minwidth=400, stretch=tk.NO)
            self.tree.column(3, width=450, minwidth=450, stretch=tk.NO)
            self.tree.column(4, width=450, minwidth=450, stretch=tk.NO)

            # データ挿入
            for i in range(len(self.result['rest'])):
                name = self.result['rest'][i]['name']  # 店舗名
                add8tel = self.result['rest'][i]['address'] + '\n[TEL]' + self.result['rest'][i]['tel']  # 住所/TEL
                # 営業時間/休業日
                time = '\n'.join(textwrap.wrap(self.result['rest'][i]['opentime'], 40))  # 文字列折返し
                time8holi = '[営業時間]\n' + time + '\n[休業日] ' + self.result['rest'][i]['holiday']
                # PR文
                pr = self.result['rest'][i]['pr']['pr_short']
                pr = '\n'.join(textwrap.wrap(pr, 40))  # 文字列折返し

                # データ挿入
                self.tree.insert("", "end", values=(name, add8tel, time8holi, pr))

            # 水平スクロールバー
            xsb = tk.Scrollbar(result_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
            self.tree["xscrollcommand"] = xsb.set
            # 垂直スクロールバー
            ysb = tk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.tree.yview)
            self.tree["yscrollcommand"] = ysb.set
            self.tree.grid_rowconfigure(0, weight=1)  # カラム幅によってスクロールバー有効化

            # 配置
            result_frame.grid(row=0, column=0, sticky=tk.W)
            self.tree.grid(row=0, column=0)
            xsb.grid(row=1, column=0, sticky=tk.EW)
            ysb.grid(row=0, column=1, sticky=tk.NS)

            # 行が選択されたらイベント発生
            self.tree.bind("<<TreeviewSelect>>", self.openURL)

        result_win.mainloop()  # ウィンドウ表示

    # * サイトURL開く処理
    def openURL(self, event):
        for item in self.tree.selection():
            # 2度クリックされたら
            if self.flg == 1 and self.iidf == item:
                idx = int(item[1:], 16) - 1
                url = self.result['rest'][idx]['url']  # サイトURL
                webbrowser.open(url)  # ブラウザで開く
                self.flg = 0
            else:
                self.flg = 1
                self.iidf = item

    # * プログラム終了処理
    def on_closing(self):
        # iniファイル初期化
        self.exp_ini.set('category', 'categoryL', "0")
        self.exp_ini.set('category', 'categoryS', "0")
        for i in range(14):
            self.exp_ini.set('terms', self.exp_label[i], "False")

        os.remove("./exp.ini")
        with open("./exp.ini", 'w') as f:
            self.exp_ini.write(f)

        self.win.destroy()  # ウィンドウ閉じる


def main():
    w = Window()
    w.searchWindow()


if __name__ == "__main__":
    main()
