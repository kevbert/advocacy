import streamlit as st

st.set_page_config(
    page_title="Summary",
    page_icon="🩺",
)

st.markdown("# AI Summary")
st.sidebar.header("AI Summary")
st.logo("TextBotLogoSmall.jpeg")

st.divider()
#display current materials
st.write("Current Document: ", st.session_state["current_document"])
st.link_button("View Document", st.session_state["current_document_url"])

st.divider()

st.write("User interest:", st.session_state["user_interest"])
st.write("User role:", st.session_state["user_role"])
previous = st.button("Change")

st.divider()

st.write("AI Summary goes here.")

next = st.button("Make Comment")

if previous:
    st.switch_page("Home.py")

if next:
    st.switch_page("pages/3_Comment.py")