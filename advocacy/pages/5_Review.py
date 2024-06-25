import streamlit as st
import openai
import threading
import time

from utils import run_thread

st.set_page_config(
    page_title="Review",
    page_icon="🩺",
)

st.markdown("# Review")
st.sidebar.header("Review")
st.logo("CGLogoDNAsmall.png")

st.divider()

st.sidebar.write("Current Document: ", st.session_state["current_document"])
st.sidebar.link_button("View Document", st.session_state["current_document_url"])

# recover AI variables from state
client = st.session_state["client"]
thread = st.session_state["thread"]
assistant = st.session_state["assistant"]

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

    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=specific_instructions 
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
    st.session_state["review"] = message.content[0].text.value
    last_message_id = message.id
    st.session_state["last_message_id"] = last_message_id


st.write(st.session_state["review"])

#textbox for revising comment
st.text_area("Revise Comment", st.session_state["user_comment"], height=300)

previous = st.button("Cancel")
next = st.button("Submit Comment")

if previous:
    st.switch_page("pages/4_Comment.py")

if next:
    st.switch_page("pages/6_Submit.py")