import re

#将获得到的Keywords文件进行分行，便于后续readlines
with open('keywords.txt', 'r',encoding='utf-8') as f:
    content = f.read()
# 将所有的')'后面的','替换为'\n'
content = content.replace('),', ')\n')

# 将修改后的内容写回文件
with open('keywords.txt', 'w',encoding='utf-8') as f:
    f.write(content)

# 这里得到了停止词的一个列表
with open('stopwords.txt', 'r') as file:
    stopwords = file.readlines()
stopwords = [line.strip() for line in stopwords]


# 创建一个新的文件来存储你想要的行
with open('keywords.txt', 'r',encoding='utf-8') as file2:
    txt=file2.readlines()
txt = [line.strip()for line in txt]

print(stopwords)
print(txt)
pattern = re.compile(r"'(.*?)'")

# 使用列表推导式来创建一个新的B列表，只包含那些单引号内的内容不在A列表中的元素
txt = [item for item in txt if pattern.search(item).group(1) not in stopwords]

print(txt)  # 输出更新后的B列表
with open("result.txt","w",encoding='utf-8')as file3:
    file3.write(str(txt))