import streamlit as st

st.set_page_config(
    page_title="Submit",
    page_icon="🩺",
)

st.markdown("# Submit")
st.sidebar.header("Submit")
st.logo("TextBotLogoSmall.jpeg")

st.sidebar.write("Current Document: ", st.session_state["current_document"])
st.sidebar.link_button("View Document", st.session_state["current_document_url"])

st.divider()

st.write("Done!")
#st.image("BalloonsSmall.jpeg")
st.balloons()

next = st.button("Done")

if next:
    st.switch_page("Home.py")