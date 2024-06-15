import streamlit as st
import openai
import threading
import time

from utils import run_thread, reset_values

st.set_page_config(
    page_title="Summary",
    page_icon="🩺",
)

st.markdown("# AI Summary")
st.sidebar.header("AI Summary")
st.logo("TextBotLogoSmall.jpeg")

st.divider()
#display current materials
st.sidebar.write("Current Document: ", st.session_state["current_document"])
st.sidebar.link_button("View Document", st.session_state["current_document_url"])

st.divider()

# recover AI variables from state
client = st.session_state["client"]
thread = st.session_state["thread"]
assistant = st.session_state["assistant"]

st.write("User interest:", st.session_state["user_interest"])
st.write("User role:", st.session_state["user_role"])
previous = st.button("Change")

st.divider()


# get new dis_message if it isn't already in session state or blank
if 'dis_message' not in st.session_state or st.session_state["dis_message"] == "":
    #get AI response for user role and interest
    ai_prompt = f"I am a {st.session_state["user_role"]}. My interests are: {st.session_state["user_interest"]}."
    specific_instructions = """ Extract and summarize relevant parts of the documents.
                Review the document. There are many different topics covered in the document. Decide if each topic is relevant to the user. If it is relevant, write it out a title and a brief summary of less than 5 words. Here is an example: Diabetes Management: strategies for managing diabetes
                Then ask the user which of the topics they are interested in"""

    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=ai_prompt+specific_instructions 
    )
    # run thread on assistant
    run = run_thread(thread.id, assistant.id, client)
    # Poll for task completion
    while run.status != "completed":
        #show status in sidebar
        st.sidebar.info(f"Task status: {run.status}")
        time.sleep(1)  # Adjust polling interval as needed
        #TODO: should check timeout and errors

    #messages.list normally returns ALL the messages, so we need to do some filtering or limiting
    # the one we want should be the most recent one with role assistant
    # could filter it, but can also just pop off the first one, as that is the most recent
    #messages = client.beta.threads.messages.list(thread_id=thread.id, before=f"{st.session_state['last_message_id']}")
    messages = client.beta.threads.messages.list(thread_id=thread.id)


    #filter for assistant messages
    assistant_messages = [message for message in messages.data if message.role == "assistant"]
    # the first message is the most recent one
    message = assistant_messages[0]
    #st.write(f"{message.role} ({message.id}): {message.content[0].text.value}")
    # save disambuguation message
    st.session_state["dis_message"] = message.content[0].text.value
    last_message_id = message.id
    st.session_state["last_message_id"] = last_message_id


st.write(st.session_state["dis_message"])

next = st.button("Make Comment")

if previous:
    st.switch_page("Home.py")

if next:
    st.switch_page("pages/3_Comment.py")