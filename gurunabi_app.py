import tkinter as tk
from tkinter import ttk

import gurunabi
import config

import configparser as cp

import os
import errno

# 検索フォーム入力値検証
def validate_search(P):
    if P == "":
        search_submit['state'] = "disabled" # submit無効
    else:
        search_submit['state'] = "normal" # submit有効
    return True

# ウィンドウ設定
win = tk.Tk()
win.title("ぐるぐるぐるナビ(笑)((激寒") # ウィンドウタイトル
win.resizable(False, False) # ウィンドウリサイズ無効化
val_search = win.register(validate_search) # 入力値検証 コールバック登録


exp_ini = cp.ConfigParser()
if os.path.exists("./exp.ini"):
    exp_ini.read("./exp.ini", encoding="utf-8")
else:
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "./exp.ini")


# 検索方式選定
search_method_frame = ttk.Frame(win, padding=8)
# 検索方式ラベルフレーム
search_method_labelf = ttk.Labelframe(search_method_frame, text="検索方式", style='My.TLabelframe')
# 検索方式ラジオボタン
rbv = tk.StringVar(None, "0") # デフォルト -> フリーワード検索
search_method_rb1 = ttk.Radiobutton(search_method_labelf, text="フリーワード検索", value="0", variable=rbv)
search_method_rb2 = ttk.Radiobutton(search_method_labelf, text="店名検索", value="1", variable=rbv)
search_method_rb3 = ttk.Radiobutton(search_method_labelf, text="住所検索", value="2", variable=rbv)


# 検索地域選定
place = config.PLACE
search_place_frame = ttk.Frame(win, padding=8)
# 検索地域ラベルフレーム
search_place_labelf = ttk.Labelframe(search_place_frame, text="検索地域", style='My.TLabelframe', padding=8)
# 検索地域ラベル(都道府県)
search_place_pref_label = ttk.Label(search_place_labelf, text="都道府県", padding=(5, 2))
# 検索地域コンボボックス(都道府県)
cbv_pref = tk.StringVar()
pref_list = list(place.keys()) # 都道府県リスト
search_place_pref_cb = ttk.Combobox(search_place_labelf, state="readonly", textvariable=cbv_pref, values=pref_list)
search_place_pref_cb.set(pref_list[7]) # デフォルト -> 東京都

# 都道府県に応じてエリアL反映
search_place_pref_cb.bind(
    '<<ComboboxSelected>>', 
    lambda e: search_place_areaL_cb.config(values=list(place[cbv_pref.get()]['areaL'].keys()))
)
# 検索地域ラベル(エリアL)
search_place_areaL_label = ttk.Label(search_place_labelf, text="エリアL", padding=(5, 2))
# 検索地域コンボボックス(エリアL)
cbv_areaL = tk.StringVar()
search_place_areaL_cb = ttk.Combobox(search_place_labelf, state="readonly", textvariable=cbv_areaL, values=list(place[cbv_pref.get()]['areaL'].keys()))

