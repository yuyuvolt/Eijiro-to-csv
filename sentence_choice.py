import file_choice, error_popup, write_csv
import tkinter as tk
import re

root = None
out_file = None
previous_root = None
frame_sentence_choice = None
frame_sentence_choice_last = None
word_information_full = None
meaning_bool = []
sentences_bool = []
ith_word = 0

def sentence_choice(word_information_full_, out_file_):
    global word_information_full, out_file
    out_file = out_file_
    word_information_full = word_information_full_

    initialize()

def choice():
    frame_sentence_choice.config(padx = 0, pady = 0)

    frame_footer = tk.Frame(frame_sentence_choice, padx= 8, pady= 8)

    def next():
        if ith_word == len(word_information_full) - 1:
            raise_frame_sentence_choice_last()
        else:
            move_to_ith_word(ith_word + 1, frame_meaning, frame_sentences)
    def previous():
        if ith_word == 0:
            error_popup.error_popup("最初の単語です．戻れません．")
        else:
            move_to_ith_word(ith_word - 1, frame_meaning, frame_sentences)
    button_next = tk.Button(frame_footer, text="Next", command=next)
    button_previous = tk.Button(frame_footer, text="Previous", command=previous)
    frame_footer.pack(side=tk.BOTTOM, fill=tk.X)
    button_next.pack(side=tk.RIGHT)
    button_previous.pack(side=tk.LEFT)

    frame_meaning = tk.Frame(frame_sentence_choice, width=400)
    frame_meaning.pack(side=tk.LEFT, fill=tk.Y)
    frame_sentences = tk.Frame(frame_sentence_choice, width=400)
    frame_sentences.pack(side=tk.LEFT, fill=tk.Y)

    move_to_ith_word(0, frame_meaning, frame_sentences)

def move_to_ith_word(i:int, frame_meaning:tk.Frame, frame_sentences:tk.Frame):
    meaning = word_information_full[i][2]
    sentences = word_information_full[i][3]
    destroy_children(frame_meaning)
    destroy_children(frame_sentences)
    set_frame_meaning(i, meaning, frame_meaning)
    set_frame_sentences(i, sentences, frame_sentences)

def set_frame_sentences(i, sentences, frame_sentences:tk.Frame):
    global ith_word
    ith_word = i
    frame_sentences.update_idletasks()
    w = frame_sentences.winfo_width()
    h = frame_sentences.winfo_height()
    canvas = tk.Canvas(frame_sentences, width=w, height=h)
    frame = tk.Frame(canvas)

    sentences_bool.append([])
    for j in range(len(sentences)):
        subframe = tk.Frame(frame)
        subframe.pack(side=tk.TOP, fill=tk.X)
        sentences_bool[i].append(tk.BooleanVar(value=False))
        cb = tk.Checkbutton(subframe, variable = sentences_bool[i][j])
        cb.pack(side=tk.LEFT)
        label = tk.Label(subframe, text=rem_html_tags(sentences[j]), justify=tk.LEFT, wraplength=350)
        label.pack(anchor='w')
    
    # スクロールバーの配置
    vbar = tk.Scrollbar(frame_sentences, orient=tk.VERTICAL)
    vbar.config(command=canvas.yview)
    vbar.pack(side=tk.RIGHT,fill=tk.Y)

    canvas.create_window(0, 0, window=frame)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=vbar.set)

    canvas.xview_moveto(0)
    canvas.yview_moveto(0)

def set_frame_meaning(i, meaning, frame_meaning:tk.Frame):
    global ith_word
    ith_word = i
    frame_meaning.update_idletasks()
    w = frame_meaning.winfo_width()
    h = frame_meaning.winfo_height()
    canvas = tk.Canvas(frame_meaning, width=w, height=h)
    frame = tk.Frame(canvas)

    meaning_bool.append([])
    for j in range(len(meaning)):
        subframe = tk.Frame(frame)
        subframe.pack(side=tk.TOP, fill=tk.X)
        meaning_bool[i].append(tk.BooleanVar(value=False))
        cb = tk.Checkbutton(subframe, variable = meaning_bool[i][j])
        cb.pack(side=tk.LEFT)
        label = tk.Label(subframe, text=rem_html_tags(meaning[j]), justify=tk.LEFT, wraplength=350)
        label.pack(anchor='w')
    
    # スクロールバーの配置
    vbar = tk.Scrollbar(frame_meaning, orient=tk.VERTICAL)
    vbar.config(command=canvas.yview)
    vbar.pack(side=tk.RIGHT,fill=tk.Y)

    canvas.create_window(0, 0, window=frame)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=vbar.set)

    canvas.xview_moveto(0)
    canvas.yview_moveto(0)

def initialize():
    global root, previous_root, frame_sentence_choice

    previous_root = file_choice.root

    root = tk.Toplevel()
    root.geometry("800x1000")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    frame_sentence_choice= tk.Frame(root, padx=16, pady=16)
    frame_sentence_choice.grid(row=0, column=0, sticky="nsew")
    label = tk.Label(frame_sentence_choice, text="単語帳に乗せる意味と例文を選びましょう．")
    button = tk.Button(frame_sentence_choice, text="Proceed", command=lambda : [label.destroy(), button.destroy(), choice()])
    label.pack()
    button.pack()

    set_frame_sentence_choice_last()
    raise_frame_sentence_choice()

def set_frame_sentence_choice_last():
    global frame_sentence_choice_last
    frame_sentence_choice_last= tk.Frame(root, padx=16, pady=16)
    frame_sentence_choice_last.grid(row=0, column=0, sticky="nsew")
    label = tk.Label(frame_sentence_choice_last, text="例文選択を終了します")
    frame_footer = tk.Frame(frame_sentence_choice_last)
    previous = tk.Button(frame_footer, text="Prevoius", command=raise_frame_sentence_choice)
    finish = tk.Button(frame_footer, text="Finish", command=finish_up)
    label.pack()
    frame_footer.pack()
    finish.pack(side=tk.RIGHT)
    previous.pack(side=tk.LEFT)

def raise_frame_sentence_choice():
    frame_sentence_choice.tkraise()

def raise_frame_sentence_choice_last():
    frame_sentence_choice_last.tkraise()

def destroy_children(widget:tk.Widget):
    children = widget.winfo_children()
    for child in children:
        child.destroy()

def rem_html_tags(s:str):
    ret = re.sub(r'<.*?>', '', s, re.MULTILINE)
    return ret

def finish_up():
    write_csv.write_csv(word_information_full, meaning_bool, sentences_bool, out_file)
    root.destroy()