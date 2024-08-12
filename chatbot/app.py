from graph_service import GraphService
import streamlit as st

# Initialize the GraphService only once
@st.cache_resource
def get_graph_service():
    return GraphService()

# Main app function
def main():
    st.set_page_config(
    page_title="AWSage",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded")

    graph_service = get_graph_service()
    if not graph_service.check_for_vector_store():
        st.error("Pinecone Vector Store not initialized, \
                        \nplease execute: 'pinecone-data-upload/load_data.py'")
        st.stop()
    else:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.experimental_rerun()
        st.title("AWSage: AWS Queries Assistant")

        body ="""Hi there! I'm AWSage, your AWS chatbot here to help you navigate the complexities of AWS Compute services.
                Whether you have questions about instances, storage, or configuration, I've got the answers
                based on the AWS Compute FAQs.\n\nHere are the types of questions you can ask:
                
        - How can I use EC2 with S3?
    - Is Amazon ECR similar to Docker?
    - How much does AWS Batch cost?
    - How much does ECR cost?"""
        st.write(body)
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display chat history
        for message in st.session_state.chat_history:
            if message[0] == "user":
                with st.chat_message(message[0], avatar="🧑‍💻"):
                    st.markdown(message[1])
            else:
                with st.chat_message(message[0],avatar="🤖"):
                    st.markdown(message[1])


        # User input
        if user_query := st.chat_input("Ask me anything about AWS Compute"):
            
            # Display user message in chat message container
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(user_query)
            
            # Append user message to chat history
            st.session_state.chat_history.append(("user", user_query))
            with st.spinner('Gathering Information...'):
                response = graph_service.invoke(user_query)
                st.session_state.chat_history.append(("assistant", response))
            
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(response)


if __name__ == "__main__":
    main()