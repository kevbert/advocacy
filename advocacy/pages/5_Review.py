import streamlit as st

st.set_page_config(
    page_title="Review",
    page_icon="🩺",
)

st.markdown("# Review")
st.sidebar.header("Review")
st.logo("TextBotLogoSmall.jpeg")

st.divider()

st.sidebar.write("Current Document: ", st.session_state["current_document"])
st.sidebar.link_button("View Document", st.session_state["current_document_url"])

st.divider()

st.write("User role:", st.session_state["user_role"])


st.divider()

st.write("Suggestions for revision go here.")

#textbox for revising comment
st.text_area("Revise Comment", st.session_state["user_comment"], height=300)

previous = st.button("Cancel")
next = st.button("Submit Comment")

if previous:
    st.switch_page("pages/4_Comment.py")

if next:
    st.switch_page("pages/6_Submit.py")