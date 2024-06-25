import streamlit as st
from tenacity import retry, wait_random_exponential, stop_after_attempt
import time

# @st.cache_data   #TODO this should have caching
def run_thread(thread_id, assistant_id, client):
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        # instructions="Can add instructions here that override the Assistant's default instructions."
    )
    return run

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
def generate_embeddings(text: str, client, deployment):
    '''
    Generate embeddings from string of text using the deployed Azure OpenAI API embeddings model.
    This will be used to vectorize document data and incoming user messages for a similarity search with
    the vector index.
    '''
    response = client.embeddings.create(input=text, model=deployment)
    embeddings = response.data[0].embedding
    time.sleep(0.5) # rest period to avoid rate limiting on AOAI
    return embeddings

def vector_search(db, collection_name, query, num_results=3):
    """
    Perform a vector search on the specified collection by vectorizing
    the query and searching the vector index for the most similar documents.

    returns a list of the top num_results most similar documents
    """
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