import streamlit as st

st.set_page_config(
    page_title="Comment",
    page_icon="🩺",
)

st.markdown("# Comment")
st.sidebar.header("Comment")
st.logo("TextBotLogoSmall.jpeg")

st.divider()

def clear_text():
    st.session_state["user_comment"] = ""
    st.session_state["comment_box"] = ""

st.write("Current Document: ", st.session_state["current_document"])
st.link_button("View Document", st.session_state["current_document_url"])

st.divider()

st.write("User role:", st.session_state["user_role"])


st.divider()

st.write("AI Summary goes here.")

if "user_comment" not in st.session_state:
    st.session_state["user_comment"] = ""

clear = st.button("Clear", on_click=clear_text)
user_comment = st.text_area("Write your comment here:", st.session_state["user_comment"], height=300, key="comment_box")

previous = st.button("Cancel")
next = st.button("Review Comment")

if previous:
    st.session_state["user_comment"] = user_comment
    st.switch_page("pages/2_AI_Summary.py")

if next:
    st.session_state["user_comment"] = user_comment
    st.switch_page("pages/4_Review.py")