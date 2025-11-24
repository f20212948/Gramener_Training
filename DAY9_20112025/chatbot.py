import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List, Union


GOOGLE_GEMINI_API_KEY = "AIzaSyCimETCgcfkXOPUnCcyfuRxiAmJOUIOG6I"

def format_docs(docs: List[str]) -> str:
    """Combines documents into a single string for the prompt context."""
    return "\n\n".join(doc.page_content for doc in docs)

#-- Core RAG Logic ---

def setup_rag_chain(llm, retriever):

    # 1. Define the Prompt Template (Crucial for grounding the answer in the context)
    prompt_template = """
    You are an AI assistant specialized in answering questions based on the provided documents.
    Answer the user's question only based on the 'CONTEXT' provided below. 
    If the answer is not found in the context, clearly state that you do not have enough information.

    CONTEXT:
    {context}

    QUESTION: {question}
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    # 2. Define the LCEL Chain
    rag_chain = (
        # Map the incoming dictionary (which contains the 'question')
        {
            # 'context': gets the list of documents from the retriever, then formats them
            "context": retriever | format_docs,
            # 'question': passes the original question string through
            "question": RunnablePassthrough(),
        }
        # Pass the structured input (context, question) to the prompt
        | prompt
        # Pass the formatted prompt to the LLM
        | llm
        # Parse the final output into a simple string
        | StrOutputParser()
    )
    return rag_chain

def main():
    st.set_page_config(page_title="Gemini PDF Chatbot", layout="wide")
    st.header("Gemini PDF RAG Chatbot")

    # Initialize session state for processed data
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    
    if GOOGLE_GEMINI_API_KEY == "":
        st.warning("Please set your `GEMINI_API_KEY` ")
        return

    # --- Sidebar for File Upload ---
    with st.sidebar:
        st.title("Your Documents")
        file = st.file_uploader("Upload a PDF file and start asking questions", type="pdf")
        
        # Process file if uploaded
        if file is not None:
            # Check if this file has already been processed to avoid re-running embeddings
            if st.session_state.vector_store is None or st.session_state.vector_store.file_name != file.name:
                with st.spinner("Processing PDF..."):
                    try:
                        # 1. Extract the text
                        pdf_reader = PdfReader(file)
                        text = "".join(page.extract_text() or "" for page in pdf_reader.pages)
                        
                        # 2. Break it into chunks
                        text_splitter = RecursiveCharacterTextSplitter(
                            separators=["\n\n", "\n", ".", " "],
                            chunk_size=1000,
                            chunk_overlap=200,
                            length_function=len
                        )                                                           
                        chunks = text_splitter.split_text(text)
                        
                        # 3. Generating embeddings and creating vector store (FAISS)
                        embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-004", google_api_key=GOOGLE_GEMINI_API_KEY)
                        vector_store = FAISS.from_texts(chunks, embeddings)
                        
                        # Store in session state
                        st.session_state.vector_store = vector_store
                        st.session_state.vector_store.file_name = file.name
                        st.success(f"PDF '{file.name}' processed successfully!")
                    
                    except Exception as e:
                        st.error(f"Error processing file: {e}")
                        st.session_state.vector_store = None
    
    # --- Main Chat Interface ---

    vector_store = st.session_state.vector_store
    
    if vector_store:
        user_question = st.text_input("Ask a question about the document:", key="user_input")

        if user_question:
            with st.spinner("Searching and generating answer..."):
                try:
                    # 1. Define the LLM
                    llm = ChatGoogleGenerativeAI(
                        model="gemini-2.5-flash",
                        temperature=0.0,
                        max_output_tokens=1000,
                        google_api_key=GOOGLE_GEMINI_API_KEY,
                    )
                    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
                    rag_chain = setup_rag_chain(llm, retriever)
                    response = rag_chain.invoke(user_question)
                    st.subheader("Answer")
                    st.info(response)

                except Exception as e:
                    st.error(f"An error occurred during chain execution: {e}")
    else:
        st.info("Please upload a PDF document in the sidebar to start.")


if __name__ == "__main__":
    main()
