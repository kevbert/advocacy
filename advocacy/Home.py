import streamlit as st
from openai import OpenAI
import threading
import time
import os

from utils import run_thread, reset_values

st.set_page_config(
    page_title="Advocacy",
    page_icon="🩺",
)

st.title("Advocacy Home")

# add logo file "TextBotLogoSmall.jpeg" to sidebar
st.logo("TextBotLogoSmall.jpeg")

#these are currently mockups
ai_url = "https://openai.com"
current_document = "CMS Long Document Long"
current_document_url = "https://cms.gov"

#set these in state
st.session_state["current_document"] = current_document
st.session_state["current_document_url"] = current_document_url

#display current materials
st.sidebar.write("Current Document: ", current_document)
st.sidebar.link_button("View Document", current_document_url)

if 'api_key' not in st.session_state:
    # get OPENAI_API_KEY from .env file
    from dotenv import load_dotenv
    load_dotenv()
    #set up OpenAI API stuff
    # Access the API key from the environment
    api_key = os.getenv("ADVOCACY_OPENAI_API_KEY")
    st.session_state["api_key"] = api_key
    #st.write("new api key: ", api_key)
else:
    api_key = st.session_state["api_key"]
    #st.write("loaded api key: ", api_key)

if 'client' not in st.session_state:
    #set up OpenAI API stuff
    # Access the API key from the environment
    api_key = os.getenv("ADVOCACY_OPENAI_API_KEY")
    # connect to LLM Assistant API
    client = OpenAI(api_key=api_key)
    st.session_state["client"] = client
    #st.write("new client: ", client.api_key)
else:
    client = st.session_state["client"]
    #st.write("loaded client: ", client.api_key)

if 'assistant' not in st.session_state:
    #fetch assistant
    assistant = client.beta.assistants.retrieve("asst_NKfcLtfzuj3uCPa1cDlNNlTy")   #gpt 4, temperature .1, Long original document
    # assistant = client.beta.assistants.retrieve("asst_qM2xHQ1uBPocEnkpw3Jq4qhS")   #gpt 4, temperature .1, SNF document
    st.session_state["assistant"] = assistant
else:
    assistant = st.session_state["assistant"]

#check if thread is already in state or empty (been reset)    
if 'thread' not in st.session_state or st.session_state["thread"] == "":
    #create a thread for this session
    thread = client.beta.threads.create()
    st.session_state["thread"] = thread
else:
    thread = st.session_state["thread"]

#get summary intro message if it's not already here or if its empty (been reset)
if 'intro_message' not in st.session_state or st.session_state["intro_message"] == "":
    #start with a simple message to get basic info and assure connection
    #initial info message on thread
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="""What is the agency, title, and due date for comments on this call? 
    Example response: 
    '''Agency: CMS
    Title: CY 2023 Physician Fee Schedule
    Comments: comments due September 30, 2022.'''
   """

    #TODO: get title and due date from API rather than the LLM
    )
    # run thread on assistant
    run = run_thread(thread.id, assistant.id, client)

    # Poll for task completion
    while run.status != "completed":
        #show status in sidebar
        st.sidebar.info(f"Task status: {run.status}")
        time.sleep(1)  # Adjust polling interval as needed
        #TODO: should check timeout and errors

    st.sidebar.success("Assistant Connected")

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    #filter for assistant messages
    assistant_messages = [message for message in messages.data if message.role == "assistant"]
    # save intro message
    st.session_state["intro_message"] = assistant_messages[0]
    #save last message id in session state
    last_message_id = assistant_messages[0].id
    st.session_state["last_message_id"] = last_message_id

st.write(st.session_state["intro_message"].content[0].text.value)

#for debugging and monitoring
st.sidebar.write(f"Message annotations: {st.session_state.intro_message.content[0].text.annotations}")

if "user_interest" not in st.session_state:
    st.session_state["user_interest"] = ""
if "user_role" not in st.session_state:
    st.session_state["user_role"] = ""

user_role = st.selectbox(
   "Select your role:",
   ("Advocate", "Community Member", "Researcher", "Practitioner")
)

user_interest = st.text_area("Describe your interests, expertise, or subject area:", st.session_state["user_interest"], height=300, placeholder="Enter your work, interests, experience or research here")

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