def expanded_search():
    
    def expanded_submit():
        exp_ini.set('category', 'categoryL', str(categoryL_list.index(cbv_cateL.get())))
        exp_ini.set('category', 'categoryS', str(list(category[cbv_cateL.get()]['categoryS'].keys()).index(cbv_cateS.get())))

        exp_ini.set('terms', 'ckv_lunch', str(ckv_lunch.get()))
        exp_ini.set('terms', 'ckv_breakfast', str(ckv_breakfast.get()))
        exp_ini.set('terms', 'ckv_takeout', str(ckv_takeout.get()))
        exp_ini.set('terms', 'ckv_delivery', str(ckv_delivery.get()))
        exp_ini.set('terms', 'ckv_nosmoking', str(ckv_nosmoking.get()))
        exp_ini.set('terms', 'ckv_privateroom', str(ckv_privateroom.get()))
        exp_ini.set('terms', 'ckv_midnight', str(ckv_midnight.get()))
        exp_ini.set('terms', 'ckv_untilmorning', str(ckv_untilmorning.get()))
        exp_ini.set('terms', 'ckv_bottomlesscup', str(ckv_bottomlesscup.get()))
        exp_ini.set('terms', 'ckv_outret', str(ckv_outret.get()))
        exp_ini.set('terms', 'ckv_card', str(ckv_card.get()))
        exp_ini.set('terms', 'ckv_emoney', str(ckv_emoney.get()))
        exp_ini.set('terms', 'ckv_parking', str(ckv_parking.get()))
        exp_ini.set('terms', 'ckv_webreserve', str(ckv_webreserve.get()))

        with open("./exp.ini", 'w') as f:
            exp_ini.write(f)

        exp_win.destroy()

    # 高度な検索ウィンドウ
    exp_win = tk.Toplevel(win)
    exp_win.grab_set() # 親ウィンドウ操作無効化
    exp_win.title("高度な検索") # ウィンドウタイトル
    exp_win.resizable(False, False) # ウィンドウリサイズ無効化

    # カテゴリ指定
    cate_ini = exp_ini['category']
    category = config.category
    categoryL_list = list(category.keys())
    category_frame = ttk.Frame(exp_win, padding=8)
    category_labelf = ttk.LabelFrame(category_frame, text="カテゴリ", padding=8)

    # 大カテゴリラベル
    categoryL_label = ttk.Label(category_labelf, text="大カテゴリ", padding=(5, 2))
    # 大カテゴリコンボボックス
    cbv_cateL = tk.StringVar()
    categoryL_cb = ttk.Combobox(category_labelf, state="readonly", textvariable=cbv_cateL, values=categoryL_list)
    categoryL_cb.set(categoryL_list[int(cate_ini.get('categoryL'))]) 



    # 大カテゴリに応じて小カテゴリ反映

    def changecateL():
        categoryS_cb.config(values=list(category[cbv_cateL.get()]['categoryS'].keys()))
        categoryS_cb.set(list(category[cbv_cateL.get()]['categoryS'].keys())[0])

    categoryL_cb.bind(
        '<<ComboboxSelected>>', 
        lambda e: changecateL()
    )

    # 小カテゴリラベル
    categoryS_label = ttk.Label(category_labelf, text="小カテゴリ", padding=(5, 2))
    # 小カテゴリコンボボックス
    cbv_cateS = tk.StringVar()
    categoryS_cb = ttk.Combobox(category_labelf, state="readonly", textvariable=cbv_cateS, values=list(category[cbv_cateL.get()]['categoryS'].keys()))
    categoryS_cb.set(list(category[cbv_cateL.get()]['categoryS'].keys())[int(cate_ini.get('categoryS'))]) 

    # 条件指定
    terms_ini = exp_ini['terms']
    terms_frame = ttk.Frame(exp_win, padding=8)
    terms_labelf = ttk.LabelFrame(terms_frame, text="条件指定", padding=8)
    
    # 条件指定チェックボックス
    # ランチ営業有
    ckv_lunch = tk.BooleanVar()
    ckv_lunch.set(terms_ini.get('ckv_lunch'))
    terms_lunch = ttk.Checkbutton(terms_labelf, text="ランチ営業有", variable=ckv_lunch)
    # 朝食有
    ckv_breakfast = tk.BooleanVar()
    ckv_breakfast.set(terms_ini.get('ckv_breakfast'))
    terms_breakfast = ttk.Checkbutton(terms_labelf, text="朝食有", variable=ckv_breakfast)
    # テイクアウト可
    ckv_takeout = tk.BooleanVar()
    ckv_takeout.set(terms_ini.get('ckv_takeout'))
    terms_takeout = ttk.Checkbutton(terms_labelf, text="テイクアウト可", variable=ckv_takeout)
    # デリバリー可
    ckv_delivery = tk.BooleanVar()
    ckv_delivery.set(terms_ini.get('ckv_delivery'))
    terms_delivery = ttk.Checkbutton(terms_labelf, text="デリバリー可", variable=ckv_delivery)
    # 禁煙席有
    ckv_nosmoking = tk.BooleanVar()
    ckv_nosmoking.set(terms_ini.get('ckv_nosmoking'))
    terms_nosmoking = ttk.Checkbutton(terms_labelf, text="禁煙席有", variable=ckv_nosmoking)
    # 個室有
    ckv_privateroom = tk.BooleanVar()
    ckv_privateroom.set(terms_ini.get('ckv_privateroom'))
    terms_privateroom = ttk.Checkbutton(terms_labelf, text="個室有", variable=ckv_privateroom)
    # 深夜営業
    ckv_midnight = tk.BooleanVar()
    ckv_midnight.set(terms_ini.get('ckv_midnight'))
    terms_midnight = ttk.Checkbutton(terms_labelf, text="深夜営業", variable=ckv_midnight)
    # 翌朝営業
    ckv_untilmorning = tk.BooleanVar()
    ckv_untilmorning.set(terms_ini.get('ckv_untilmorning'))
    terms_untilmorning = ttk.Checkbutton(terms_labelf, text="翌朝営業", variable=ckv_untilmorning)
    # 飲み放題有
    ckv_bottomlesscup = tk.BooleanVar()
    ckv_bottomlesscup.set(terms_ini.get('ckv_bottomlesscup'))
    terms_bottomlesscup = ttk.Checkbutton(terms_labelf, text="飲み放題有", variable=ckv_bottomlesscup)
    # 電源有
    ckv_outret = tk.BooleanVar()
    ckv_outret.set(terms_ini.get('ckv_outret'))
    terms_outret = ttk.Checkbutton(terms_labelf, text="電源有", variable=ckv_outret)
    # カード決済可
    ckv_card = tk.BooleanVar()
    ckv_card.set(terms_ini.get('ckv_card'))
    terms_card = ttk.Checkbutton(terms_labelf, text="カード決済可", variable=ckv_card)
    # 電子マネー決済可
    ckv_emoney = tk.BooleanVar()
    ckv_emoney.set(terms_ini.get('ckv_emoney'))
    terms_emoney = ttk.Checkbutton(terms_labelf, text="電子マネー決済可", variable=ckv_emoney)
    # 駐車場有
    ckv_parking = tk.BooleanVar()
    ckv_parking.set(terms_ini.get('ckv_parking'))
    terms_parking = ttk.Checkbutton(terms_labelf, text="駐車場有", variable=ckv_parking)
    # Web予約可
    ckv_webreserve = tk.BooleanVar()
    ckv_webreserve.set(terms_ini.get('ckv_webreserve'))
    terms_webreserve = ttk.Checkbutton(terms_labelf, text="Web予約可", variable=ckv_webreserve)

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
    terms_frame.grid(row=0, column=1, sticky=tk.W+tk.E)
    terms_labelf.grid(row=0, column=0, sticky=tk.W+tk.E)
    terms_lunch.grid(row=0, column=0, sticky=tk.W+tk.E)
    terms_breakfast.grid(row=0, column=1, sticky=tk.W+tk.E)
    terms_takeout.grid(row=0, column=2, sticky=tk.W+tk.E)
    terms_delivery.grid(row=0, column=3, sticky=tk.W+tk.E)
    terms_nosmoking.grid(row=1, column=0, sticky=tk.W+tk.E)
    terms_privateroom.grid(row=1, column=1, sticky=tk.W+tk.E)
    terms_midnight.grid(row=1, column=2, sticky=tk.W+tk.E)
    terms_untilmorning.grid(row=1, column=3, sticky=tk.W+tk.E)
    terms_bottomlesscup.grid(row=2, column=0, sticky=tk.W+tk.E)
    terms_outret.grid(row=2, column=1, sticky=tk.W+tk.E)
    terms_card.grid(row=2, column=2, sticky=tk.W+tk.E)
    terms_emoney.grid(row=2, column=3, sticky=tk.W+tk.E)
    terms_parking.grid(row=3, column=0, sticky=tk.W+tk.E)
    terms_webreserve.grid(row=3, column=1, sticky=tk.W+tk.E)

    # 適用ボタン配置
    exp_submit_frame.grid(row=1, column=2)
    exp_submit.grid(row=0, column=0)

    exp_win.mainloop()

