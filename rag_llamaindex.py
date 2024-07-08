import streamlit as st
from llama_index.llms.mistralai import MistralAI
from llama_index.core.llms import ChatMessage
from indexify import IndexifyClient
from decouple import config

llm = MistralAI(api_key=config("MISTRAL_API_KEY"))
client = IndexifyClient()


def query_database(question: str, index: str, top_k=3):
    retrieved_results = client.search_index(
        name=index, query=question, top_k=top_k)
    context = "\n-".join([item["text"] for item in retrieved_results])
    return context


def ai_responses(user_query):
    context = query_database(
        user_query, "wiki_extraction_pipeline_tutorial.wikiembedding.embedding", 4)

    print(context)

    messages = [
        ChatMessage(role="system",
                    content=(
                        "You are a helpful AI assistant. Answer user queries based on the context.\n"
                        f"Context: {context}"
                    )),
        ChatMessage(role="user", content=user_query),
    ]
    resp = llm.stream_chat(messages)

    for r in resp:
        yield r.delta


st.title("Hello, Welcome To Indexify")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(ai_responses(prompt))
    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
