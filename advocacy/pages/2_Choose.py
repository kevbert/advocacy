import streamlit as st
import time
import os
import json
import pymongo

from utils import reset_values, generate_embeddings, vector_search, print_chunk_search_result,rag_with_vector_search
from openai import AzureOpenAI

st.set_page_config(
    page_title="Choose",
    page_icon="🩺",
)

st.markdown("# Choose")
st.sidebar.header("Choose")
st.logo("TextBotLogoSmall.jpeg")

st.divider()
#display current materials
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

# get new dis_message if it isn't already in session state or blank
if 'dis_message' not in st.session_state or st.session_state["dis_message"] == "":
    #get AI response for user role and interest
    ai_prompt = f"I am a {st.session_state['user_role']}. My interests are: {st.session_state['user_interest']}."
    specific_instructions = """
Extract and summarize relevant parts of the document. Identify topics that match the user's role and interests. For each relevant topic, provide a title and a brief summary (less than 5 words). 
Example: Diabetes Management: strategies for managing diabetes.
Then, ask the user to select their topic of interest.
"""

    completion = rag_with_vector_search(ai_prompt+specific_instructions)

    # save disambuguation message
    st.session_state["dis_message"] = completion

st.write(st.session_state["dis_message"])

if "user_choice" not in st.session_state:
    st.session_state["user_choice"] = ""

user_choice = st.text_area("What area would you like to dig into?", st.session_state["user_choice"], height=100, placeholder="Nunmerical value of the area you are interested in or name an area")

next = st.button("Choose")

if previous:
    st.switch_page("Home.py")

if next:
    st.session_state["user_choice"] = user_choice
    st.session_state["guidance"] = ""
    st.switch_page("pages/3_Summary.py")