# 高度検索フレーム
expanded_search_frame = ttk.Frame(win, padding=8)
expanded_search_button = ttk.Button(
    expanded_search_frame,
    text="高度な検索",
    command=expanded_search
)

# 検索フレーム
search_frame = ttk.Frame(win, padding=8)
# 検索フォームラベル
search_label = ttk.Label(search_frame, text="検索ワード", padding=(5, 2))
# 検索フォーム
search_word = tk.StringVar() # 検索キーワード
search_form = ttk.Entry(search_frame, width=80, textvariable=search_word, validatecommand=(val_search, '%P'), validate='all')
# 検索ボタン
search_submit = ttk.Button(
    search_frame,
    state="disabled",
    text="検索",
    command=lambda: print("{},{}".format(search_word.get(), rbv.get()))
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
# 高度検索ボタン配置
expanded_search_frame.grid(row=0, column=2)
expanded_search_button.grid(row=0, column=0)
api_img = tk.PhotoImage(file="./api_265_65.png")
canvas = tk.Canvas(bg="black", width=264, height=64)
canvas.place(x=490, y=70)
canvas.create_image(0, 0, image=api_img, anchor=tk.NW)

def on_closing():
    exp_ini.set('category', 'categoryL', "0")
    exp_ini.set('category', 'categoryS', "0")

    exp_ini.set('terms', 'ckv_lunch', "False")
    exp_ini.set('terms', 'ckv_breakfast', "False")
    exp_ini.set('terms', 'ckv_takeout', "False")
    exp_ini.set('terms', 'ckv_delivery', "False")
    exp_ini.set('terms', 'ckv_nosmoking', "False")
    exp_ini.set('terms', 'ckv_privateroom', "False")
    exp_ini.set('terms', 'ckv_midnight', "False")
    exp_ini.set('terms', 'ckv_untilmorning', "False")
    exp_ini.set('terms', 'ckv_bottomlesscup', "False")
    exp_ini.set('terms', 'ckv_outret', "False")
    exp_ini.set('terms', 'ckv_card', "False")
    exp_ini.set('terms', 'ckv_emoney', "False")
    exp_ini.set('terms', 'ckv_parking', "False")
    exp_ini.set('terms', 'ckv_webreserve', "False")

    os.remove("./exp.ini")
    with open("./exp.ini", 'w') as f:
        exp_ini.write(f)

    win.destroy()


win.protocol("WM_DELETE_WINDOW", on_closing)
# 表示
win.mainloop()
