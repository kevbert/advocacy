import streamlit as st
import time
import os
import json
import pymongo

from utils import reset_values, generate_embeddings, vector_search, print_chunk_search_result,rag_with_vector_search
from openai import AzureOpenAI

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
previous = st.button("Change")

st.divider()

# get new guidance if it isn't already in session state or blank
if 'review' not in st.session_state or st.session_state["review"] == "":
    #get AI response for user choice
    specific_instructions = f""" Review the user's comment. Provide feedback on the user's comment. Here are some guidelines for providing feedback:
    Read and understand the regulatory document you are commenting on
Feel free to reach out to the agency with questions
Be concise but support your claims
Base your justification on sound reasoning, scientific evidence, and/or how you will be impacted
Address trade-offs and opposing views in your comment
There is no minimum or maximum length for an effective comment
The comment process is not a vote – one well supported comment is often more influential than a thousand form letters
Be respectful and professional
    User's comment: {st.session_state["user_comment"]}
    Your feedback:
    """

    completion = rag_with_vector_search(specific_instructions)

    # save review message
    st.session_state["review"] = completion

st.write(st.session_state["review"])

#textbox for revising comment
st.text_area("Revise Comment", st.session_state["user_comment"], height=300)

previous = st.button("Cancel")
next = st.button("Submit Comment")

if previous:
    st.switch_page("pages/4_Comment.py")

if next:
    st.switch_page("pages/6_Submit.py")