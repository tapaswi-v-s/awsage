# AWSage Chatbot

## Chatbot Overview
AWSage is an agentic chatbot designed to streamline the handling of AWS Compute queries by leveraging a combination of generative AI, RAG (Retrieval-Augmented Generation), and LangChain technologies. This chatbot transforms traditional FAQ systems into a dynamic, interactive solution, capable of handling complex queries that span multiple AWS topics, providing precise and consolidated responses.

**Find the Project Report [here](report.pdf)**

## How this Chatbot Works
![Chatbot Architecture](chatbot_architecture.png "chatbot_architecture")

## Features
- **Dynamic FAQ Integration:** Converts static AWS FAQ content into an interactive chat interface.
- **Hybrid Query Handling:** Utilizes embedded knowledge and real-time internet search to answer a wide range of queries.
- **Smart Routing:** Efficiently directs questions to the most appropriate tool or model, optimizing response accuracy and speed.

## Project Structure
Follow these steps to set up and run the final chatbot:

### Installation:
1. Clone the repo.
2. Navigate to the project directory: `cd awsage`
3. Install the necessary libraries: `pip install -r requirements.txt`
4. Add the following required keys to your `.env` file:
    - `JINA_API_KEY` for [Jina Text Embeddings](https://jina.ai/embeddings/)
    - `PINECONE_API_KEY` for [Pinecone](https://www.pinecone.io/) Vector Store
    - `OPENAI_API_KEY` for [OpenAI](https://platform.openai.com/) LLM
    - `TAVILY_API_KEY` for [Tavily](https://app.tavily.com/sign-in) web search

### Project Components:
- **data-collection**
    - `scrapper.py`: Scrapes all the FAQs and their answers from the AWS website. These scrapped FAQs and answers will be stored in the CSV files.
- **vector-embeddings**
    - `embed.py`: Converts the scrapped FAQs and answers into embeddings and saves them into CSV files.
- **pinecone-data-upload**
    - `load-data.py`: Upserts the embeddings to Pinecone vector store.
- **chatbot**
    - `app.py`: The main entry point of the chatbot with a Streamlit interface.
    - `graph_service.py`: The LangGraph service that encompasses the Agentic Workflow with tools.

### Running the Application:
Execute the following command to run the chatbot: `streamlit run chatbot/app.py`

## Contact Information
For further inquiries or suggestions, please contact me at:
- Email: [satyapanthi.t@northeastern.edu](mailto:satyapanthi.t@northeastern.edu)
- LinkedIn: [tapaswi-v-s](https://www.linkedin.com/in/tapaswi-v-s/)
