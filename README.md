# 🌐 AWSage: Your AI-Powered AWS Guru

<a href="https://youtu.be/95gRG43AcXg">
    <img src="thumbnail.jpg" alt="AWSage YouTube Walkthrough" width="400" height="200"/>
</a>

Welcome to **AWSage**, the ultimate agentic chatbot that’s ready to tackle all your AWS Compute queries with ease! Powered by cutting-edge AI, RAG (Retrieval-Augmented Generation), and LangChain technologies, AWSage transforms static FAQs into dynamic conversations, delivering accurate, consolidated answers to even the most complex questions.

🖥️ **Check out the video walkthrough [here](https://youtu.be/95gRG43AcXg)**<br>
📄 **Read the full Project Report [here](report.pdf)**

## 🚀 How AWSage Works
![Chatbot Architecture](chatbot_architecture.png "AWSage Architecture")

AWSage is more than just a chatbot—it’s your personal guide through the labyrinth of AWS services. Here's how it does the magic:

### 🛠️ Key Features
- **Interactive FAQ Experience**: No more digging through pages of static FAQs! AWSage brings them to life in a chat interface where you can ask and get answers in real-time.
- **Hybrid Query Handling**: Whether the answer lies in pre-embedded knowledge or requires a live web search, AWSage has you covered.
- **Smart Routing**: Every query is directed to the best tool or model for the job, ensuring you get fast, accurate responses every time.

## 🏗️ Project Structure
Ready to set up AWSage? Follow these simple steps and you’ll be up and running in no time!

### 🔧 Installation:
1. **Clone the repo**: `git clone https://github.com/yourusername/awsage.git`
2. **Navigate to the project directory**: `cd awsage`
3. **Install the necessary libraries**: `pip install -r requirements.txt`
4. **Add your API keys**:
    - `JINA_API_KEY` for [Jina Text Embeddings](https://jina.ai/embeddings/)
    - `PINECONE_API_KEY` for [Pinecone](https://www.pinecone.io/) Vector Store
    - `OPENAI_API_KEY` for [OpenAI](https://platform.openai.com/) LLM
    - `TAVILY_API_KEY` for [Tavily](https://app.tavily.com/sign-in) web search

### 🗂️ Project Components:
- **data-collection**
    - `scrapper.py`: The mighty scraper that pulls all the FAQs from AWS, saving them as CSV files for later use.
- **vector-embeddings**
    - `embed.py`: Converts those scraped FAQs into embeddings—think of it as giving the chatbot its knowledge base.
- **pinecone-data-upload**
    - `load-data.py`: Uploads the embeddings to Pinecone, where they’re stored for quick retrieval.
- **chatbot**
    - `app.py`: Your gateway to AWSage, running on Streamlit with a sleek interface.
    - `graph_service.py`: Manages the LangGraph service and the Agentic Workflow, ensuring everything runs smoothly.

## 🎯 Fine-Tuning AWSage

### 🧠 Overview
To make AWSage even smarter, we fine-tuned it using OpenAI's `gpt-4o-mini-2024-07-18` model. This step sharpens its ability to generate spot-on responses tailored to AWS FAQs.

### 📝 Prerequisites
Before you start, make sure you have an OpenAI API key with fine-tuning privileges. Without it, AWSage won’t reach its full potential.

### 🛠️ Steps to Fine-Tune:
1. **Prepare the Data**:
    - Run `fine_tuning/create_data.py` to format the AWS FAQ data for fine-tuning. This script ensures everything is perfectly aligned for OpenAI’s process.
2. **Start the Fine-Tuning Job**:
    - Open the `fine_tuning/fine_tuning.ipynb` notebook and execute all cells. This will kick off the fine-tuning job, which is processed on OpenAI’s servers.
3. **Configure AWSage**:
    - Once fine-tuning is complete, set `USE_FINE_TUNED_MODEL` to `TRUE` in your `.env` file to make AWSage use the new model.

### ⏳ A Note on Fine-Tuning
Fine-tuning can be time-consuming, especially with large datasets. Keep an eye on the process through the OpenAI dashboard to ensure everything’s on track.

### ▶️ Running AWSage:
Fire up AWSage by running: `streamlit run chatbot/app.py`

## 💬 Get in Touch
Questions, suggestions, or just want to chat? Reach out!

- **Email**: [satyapanthi.t@northeastern.edu](mailto:satyapanthi.t@northeastern.edu)
- **LinkedIn**: [tapaswi-v-s](https://www.linkedin.com/in/tapaswi-v-s/)

## 📜 License
This project is licensed under the MIT License—see the [LICENSE](LICENSE) file for details.

---

Thanks for stopping by! I hope AWSage helps make your AWS journey a little smoother. Happy chatting! 🤖✨
