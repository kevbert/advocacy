import streamlit as st
from tenacity import retry, wait_random_exponential, stop_after_attempt
import time
import pymongo
from openai import AzureOpenAI
import json

def reset_values():
    st.session_state["user_interest"] = ""
    st.session_state["user_role"] = ""
    st.session_state["intro_message"] = ""
    st.session_state["dis_message"] = ""
    st.session_state["guidance"] = ""
    st.session_state["comment"] = ""
    st.session_state["review"] = ""
    st.session_state["last_message_id"] = ""
    st.session_state["thread"] = ""
    st.switch_page("Home.py")


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
def generate_embeddings(text: str):
    '''
    Generate embeddings from string of text using the deployed Azure OpenAI API embeddings model.
    This will be used to vectorize document data and incoming user messages for a similarity search with
    the vector index.
    '''
    client:AzureOpenAI = st.session_state["ai_client"]
    deployment = st.session_state["EMBEDDINGS_DEPLOYMENT_NAME"]
    response = client.embeddings.create(input=text, model=deployment)
    embeddings = response.data[0].embedding
    time.sleep(0.5) # rest period to avoid rate limiting on AOAI
    return embeddings

def vector_search(collection_name, query, num_results=3):
    """
    Perform a vector search on the specified collection by vectorizing
    the query and searching the vector index for the most similar documents.

    returns a list of the top num_results most similar documents
    """
    db = st.session_state["db"]
    collection = db[collection_name]
    query_embedding = generate_embeddings(query)    
    pipeline = [
        {
            '$search': {
                "cosmosSearch": {
                    "vector": query_embedding,
                    "path": "contentVector",
                    "k": num_results
                },
                "returnStoredSource": True }},
        {'$project': { 'similarityScore': { '$meta': 'searchScore' }, 'document' : '$$ROOT' } }
    ]
    results = collection.aggregate(pipeline)
    return results

def print_chunk_search_result(result):
    '''
    Print the search result document in a readable format
    '''
    print(f"Similarity Score: {result['similarityScore']}")  
    print(f"_id: {result['document']['_id']}\n")


def rag_with_vector_search(question: str, num_results: int = 3):
    """
    Use the RAG model to generate a prompt using vector search results based on the
    incoming question.  
    """
    ai_client = st.session_state["ai_client"]
    deployment = st.session_state["COMPLETIONS_DEPLOYMENT_NAME"]
    # perform the vector search and build document chunk list
    results = vector_search("cms_open", question, num_results=num_results)
    chunk_list = ""
    for result in results:
        if "contentVector" in result["document"]:
            del result["document"]["contentVector"]
        chunk_list += json.dumps(result["document"], indent=4, default=str) + "\n\n"

    # generate prompt for the LLM with vector results
    formatted_prompt = st.session_state["system_message"] + chunk_list

    # prepare the LLM request
    #add on to the thread
    st.session_state["thread"].append({"role": "user", "content": question})
    # put the system message in the thread, then the rest of the thread
    messages = [
        {"role": "system", "content": formatted_prompt},
        *st.session_state["thread"]
    ]

    completion = ai_client.chat.completions.create(messages=messages, model=deployment)
    #add to the thread
    st.session_state["thread"].append(completion.choices[0].message)
    return completion.choices[0].message.content