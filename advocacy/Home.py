import streamlit as st

st.set_page_config(
    page_title="Advocacy",
    page_icon="🩺",
)

st.title("Advocacy Home")

# add logo file "TextBotLogoSmall.jpeg" to sidebar
st.logo("TextBotLogoSmall.jpeg")

st.sidebar.success("Welcome")

ai_url = "https://openai.com"
current_document = "CMS Document Long <NONE>"
current_document_url = "https://cms.gov"
#set these in state
st.session_state["current_document"] = current_document
st.session_state["current_document_url"] = current_document_url

#display current materials
st.write("Current Document: ", current_document)
st.link_button("View Document", current_document_url)

if "user_interest" not in st.session_state:
    st.session_state["user_interest"] = ""
if "user_role" not in st.session_state:
    st.session_state["user_role"] = ""

user_role = st.selectbox(
   "Select your role:",
   ("Advocate", "Community Member", "Researcher", "Practitioner")
)

user_interest = st.text_area("Describe your interests, expertise, or subject area:", st.session_state["user_interest"], height=300)

go_ai = st.button("Go")
if go_ai:
    st.session_state["user_interest"] = user_interest
    st.session_state["user_role"] = user_role
    st.switch_page("pages/2_AI_Summary.py")