from typing import Optional

import streamlit as st
from httpx_oauth.clients.google import GoogleOAuth2
from httpx_oauth.oauth2 import OAuth2Token

def markdown_button(
    url: str, text: Optional[str] = None, color="#FD504D", sidebar: bool = True
):
    markdown = st.sidebar.markdown if sidebar else st.markdown

    markdown(
        f"""
    <a href="{url}" target="_self">
        <div style="
            display: inline-flex;
            -webkit-box-align: center;
            align-items: center;
            -webkit-box-pack: center;
            justify-content: center;
            font-weight: 400;
            padding: 0.25rem 0.75rem;
            border-radius: 0.25rem;
            margin: 0px;
            line-height: 1.6;
            width: auto;
            user-select: none;
            background-color: {color};
            color: rgb(255, 255, 255);
            border: 1px solid rgb(255, 75, 75);
            text-decoration: none;
            ">
            {text}
        </div>
    </a>
    """,
        unsafe_allow_html=True,
    )

def show_login_button(
    text: Optional[str] = "Login with Google", color="#FD504D", sidebar: bool = True
):
    button = st.sidebar.button if sidebar else st.button
    if button(text, type="primary"):
        st.login()


def get_logged_in_user_email() -> Optional[str]:
    return st.experimental_user.get("email", None)
