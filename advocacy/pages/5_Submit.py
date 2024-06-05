import streamlit as st

st.set_page_config(
    page_title="Submit",
    page_icon="🩺",
)

st.markdown("# Submit")
st.sidebar.header("Submit")
st.logo("TextBotLogoSmall.jpeg")

st.divider()

st.write("Done!")
#st.image("BalloonsSmall.jpeg")
st.balloons()

next = st.button("Done")

if next:
    st.switch_page("Home.py")