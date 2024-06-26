import streamlit as st
import time
import os
import json
import pymongo

from utils import reset_values, generate_embeddings, vector_search, print_chunk_search_result,rag_with_vector_search
from openai import AzureOpenAI

def clear_text():
    st.session_state["user_comment"] = ""

st.set_page_config(
    page_title="Comment",
    page_icon="🩺",
)

st.markdown("# Comment")
st.sidebar.header("Comment")
st.logo("CGLogoDNAsmall.png")

st.divider()

st.sidebar.write("Current Document: ", st.session_state["current_document"])
st.sidebar.link_button("View Document", st.session_state["current_document_url"])

st.divider()

# recover AI variables from state
ai_client = st.session_state["ai_client"]
thread = st.session_state["thread"]

st.write("User interest:", st.session_state["user_interest"])
st.write("User role:", st.session_state["user_role"])
st.write("User choice:", st.session_state["user_choice"])
previous = st.button("Change")

st.divider()

st.write(f"{st.session_state.guidance}")

st.divider()
st.markdown(""":blue-background[Guidelines for making a comment  
Read and understand the regulatory document you are commenting on  
Feel free to reach out to the agency with questions  
Be concise but support your claims  
Base your justification on sound reasoning, scientific evidence, and/or how you will be impacted  
Address trade-offs and opposing views in your comment  
There is no minimum or maximum length for an effective comment  
The comment process is not a vote – one well supported comment is often more influential than a thousand form letters  
Be respectful and professional]""")

if "user_comment" not in st.session_state:
    st.session_state["user_comment"] = ""

clear = st.button("Clear", on_click=clear_text)
user_comment = st.text_area("Write your comment here:", st.session_state["user_comment"], height=200, key="comment_box")

previous = st.button("Cancel")
next = st.button("Review Comment")

if previous:
    st.session_state["user_comment"] = user_comment
    st.switch_page("pages/3_Summary.py")

if next:
    st.session_state["user_comment"] = user_comment
    st.switch_page("pages/5_Review.py")

# # for debugging and monitoring
# st.divider()
# st.write(st.session_state["thread"])