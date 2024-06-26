import streamlit as st
from utils import submit_comment

st.set_page_config(
    page_title="Submit",
    page_icon="🩺",
)

st.markdown("# Submit")
st.sidebar.header("Submit")
st.logo("CGLogoDNAsmall.png")

st.sidebar.write("Current Document: ", st.session_state["current_document"])
st.sidebar.link_button("View Document", st.session_state["current_document_url"])

st.divider()

st.markdown("*Submitting comment...*")
regulations_response = submit_comment(st.session_state["user_comment"])
st.markdown("**Regulations.gov:** " + regulations_response)
st.write("Done!")
st.write("Thank you for submitting your comment. You are now done. You can close this tab.")
#st.image("BalloonsSmall.jpeg")
st.balloons()

next = st.button("Done")

if next:
    st.switch_page("Home.py")