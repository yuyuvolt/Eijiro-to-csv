import os
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.scrolledtext as scrolltext
import error_popup
import sentence_choice_overall

in_file = None
out_file = None
word_list = None

root = None
frame_whole = None
frame_type_words = None
frame_show_words = None
typed_words = False

def check():
    print("ok")

def file_choice():
    global root
    root = tk.Tk()
    root.title("ファイル選択")
    root.geometry("530x300")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    set_frame_whole()
    set_frame_type_words()

    frame_whole_raise()
    root.mainloop()

def set_frame_whole():
    global frame_whole

    #全体のフレーム
    frame_whole = tk.Frame(root, padx=16, pady=16)
    frame_whole.grid(row=0, column=0, sticky="nsew")

    #4つのブロック
    frame_header = tk.Frame(frame_whole)
    frame_input = tk.LabelFrame(frame_whole, text="単語の入力元", padx=8, pady=8)
    frame_output = tk.LabelFrame(frame_whole, text="単語の出力先", padx=8, pady=8)
    frame_footer = tk.Frame(frame_whole)

    frame_header.pack(fill=tk.X)
    frame_input.pack(fill=tk.X)
    frame_output.pack(fill=tk.X)
    frame_footer.pack(fill=tk.X)

    #headerブロック
    label_abstract = tk.Label(frame_header, text="単語の入力元や出力先を選択します．")

    label_abstract.pack(side=tk.LEFT)

    #inputブロック
    frame_input_header = tk.Frame(frame_input)
    frame_input_radiobuttons = tk.Frame(frame_input)
    frame_input_yes = tk.Frame(frame_input_radiobuttons)
    frame_input_no = tk.Frame(frame_input_radiobuttons)
    frame_input_yes_browse = tk.Frame(frame_input_yes)

    #inputブロック ラジオボタンセクションの詳細
    choice_value = tk.StringVar()
    label_input_abstract = tk.Label(frame_input_header, text="情報をCSVに出力したい単語のリストが書かれたテキスト形式のファイルはありますか？")
    rb_yes = tk.Radiobutton(frame_input_yes, text="Yes", value="Yes", variable=choice_value)
    button_input_browse = tk.Button(frame_input_yes_browse, text="Browse", command=lambda : input_file_choice())
    label_input_browse = tk.Label(frame_input_yes_browse, text="選んだファイル:")
    rb_no = tk.Radiobutton(frame_input_no, text="No (次のウィンドウで単語を入力します．)", value="No", variable=choice_value)

    #inputブロック browseボタンの挙動
    def input_file_choice():
        global in_file
        typ = [('プレーンテキスト', "*.txt")]
        in_file = filedialog.askopenfilename(filetypes=typ)
        label_input_browse.config(text="選んだファイル:" + os.path.basename(in_file))

    #inputブロック レイアウト
    frame_input_header.pack(fill=tk.X)
    frame_input_radiobuttons.pack(fill=tk.X)
    frame_input_yes.pack(fill=tk.X)
    frame_input_no.pack(fill=tk.X)
    frame_input_yes_browse.pack(side=tk.BOTTOM,fill=tk.X)
    label_input_abstract.pack(side=tk.LEFT)
    rb_yes.pack(side=tk.LEFT)
    button_input_browse.pack(side=tk.LEFT)
    label_input_browse.pack(side=tk.LEFT)
    rb_no.pack(side=tk.LEFT)

    #outputブロック
    frame_upper_output = tk.Frame(frame_output)
    frame_lower_output = tk.Frame(frame_output)
    label_upper_output = tk.Label(frame_upper_output, text="単語の情報を出力するCSVファイルを選択してください．")
    button_output_browse = tk.Button(frame_lower_output, text="Browse", command=lambda : output_file_choice())
    label_lower_output = tk.Label(frame_lower_output, text="選んだファイル:")

    #outpuブロック browseボタンの挙動
    def output_file_choice():
        global out_file
        typ = [('CSVファイル', '*.csv')]
        out_file = filedialog.askopenfilename(filetypes=typ)
        label_lower_output.config(text="選んだファイル:" + os.path.basename(out_file))

    #outputブロック レイアウト
    frame_upper_output.pack(fill=tk.X)
    frame_lower_output.pack(fill=tk.X)
    label_upper_output.pack(side=tk.LEFT)
    button_output_browse.pack(side=tk.LEFT)
    label_lower_output.pack(side=tk.LEFT)

    #footerブロック
    button_next = tk.Button(frame_footer, text="Next", command=lambda : second_window(choice_value.get()))
    button_next.pack(side=tk.RIGHT)

