import error_popup

out_str = ""
out_file = None

def write_csv(word_information_full, meaning_bool, sentences_bool, out_file_):
    global out_file, out_str
    out_file = out_file_
    for i in range(len(word_information_full)):
        out_str += word_information_full[i][0] + "\t"
        out_str += word_information_full[i][1] + "\t"
        out_str += meaning_str(i, word_information_full, meaning_bool) + "\t"
        out_str += sentence_str(i, word_information_full, sentences_bool)
        out_str += "\n"
    try:
        f = open(out_file, 'w')
        f.write(out_str)
    except:
        error_popup.error_popup("何らかのエラーが生じました．")

def meaning_str(i, word_information_full, meaning_bool):
    ret = "<ol>"
    for j in range(len(meaning_bool[i])):
        if meaning_bool[i][j].get():
            cur = "<li>"
            cur += word_information_full[i][2][j]
            cur += "</li>"
            ret += cur
    ret += "</ol>"
    return ret

def sentence_str(i, word_information_full, sentences_bool):
    ret = "<ul>"
    for j in range(len(sentences_bool[i])):
        if sentences_bool[i][j].get():
            cur = "<li>"
            cur += word_information_full[i][3][j]
            cur += "</li>"
            ret += cur
    ret += "</ul>"
    return ret
