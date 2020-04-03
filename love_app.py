import streamlit as st
import json
import datetime
from PIL import Image
import requests
from io import BytesIO

msg_file='message.js'
stinky_piggy_id = 'huaji1415'
silly_piggy_id = 'wxid_2379733797521'

with open(msg_file) as f:
    text = f.read()
cleaned_text = text[11:] # remove variable declaration
msg_json = json.loads(cleaned_text)
# stinky_piggy_avatar_url = msg_json['member'][stinky_piggy_id]['head']
# silly_piggy_avatar_url = msg_json['member'][silly_piggy_id]['head']

stinky_piggy_avatar = Image.open('stinky_piggy.jpeg')
silly_piggy_avatar = Image.open('silly_piggy.jpeg')
messages = msg_json['message']

def search(token, messages):
    h_count, x_count = 0, 0
    h_first, x_first = None, None
    h_msg, x_msg = None, None
    for m in messages:
        if token in m['m_nsContent'] and m['m_uiMessageType'] == 1:
            if m['m_nsToUsr'] == 'huaji1415':
                x_count += 1
                if x_first is None:
                    timestamp = m['m_uiCreateTime']
                    x_first = datetime.datetime.fromtimestamp(timestamp)
                    x_msg = m['m_nsContent']
            else:
                h_count += 1
                if h_first is None:
                    timestamp = m['m_uiCreateTime']
                    h_first = datetime.datetime.fromtimestamp(timestamp)
                    h_msg = m['m_nsContent']
    return (h_count, x_count, h_first, x_first, h_msg, x_msg)


st.title('傻猪猪和臭猪猪的恋爱笔记')
search_term = st.text_input('请输入要查找的词语', '猪猪')
counts = search(search_term, messages)
st.image(stinky_piggy_avatar, width=66)
st.write(f"臭猪说了　{counts[0]}　次　{search_term}")
st.write(f"第一次是在{counts[2]}   说的是　{counts[4]}")
st.image(silly_piggy_avatar, width=66)
st.write(f"傻猪说了　{counts[1]}　次　{search_term}")
st.write(f"第一次是在{counts[3]}   说的是　{counts[5]}")