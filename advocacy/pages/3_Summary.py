import streamlit as st
import time
import os
import json
import pymongo

from utils import reset_values, generate_embeddings, vector_search, print_chunk_search_result,rag_with_vector_search
from openai import AzureOpenAI

st.set_page_config(
    page_title="Summary",
    page_icon="🩺",
)

st.markdown("# Summary")
st.sidebar.header("Summary")
st.logo("CGLogoDNAsmall.png")

st.divider()

st.sidebar.write("Current Document: ", st.session_state["current_document"])
st.sidebar.link_button("View Document", st.session_state["current_document_url"])

st.divider()

# recover AI variables from state
ai_client = st.session_state["ai_client"]
thread = st.session_state["thread"]

st.write("User interest:", st.session_state["user_interest"])
st.write("User role:", st.session_state["user_role"])
st.write("User choice:", st.session_state["user_choice"])
previous = st.button("Change")

st.divider()


# get new guidance if it isn't already in session state or blank
if 'guidance' not in st.session_state or st.session_state["guidance"] == "":
    #get AI response for user choice
    ai_prompt = f"{st.session_state['user_choice']}."
    specific_instructions = """
Use the supplied materials and prepare a summary including:
- **Proposed Changes:** Summarize the changes.
- **Comment Source:** Origin of the comment (e.g., public submissions, surveys).
- **Specific Issues Addressed:** Main issues mentioned.
- **Evidence and Data:** Data or expert opinions supporting the comment.
- **Suggested Alternatives:** Alternative solutions or recommendations.
- **Impact Statements:** How the changes would impact the commenters and their communities. Impacts on commenters should include time and effort required to comply with the changes.

For each section, include a direct quote from the material. When including quotes, ensure they are directly extracted. Do not paraphrase or generate quotes. If a direct quote cannot be found, clearly state that no direct quote is available.

Write everything at an 8th grade literacy level.
"""
    
    completion = rag_with_vector_search(ai_prompt, 3, specific_instructions)

    # save guidance message
    st.session_state["guidance"] = completion

st.write(st.session_state["guidance"])
st.markdown(":blue-background[Would you like to make a comment?]")

previous = st.button("Cancel")
next = st.button("Make Comment")

if previous:
    st.switch_page("pages/2_Choose.py")

if next:
    st.switch_page("pages/4_Comment.py")

# for debugging and monitoring
# st.divider()
# st.write(st.session_state["thread"])

# st.divider()
# st.write(st.session_state["debug"])