def set_frame_type_words():
    global frame_type_words

    frame_type_words = tk.Frame(root, padx=16, pady=16)
    frame_type_words.grid(row=0, column=0, sticky="nsew")

    #header
    frame_header = tk.Frame(frame_type_words)
    frame_header.pack(side=tk.TOP, fill=tk.X)
    label_abstruct = tk.Label(frame_header, text="情報をCSVに出力したい単語を以下の空欄に入力してください．\n1つの単語/熟語ごとに改行してください．", justify=tk.LEFT)
    label_abstruct.pack(side=tk.LEFT, anchor="nw", fill=tk.X)

    #footer
    frame_footer = tk.Frame(frame_type_words)
    frame_footer.pack(side=tk.BOTTOM, fill=tk.X)
    button_previous = tk.Button(frame_footer, text="Previous", command=lambda : frame_whole_raise())
    button_next = tk.Button(frame_footer, text="Next", command=lambda : from_type_words(entry.get("1.0", "end-1c")))
    button_previous.pack(side=tk.LEFT)
    button_next.pack(side=tk.RIGHT)

    #entry
    frame_body = tk.Frame(frame_type_words)
    frame_body.pack(expand=True)
    entry = scrolltext.ScrolledText(frame_body)
    entry.pack(fill=tk.BOTH)

def set_frame_show_words():
    global frame_show_words, word_list
    frame_show_words = tk.Frame(root, padx=16, pady=16)
    frame_show_words.grid(row=0, column=0, sticky="nsew")

    #header
    frame_header = tk.Frame(frame_show_words)
    frame_header.pack(side=tk.TOP, fill=tk.X)
    label_abstruct = tk.Label(frame_header, text="以下が単語/熟語のリストです．", justify=tk.LEFT)
    label_abstruct.pack(side=tk.LEFT, anchor="nw", fill=tk.X)

    #footer
    frame_footer = tk.Frame(frame_show_words)
    frame_footer.pack(side=tk.BOTTOM, fill=tk.X)
    def previous():
        if typed_words:
            frame_type_words_raise()
        else:
            frame_whole_raise()
    button_previous = tk.Button(frame_footer, text="Previous", command=lambda : previous())
    button_next = tk.Button(frame_footer, text="Next", command=lambda : sentence_choice_overall.sentence_choice_overall(out_file))
    button_previous.pack(side=tk.LEFT)
    button_next.pack(side=tk.RIGHT)

    #showcase
    frame_body = tk.Frame(frame_show_words)
    frame_body.pack(expand=True)
    showcase = scrolltext.ScrolledText(frame_body)
    word_list_string = ""
    for word in word_list:
        word_list_string += (word + "\n")
    showcase.insert(tk.END, word_list_string)
    showcase.config(state=tk.DISABLED)
    showcase.pack(fill=tk.BOTH)

def frame_whole_raise():
    frame_whole.tkraise()

def frame_type_words_raise():
    frame_type_words.tkraise()

def frame_show_words_raise():
    frame_show_words.tkraise()

def second_window(choice_value):
    if out_file == None:
        error_popup.error_popup("出力先を選択してください．")
    else:
        if choice_value == "Yes":
            if in_file == None:
                error_popup.error_popup("入力元を選択してください")
            else:
                global word_list, typed_words
                in_file_ = open(in_file, 'r')
                word_list = in_file_.read().splitlines()
                typed_words = False
                set_frame_show_words()
                frame_show_words_raise()
        elif choice_value == "No":
            frame_type_words_raise()
        else:
            error_popup.error_popup("単語の入力スタイルを選択してください．")

def from_type_words(string:str):
    global word_list, typed_words
    word_list = string.splitlines()
    typed_words = True
    set_frame_show_words()
    frame_show_words_raise()