import streamlit as st
import json
import datetime
from PIL import Image
import requests
from io import BytesIO
import jieba
import os
import matplotlib.pyplot as plt
from imageio import imread
from collections import Counter
from wordcloud import WordCloud, ImageColorGenerator

d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
msg_file = d + 'message.js'
stinky_piggy_id = 'huaji1415'
silly_piggy_id = 'wxid_2379733797521'
user_dict = ['爱猪', '猪猪', '傻猪', '想猪', '傻猪', '傻猪猪', '臭猪', '笨猪', '小臭猪', '小仙女']
for w in user_dict:
    jieba.add_word(w)

stopword_file = d + '/stopwords-zh.txt'
stopwords = []
with open(stopword_file) as f:
    stopword_text = f.read()
    stopwords = stopword_text.split('\n')
    del stopword_text

font_path = d + '/fonts/NotoSansSC-Light.otf'

with open('message.js') as f:
    msg_text = f.read()
cleaned_text = msg_text[11:] # remove variable declaration
msg_json = json.loads(cleaned_text)
messages = msg_json['message']
del msg_text
del cleaned_text
del msg_json

def get_text(role):
    text_chat = []
    if role == 'stinky_piggy':
        from_id = stinky_piggy_id
    else:
        from_id = silly_piggy_id
    for m in messages:
        if m['m_uiMessageType'] == 1:
            if m['m_nsFromUsr'] == from_id:
                text_chat.append(m['m_nsContent'])
    return text_chat

def count_word(texts, stopwords=stopwords):
    words = []
    for text in texts:
        tokens = jieba.lcut(text)
        for token in tokens:
            token = token
            if token not in stopwords and token != '\n':
                words.append(token)
    return Counter(words)

def generate_word_cloud_text(word_count, number=100):
    cloud_words = []
    for w in word_count.most_common(number):
        cloud_words.append(w[0])
    return ' '.join(cloud_words)

def build_cloud(words, image_file='pig-head.jpg'):
    back_coloring = imread(os.path.join(d, image_file))
    wc = WordCloud(font_path=font_path, background_color="white", max_words=2000, mask=back_coloring,
            max_font_size=100, random_state=42, width=1000, height=860, margin=2,)
    wc.generate(cloud_words)
    # image_colors_default = ImageColorGenerator(image_file)
    return wc


st.title('傻猪猪和臭猪猪的聊天记录')
role_cn = st.radio("你想看谁的聊天记录呢？",
    ('傻猪猪', '臭猪猪'))
if role_cn == '傻猪猪':
    role = 'silly_piggy'
else:
    role = 'stinky_piggy'
number = st.slider('请选择显示词数', 100, 250, 100, 25)
image_file = st.selectbox('请选择一只猪猪的图片',
    ('pig-head.jpg', 'piglet.jpg'))
image = Image.open(image_file)
st.image(image, caption='使用这张图作为基准', width=200)
# uploaded_file = st.file_uploader("选择一张jpg图片", type="jpg")
confirm = st.button('让我来看看')

if confirm:
    text_chat = get_text(role)
    word_count = count_word(text_chat, stopwords)
    cloud_words = generate_word_cloud_text(word_count, number)
    wc = build_cloud(cloud_words, image_file)

    plt.figure()
    # recolor wordcloud and show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    st.pyplot()