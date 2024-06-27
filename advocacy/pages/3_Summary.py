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
Summarize the relevant information in simple, clear language suitable for a general audience (8th grade reading level). 
Include ONLY information from the sources.
Include the following sections:

**Current Policy**
    Briefly explain the current policy (2-3 sentences)

**Proposed Changes**
    Summarize the proposed changes (3-5 bullet points)

    Include a direct quote detailing the main change (up to 50 words)

**Key Issues and Impacts**
    List 3-5 main issues addressed by the policy
    Describe potential impacts on patients, healthcare providers, and the healthcare system
    Include a direct quote about a significant impact (up to 50 words)

**Evidence and Expert Opinions**
Summarize key data or statistics supporting the policy (1-2 bullet points)

**Alternative Proposals**
If available, briefly describe 1-2 alternative solutions

**Impact on Patients**
Explain how the policy will affect patients (1-2 sentences)

**Impact and Burden on Healthcare Providers**
Describe how the policy will impact healthcare providers (1-2 sentences)

**Next Steps**
Explain how readers can provide feedback on the policy (1-2 sentences)



Guidelines:

Use simple language and explain any technical terms
Include direct quotes where specified; do not paraphrase or generate quotes
Clearly state if a direct quote is unavailable for any section
Maintain accuracy while simplifying complex concepts
Focus on information relevant to patients, doctors, advocates, and researchers
Cite the source document for all information and quotes
"""

    
    completion = rag_with_vector_search(ai_prompt, 6, specific_instructions)

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

st.divider()
st.write(st.session_state["debug"])