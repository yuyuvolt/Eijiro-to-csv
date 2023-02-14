import file_choice as fc
import tkinter as tk
import tkinter.scrolledtext as scrolltext
import sentence_choice
import page_analysis

root = None
word_list = None
out_file = None

frame_nonexistent_words = None
frame_last_screen = None

def sentence_choice_overall(out_file):
    initialize()
    nonexitent_words, word_information_full= page_analysis.analyze_words(word_list)
    set_frame_last_screen()
    if not nonexitent_words.__eq__([]):
        set_frame_nonexistent_words(nonexitent_words)
        frame_nonexistent_words_raise()
        sentence_choice.sentence_choice(word_information_full, out_file)
        frame_last_screen_raise()
    else:
        sentence_choice.sentence_choice(word_information_full, out_file)
        frame_last_screen_raise()
    
def initialize():
    global root, word_list, out_file
    word_list = fc.word_list
    out_file = fc.out_file
    root = fc.root

def set_frame_nonexistent_words(word_list:list):
    global frame_nonexistent_words
    frame_nonexistent_words = tk.Frame(root, padx=16, pady=16)
    frame_nonexistent_words.grid(row=0, column=0, sticky="nsew")

    #header
    frame_header = tk.Frame(frame_nonexistent_words)
    frame_header.pack(side=tk.TOP, fill=tk.X)
    label_abstruct = tk.Label(frame_header, text="以下が英辞郎上に存在しなかった単語/熟語のリストです．確認してください\n確認された場合はダイアログの序盤の画面に戻って修正するか，これらの単語を無視して次の画面へ進んでください．", justify=tk.LEFT, wraplength=498)
    label_abstruct.pack(side=tk.LEFT, anchor="nw", fill=tk.X)

    #footer
    frame_footer = tk.Frame(frame_nonexistent_words)
    frame_footer.pack(side=tk.BOTTOM, fill=tk.X)
    button_previous = tk.Button(frame_footer, text="Previous", command=lambda : fc.frame_show_words_raise())
    button_next = tk.Button(frame_footer, text="Next", command=lambda : frame_last_screen_raise())
    button_previous.pack(side=tk.LEFT)
    button_next.pack(side=tk.RIGHT)

    #showcase
    frame_body = tk.Frame(frame_nonexistent_words)
    frame_body.pack(expand=True)
    showcase = scrolltext.ScrolledText(frame_body)
    word_list_string = ""
    for word in word_list:
        word_list_string += (word + "\n")
    showcase.insert(tk.END, word_list_string)
    showcase.pack(fill=tk.BOTH)

def set_frame_last_screen():
    global frame_last_screen
    frame_last_screen = tk.Frame(root)

    frame_last_screen = tk.Frame(root, padx=16, pady=16)
    frame_last_screen.grid(row=0, column=0, sticky="nsew")

    label1 = tk.Label(frame_last_screen, text="以下のファイルに単語の情報を出力しました．")
    label2 = tk.Label(frame_last_screen, text=out_file)
    button = tk.Button(frame_last_screen, text="Finish", command=lambda : root.destroy())

    label1.pack(side=tk.TOP, anchor=tk.W)
    label2.pack(side=tk.TOP, anchor= tk.W)
    button.pack(side=tk.BOTTOM)

def frame_nonexistent_words_raise():
    frame_nonexistent_words.tkraise()

def frame_last_screen_raise():
    frame_last_screen.tkraise()

def write_csv(word_information_full):
    output = open(out_file, 'w')
    for info in word_information_full:
        s = ""
        for each_info in info:
            s += str(each_info) + "\t"
        s += "\n"
        output.write(s)