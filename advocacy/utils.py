import streamlit as st

# @st.cache_data   #TODO this should have caching
def run_thread(thread_id, assistant_id, client):
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        # instructions="Can add instructions here that override the Assistant's default instructions."
    )
    return run

def reset_values():
    st.session_state["user_interest"] = ""
    st.session_state["user_role"] = ""
    st.session_state["intro_message"] = ""
    st.session_state["dis_message"] = ""
    st.session_state["guidance_message"] = ""
    st.session_state["comment"] = ""
    st.session_state["last_message_id"] = ""
    st.session_state["thread"] = ""
    st.switch_page("Home.py")