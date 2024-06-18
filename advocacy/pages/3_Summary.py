import streamlit as st
import openai
import threading
import time

from utils import run_thread

st.set_page_config(
    page_title="Summary",
    page_icon="🩺",
)

st.markdown("# Summary")
st.sidebar.header("Summary")
st.logo("TextBotLogoSmall.jpeg")

st.divider()

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

# sample JSON containing agency, due date, and title
# {
#     "agency": "CMS",
#     "due_date": "2022-12-01",
#     "title": "Proposed Rule on Medicare Payment Policies"
# }


# get new guidance if it isn't already in session state or blank
if 'guidance' not in st.session_state or st.session_state["guidance"] == "":
    #get AI response for user choice
    ai_prompt = f"{st.session_state["user_choice"]}."
    specific_instructions = """ find the topic that the user indicated, and prepare a summary of the information on that topic from the document. Include these sections: 
Proposed Changes: Summarize the proposed changes in this area.
Comment Source: Identify where the comment originated (e.g., public submissions, surveys, direct feedback).
Specific Issues Addressed: Highlight the main issues mentioned in each comment.
Evidence and Data: Look for comments supported by data, personal experiences, or expert opinions.
Suggested Alternatives: Note any alternative solutions or recommendations provided in the comments.
Impact Statements: Identify how the proposed rule or policy changes would impact the commenters and their communities.
Write everything at an 8th grade literacy level. Don't tell the user that you have made the language simpler.
"""

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
    st.session_state["guidance"] = message.content[0].text.value
    last_message_id = message.id
    st.session_state["last_message_id"] = last_message_id
    


st.write(st.session_state["guidance"])

previous = st.button("Cancel")
next = st.button("Make Comment")

if previous:
    st.switch_page("pages/2_Choose.py")

if next:
    st.switch_page("pages/4_Comment.py")