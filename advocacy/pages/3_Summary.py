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
    ai_prompt = f"{st.session_state['user_choice']}."
    specific_instructions = """
Find the selected topic and prepare a summary including:
- **Proposed Changes:** Summarize the changes.
- **Comment Source:** Origin of the comment (e.g., public submissions, surveys).
- **Specific Issues Addressed:** Main issues mentioned.
- **Evidence and Data:** Data or expert opinions supporting the comment.
- **Suggested Alternatives:** Alternative solutions or recommendations.
- **Impact Statements:** How the changes would impact the commenters and their communities. Impacts on commenters should include time and effort required to comply with the changes.

For each section, include a direct quote from the material. When including quotes from the document, ensure they are directly extracted. Do not paraphrase or generate quotes. If a direct quote cannot be found, clearly state that no direct quote is available.

Write everything at an 8th grade literacy level.
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