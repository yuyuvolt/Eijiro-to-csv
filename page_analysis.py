import requests, bs4
import re

def analyze_words(word_list:list):
    nonexistent_words = []
    word_information_full = []
    for word in word_list:
        flag, word_, pron, meaning, sentence = analyze_word(word)
        if flag != True:
            nonexistent_words.append(word)
        else:
            word_information = [word_, pron, meaning, sentence]
            word_information_full.append(word_information)
    return nonexistent_words, word_information_full

def analyze_word(word:str):
    response = requests.get(url(word))
    flag, word_, pron, meaning, sentence = html_analysis(response)
    return flag, word_, pron, meaning, sentence

#単語を与えられて，url返す関数
def url(word:str):
    url_string = ""
    parts = word.split()
    for i in range(len(parts)):
        if i != 0:
            url_string += '+'
        url_string += parts[i]
    url_ = "https://eow.alc.co.jp/search?q=" + url_string
    return url_

#htmlを与えられて，単語の情報を返す関数
def html_analysis(response):
    flag = True
    if "に該当する項目は見つかりませんでした。" in response.text:
        flag = False
        return flag, None, None, None, None
    whole_html = bs4.BeautifulSoup(response.text, 'html.parser')
    word, pron, meaning = use_analysis(whole_html.select_one('div[class="search-use-list"]'))
    sentence = sentences_analysis(whole_html.select_one('div[class="search-sentence-list"]'))
    extract_sentence_from_meaning(meaning, sentence)
    meaning = meaning_molding(meaning)
    sentence_molding(sentence)
    return flag, word, pron, meaning, sentence

def extract_sentence_from_meaning(meaning, sentences):
    extracted = []
    for i in range(len(meaning)):
        res = re.findall(r'(<br/>.*?(?=</li>))', meaning[i], re.MULTILINE)
        for e_ in res:
            meaning[i] = meaning[i].replace(e_, '')
            extracted.extend([i for i in e_.split('<br/>')if i != ''])
    for i in range(len(extracted)):
        extracted[i] = extracted[i][1:]
    sentences.extend(extracted)

def meaning_molding(meaning):#meaning
    for i in range(len(meaning)):
        word_class = re.match(r'^.*?</span>', meaning[i], re.MULTILINE).group()
        meaning[i] = meaning[i].replace(word_class, '')
        word_class = word_class[24:-7]
        meaning[i] = meaning[i].replace('<li>','<li>' + word_class)
    meaning_ = ""
    for element in meaning:
        meaning_ += element
    meaning_ = meaning_.replace('<ol>', '')
    meaning_ = meaning_.replace('</ol>', '')
    meaning__ = [i for i in re.split(r'<li>|</li>', meaning_) if i != '']
    return meaning__

def sentence_molding(sentences):#sentence
    for i in range(len(sentences)):
        rim_list = ['\n', r'<li class="result-item">', r'<span class="midashi">', r'<span class="redtext">', r'<h2>', r'</h2>', r'</span>', r'</li>', r'</div>']
        if sentences[i][0] == '<':
            for item in rim_list:
                sentences[i] = sentences[i].replace(item, '')
            sentences[i] = sentences[i].replace('<div>',' : ')

def use_analysis(use):
    #minimalな情報だけが含まれたブロックを抽出
    use = bs4.BeautifulSoup(use.__str__(), 'html.parser')
    use = use.select_one('li[class="result-item"]')
    use = bs4.BeautifulSoup(use.__str__(), 'html.parser')

    #word, pronunciationの抽出
    word = use.select_one('span[class="redtext"]').__str__()
    word = word[22:-7]
    pron = use.select_one('span[class="pron"]').__str__()
    if pron != "None":
        pron = pron[19:-7]
    else:
        pron = ""
    
    #meaningの抽出
    use = use.__str__()
    pattern = r'(<span class="wordclass">.*?</ol>)'
    res = re.findall(pattern, use, re.MULTILINE)
    for i in range(len(res)):
        rem = re.findall(r'(<span class="kana">(.|\s)*?</span>)', res[i], re.MULTILINE)
        for each in rem:
            res[i] = res[i].replace(each[0], '')
    meaning = res

    return word, pron, meaning

def sentences_analysis(sentences):
    sentences = sentences.__str__()
    pattern = r'(<li class="result-item">(.|\s)*?</li>)'
    res = re.findall(pattern, sentences, re.MULTILINE)
    for i in range(len(res)):
        res[i] = res[i][0]
    for i in range(len(res)):
        res[i] = re.sub(r'<span class="kana">(.|\s)*?</span>', '', res[i], re.MULTILINE)
        res[i] = re.sub(r'<span class="tango">(.|\s)*?</span>', '', res[i], re.MULTILINE)
    return res