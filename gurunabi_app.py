import tkinter as tk
from tkinter import ttk

import gurunabi
import config

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
    # 高度な検索ウィンドウ
    exp_win = tk.Toplevel(win)
    exp_win.grab_set() # 親ウィンドウ操作無効化
    exp_win.title("高度な検索") # ウィンドウタイトル
    exp_win.resizable(False, False) # ウィンドウリサイズ無効化

    # カテゴリ指定
    category = config.category
    categoryL_list = list(category.keys())
    category_frame = ttk.Frame(exp_win, padding=8)
    category_labelf = ttk.LabelFrame(category_frame, text="カテゴリ", padding=8)

    # 大カテゴリラベル
    categoryL_label = ttk.Label(category_labelf, text="大カテゴリ", padding=(5, 2))
    # 大カテゴリコンボボックス
    cbv_cateL = tk.StringVar()
    categoryL_cb = ttk.Combobox(category_labelf, state="readonly", textvariable=cbv_cateL, values=categoryL_list)
    categoryL_cb.set(categoryL_list[0]) 

    # 大カテゴリに応じて小カテゴリ反映
    categoryL_cb.bind(
        '<<ComboboxSelected>>', 
        lambda e: categoryS_cb.config(values=list(category[cbv_cateL.get()]['categoryS'].keys()))
    )

    # 小カテゴリラベル
    categoryS_label = ttk.Label(category_labelf, text="小カテゴリ", padding=(5, 2))
    # 小カテゴリコンボボックス
    cbv_cateS = tk.StringVar()
    categoryS_cb = ttk.Combobox(category_labelf, state="readonly", textvariable=cbv_cateS, values=list(category[cbv_cateL.get()]['categoryS'].keys()))

    category_frame.grid(row=0, column=0)
    category_labelf.grid(row=0, column=0)
    categoryL_label.grid(row=0, column=0)
    categoryL_cb.grid(row=0, column=1)
    categoryS_label.grid(row=1, column=0)
    categoryS_cb.grid(row=1, column=1)

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

# 表示
win.mainloop()
