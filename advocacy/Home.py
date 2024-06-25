import streamlit as st
import time
import os
import json
import pymongo

from utils import reset_values, generate_embeddings, vector_search, print_chunk_search_result,rag_with_vector_search
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

#set up Azure stuff
CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")
db_client = pymongo.MongoClient(CONNECTION_STRING)
# Create database to hold cosmic works data
# MongoDB will create the database if it does not exist
db = db_client.cms_open
st.session_state["db"] = db

EMBEDDINGS_DEPLOYMENT_NAME = "text-embedding-3-small"
st.session_state["EMBEDDINGS_DEPLOYMENT_NAME"] = EMBEDDINGS_DEPLOYMENT_NAME
COMPLETIONS_DEPLOYMENT_NAME = "gpt-4"
st.session_state["COMPLETIONS_DEPLOYMENT_NAME"] = COMPLETIONS_DEPLOYMENT_NAME
AOAI_ENDPOINT = os.environ.get("AOAI_ENDPOINT")
AOAI_KEY = os.environ.get("AOAI_KEY")
AOAI_API_VERSION = "2024-02-01"

st.set_page_config(
    page_title="Advocacy",
    page_icon="🩺",
)


st.logo("CGLogoDNAsmall.png")

#these are currently mockups - should pull the real stuff
ai_url = "https://openai.com"
#could read these form Gov API
current_document = "CMS-2024-0131-0001"
current_document_url = "https://downloads.regulations.gov/CMS-2024-0131-0001/content.pdf"
comment_start = "April 10, 2024"
comment_end = "May 3, 2024"
#could extract this from the document somehow? Not in API
document_title = "Medicare and Medicaid Programs and the Children’s Health Insurance Program; Hospital Inpatient Prospective Payment Systems for Acute Care Hospitals and the Long-Term Care Hospital Prospective Payment System and Policy Changes and Fiscal Year 2025 Rates; Quality Programs Requirements; and Other Policy Changes"

#set these in state
st.session_state["current_document"] = current_document
st.session_state["current_document_url"] = current_document_url

#display current materials
st.sidebar.write("Current Document:", current_document)
st.sidebar.link_button("Download Document", current_document_url)

if 'ai_client' not in st.session_state:
    #azure client
    ai_client = AzureOpenAI(
    azure_endpoint = AOAI_ENDPOINT,
    api_version = AOAI_API_VERSION,
    api_key = AOAI_KEY
    )
    st.session_state["ai_client"] = ai_client
else:
    ai_client = st.session_state["ai_client"]

#check if thread is already in state or empty (been reset)    
if 'thread' not in st.session_state or st.session_state["thread"] == "":
    #create a thread for this session
    # in azure, a thread is just an array of messages
    thread = []
    st.session_state["thread"] = thread
else:
    thread = st.session_state["thread"]

st.session_state["system_message"] = "You are the Advocacy Assistant. You have extensive knowledge of healthcare policy."

#get summary intro message if it's not already here or if its empty (been reset)
if 'intro_message' not in st.session_state or st.session_state["intro_message"] == "":
    #start with a simple message to get basic info and assure connection
    #put initial info message on thread. The system message and RAG results will be put before this
    question = """Write a short haiku about healthcare policy. Make sure to include line breaks to maintain the haiku structure."""

    completion = rag_with_vector_search(question)
    
    # #filter for assistant messages
    # assistant_messages = [message for message in messages.data if message.role == "assistant"]
    # # save intro message
    st.session_state["intro_message"] = completion

# put an image in top of the page, centered
with st.columns(3)[1]:
    st.image("CGLogoDNA.png", width=200)
    st.markdown(f":gray[*{st.session_state['intro_message']}*]")

st.divider()
st.title("Advocacy Home")

st.write("Welcome to the Advocacy Assistant! Let's get started.")
st.write("Current Document:", current_document)
st.write("Title:", document_title)
st.write("Comment period:", comment_start, "to", comment_end)
st.divider()
st.write("I can scan the document and help you find the information that is most relevant to you. Please provide some information about yourself and your interests.")


#for debugging and monitoring
#st.sidebar.write(f"Message annotations: {st.session_state.intro_message.content[0].text.annotations}")

if "user_interest" not in st.session_state:
    st.session_state["user_interest"] = ""
if "user_role" not in st.session_state:
    st.session_state["user_role"] = ""

user_role = st.selectbox(
   "Select your role:",
   ("Advocate", "Community Member", "Researcher", "Practitioner", "Other (specify below)")
)

user_interest = st.text_area("Describe your interests, expertise, or subject area:", st.session_state["user_interest"], height=150, placeholder="Enter your work, interests, experience or research here")

go_ai = st.button("Go")
if go_ai:
    st.session_state["user_interest"] = user_interest
    st.session_state["user_role"] = user_role
    # erase the next variable so they can be reloaded
    st.session_state["dis_message"] = ""
    st.switch_page("pages/2_Choose.py")

#a reset button that erases state for user_interest, user_role, intro_message, and last_message_id
reset = st.button("Reset")
if reset:
    reset_values()