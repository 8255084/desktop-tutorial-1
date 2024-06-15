# 使用方法：
# 1.安装依赖包：streamlit, sqlite3, re, hashlib。
# 2.创建data.db数据库文件，路径默认为主py文件所在文件夹，可自定义修改为其他路径。
# 3.在需要设置登录页面的文件中导入SimpleLogin类，并调用login()方法进行登录页面的设置。
# 4.将设置登录页面的主要代码放入main_page()方法中，通过login方法成功验证后，可以调用main_page()中的代码。

import streamlit as st
import sqlite3
import re
import hashlib


class SimpleLogin:
    def __init__(self):
        self.conn = sqlite3.connect('data.db')
        self.c = self.conn.cursor()
        if 'username' not in st.session_state:
            st.session_state['username'] = ''
        if 'password' not in st.session_state:
            st.session_state['password'] = ''
        if 'is_login' not in st.session_state:
            st.session_state['is_login'] = False

    def create_usertable(self):
        self.c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

    def add_userdata(self, username, password):
        self.c.execute('SELECT username FROM userstable WHERE username =?', (username,))
        if self.c.fetchone():
            return False
        else:
            self.c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
            self.conn.commit()
            return True

    def login_user(self, username, password):
        self.c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
        data = self.c.fetchall()
        return data

    def view_all_users(self):
        self.c.execute('SELECT * FROM userstable')
        data = self.c.fetchall()
        return data

    def sign_up(self):
        """Simple sign up"""

        st.title("注册新用户")

        st.subheader("创建新账号")
        new_user = st.text_input("用户名", key='new_user')
        new_password = st.text_input("密码", type='password', key='new_password')

        if st.button("注册"):
            if is_email(new_user):
                self.create_usertable()
                is_signed = self.add_userdata(new_user, make_hashes(new_password))
                if is_signed:
                    st.success("你成功创建了一个新账号")
                    st.info("请返回登录页面登录")
                else:
                    st.warning("用户名已存在，请换个注册名！")
            else:
                st.error("请输入有效的电子邮件地址作为用户名")

    def show_login_page(self):
        if not st.session_state.is_login:
            st.title("登录")
            username = st.text_input("用户名")
            password = st.text_input("密码", type='password')
            if st.button("登录"):
                hashed_pswd = make_hashes(password)
                result = self.login_user(username, check_hashes(password, hashed_pswd))
                if result:
                    st.success("当前用户：{}".format(username))
                    st.session_state.username = username
                    st.session_state.is_login = True
                    return True
                else:
                    st.error("登录失败，请检查用户名和密码是否正确！")
                    return False
            # 如果用户没有点击登录按钮，函数将在这里结束并返回False
        return False

    def LoggedOut_Clicked(self):
        st.session_state.is_login = False

    def show_logout_page(self):
        if 'username' in st.session_state.keys():
            st.sidebar.markdown(f'<p style="color:green;">当前用户：{st.session_state["username"]}</p>',
                                unsafe_allow_html=True)
            st.sidebar.button("退出登录", key="logout", on_click=self.LoggedOut_Clicked)


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


def is_email(address):
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_pattern, address):
        return True
    else:
        return False
