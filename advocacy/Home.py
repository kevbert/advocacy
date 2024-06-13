import streamlit as st
from openai import OpenAI
import threading
import time

@st.cache_data   #TODO check if this caching is working
def run_thread(thread_id, assistant_id, _client):
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Answer user questions based on the reference materials."
    )
    return run

st.set_page_config(
    page_title="Advocacy",
    page_icon="🩺",
)

st.title("Advocacy Home")

# add logo file "TextBotLogoSmall.jpeg" to sidebar
st.logo("TextBotLogoSmall.jpeg")

# get OPENAI_API_KEY from .env file
import os
from dotenv import load_dotenv
load_dotenv()

#set up OpenAI API stuff
# Access the API key from the environment
api_key = os.getenv("ADVOCACY_OPENAI_API_KEY")
# connect to LLM Assistant API
client = OpenAI(api_key=api_key)
st.session_state["client"] = client
#fetch assistant
assistant = client.beta.assistants.retrieve("asst_NKfcLtfzuj3uCPa1cDlNNlTy")
st.session_state["assistant"] = assistant
#create a thread for this session
thread = client.beta.threads.create()
st.session_state["thread"] = thread

#start with a simple message to get basic info and assure connection
#initial info message on thread
message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="What is the agency, title, and due date for comments on this call? Example response: '''CMS, CY 2023 Physician Fee Schedule, comments due September 30, 2022.'''" 
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
#print content all messages in main window
for message in assistant_messages:
    # st.write(f"{message.role} ({message.id}): {message.content[0].text.value}")
    st.write(f"{message.content[0].text.value}")

ai_url = "https://openai.com"
current_document = "CMS Document Long <NONE>"
current_document_url = "https://cms.gov"
#set these in state
st.session_state["current_document"] = current_document
st.session_state["current_document_url"] = current_document_url

#display current materials
st.sidebar.write("Current Document: ", current_document)
st.sidebar.link_button("View Document", current_document_url)

if "user_interest" not in st.session_state:
    st.session_state["user_interest"] = ""
if "user_role" not in st.session_state:
    st.session_state["user_role"] = ""

user_role = st.selectbox(
   "Select your role:",
   ("Advocate", "Community Member", "Researcher", "Practitioner")
)

user_interest = st.text_area("Describe your interests, expertise, or subject area:", st.session_state["user_interest"], height=300)

go_ai = st.button("Go")
if go_ai:
    st.session_state["user_interest"] = user_interest
    st.session_state["user_role"] = user_role
    st.switch_page("pages/2_AI_Summary.py")