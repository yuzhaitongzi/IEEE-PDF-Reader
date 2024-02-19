# 本代码实现删除pdf的页眉和页脚
from PyPDF2 import PdfReader
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.chunk import RegexpParser


# 规定一个进行分句的函数
def cut_sentences(content):
    end_flag = ['?', '!', '.', '？', '！', '。', '…']
    punctuation = ['?', '!', '？', '！', '(', ')', '/','@', '0', '1', '2', '3', '4','5','6', '7', '8', '9']
    window_size = 10

    content_len = len(content)
    sentences = []
    tmp_char = ''

    for idx, char in enumerate(content):
        tmp_char += char

        if (idx + 1) == content_len:
            sentences.append(tmp_char)
            break

        if char in end_flag:
            next_idx = idx + 1

            if not content[next_idx] in end_flag and not any(
                    punc in content[next_idx - window_size:next_idx + window_size] for punc in punctuation):
                sentences.append(tmp_char)
                tmp_char = ''

    return sentences


# 规定分词块的语法
grammar = r"""
  NP: {<DT|PP\$>?<JJ>*<NN>}   # 匹配形容词+名词/动名词/过去分词   
      {<DT>+<VBG|VBN>}           #匹配形容词+动名词/过去分词
      {<DT>?<JJ>*<NN.*>}      #匹配冠词+形容词+名词  .*表示可以出现一个或者多个
      {<NNP|NNPS>+}                # 匹配连续的专有名词或者复数形式
      {<FW.*>}                  #匹配外来语，外来词，外文原词
      {<PRP>}                 # 匹配人称代词
"""


# 设置裁剪页眉页脚的高度函数
def visitor_body(text, cm, tm, fontDict, fontSize):
    y = tm[5]
    if y > 35 and y < 720:
        parts.append(text)


'''
论文处理部分
'''
# 创建阅读器
reader = PdfReader("getPDF.jsp--神经网络的参考源头.pdf") # 这里替换你需要的pdf
# 获取pdf页数
num_pages = reader.getNumPages()
# 创建一个空列表用于存入内容
parts = []
for i in range(0, num_pages):
    page = reader.pages[i]
    pages = str(reader.pages[i])
    parts.append(pages)
    page.extract_text(visitor_text=visitor_body)  # 写入时用删除页眉页脚函数
    text_body = "".join(parts)

# 创建一个body文件，来接收论文的主内容

txt_file = open("body.txt", mode='a', encoding='utf-8')
text = str(text_body)
# 使用正则表达式匹配"REFERENCES"
references = re.findall(r".*?(REFERENCES).*?", text, re.DOTALL)
# 找到了"REFERENCES"，则删除其后的所有内容
if references:
    text = text.split(references[0])[0]
# 删除分页后出现的标识文字
pattern = r"\[.*?\]"
result = re.sub(pattern, "", text)
new_text1 = re.sub(r'\{.*?\}|\{.*?\}', '', result)
new_text2 = re.sub(r'\'.*?\'|\'.*?\'', '', new_text1)
txt_file.write(str(new_text2))
'''
获得到了一个去除页眉页脚的body.txt文本
'''

'''
对文本进行分句，并且删除掉文章中不想要的内容
'''
with open('body.txt', 'r', encoding='utf-8') as f:
    body_text = f.read()
# 去掉换行符
body_text = body_text.replace('\n', '')

# 删除指定内容之间的部分
start_index = body_text.find('Manuscript')
end_index = body_text.find('Index')
if start_index != -1 and end_index != -1:
    body_text = body_text[:start_index] + body_text[end_index:]
sentences = cut_sentences(body_text)
txt = '\n\n'.join(sentences)
file = open('output.txt', 'a', encoding='utf-8')
new_text = re.sub(r'-\s*', '', txt)
file.write(new_text)
file.close()
'''
获得到了一个获取了指定内容，并且完成分句的output.txt文件
'''

'''
实现对output.txt文件进行词频分析
'''

# 根据词性进行分块
chunk_parser = RegexpParser(grammar)
cp = open("output.txt", 'r', encoding="utf-8").read()
cp = cp.lower()
for ch in '!"#\"\“\"_-$%&()*+\',-./:;<=>?@[\\]^_‘{|}~':
    cp = cp.replace(ch, ' ')  # 去掉特殊符号
tokens = word_tokenize(cp)
# 标记词性
tagged_tokens = nltk.pos_tag(tokens)
# 进行分块
tree = chunk_parser.parse(tagged_tokens)
# 提取名词短语
noun_phrases = []
for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
    noun_phrases.append(' '.join(word for word, tag in subtree.leaves()))
noun_phrases = nltk.FreqDist(noun_phrases)
txt = str(noun_phrases.most_common(1000))

# 将提取出来的词频写入到keyword文档中
file = open("keywords.txt", "w", encoding='utf-8')
file.writelines(txt)
file.close()