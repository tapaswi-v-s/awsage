from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import JinaEmbeddings
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, PromptTemplate
from langchain_core.messages.human import HumanMessage
from langgraph.prebuilt import tools_condition
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pinecone.grpc import PineconeGRPC as Pinecone
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

class GraphService:

    def check_for_vector_store(self):
        "Checks if the index is exists in the pinecone or not"
        pc = Pinecone(api_key=os.environ['PINECONE_API_KEY'])
        indexes = pc.list_indexes().names()
        
        if os.environ.get('PINECONE_INDEX', 'aws-faq') in indexes:
            return True
        else:
            return False


    def init_tools(self):
        def init_retriever_tool():
            embeddings = JinaEmbeddings(jina_api_key=os.environ['JINA_API_KEY'], 
                            model_name='jina-embeddings-v2-base-en')
            vector_store = PineconeVectorStore.from_existing_index(index_name=os.environ.get('PINECONE_INDEX', 'aws-faq'),
                                                                    embedding=embeddings,
                                                                    namespace=os.environ.get('PINECONE_INDEX', 'FAQ'), 
                                                                    text_key='answer')
            retriever = vector_store.as_retriever(search_kwargs={'k':3})
            return create_retriever_tool(retriever, 'retriever_aws_faqs',
                                        'Search and return information about amazon web service(AWS) Compute \
                                        from the vector store created from the scrapped AWS FAQs.')
        
        def init_search_tool():
            tavily_search = TavilySearchResults(
                max_result = 5,
                search_depth="advanced",
                include_answer=True,
                include_raw_content=False,
                include_images=False
            )
            return tavily_search
        
        self.tools = []
        self.tools.extend([init_retriever_tool(), init_search_tool()])


    def init_nodes_and_edges(self):
        def agent_node(state):
            """Invokes the agent model to generate a response based on the current state. Given
            the question, it will decide to retrieve using the retriever tool, or simply end.

            Args:
                state (messages): The current state

            Returns:
                dict: The updated state with the agent response appended to messages"""
            messages = state["messages"]
            model = ChatOpenAI(temperature=0, streaming=True, model="gpt-3.5-turbo-0125")
            model = model.bind_tools(self.tools)
            response = model.invoke(messages)
            return {"messages": [response]}
        self.agent_node = agent_node
        
        def generate_node(state):
            """Generate answer
            Args:
                state (messages): The current state
            Returns:
                dict: The updated state with re-phrased question
            """

            messages = state["messages"]
            question = list(filter(lambda x: isinstance(x, HumanMessage), messages))[-1]
            last_message = messages[-1]
            docs = last_message.content
            
            prompt = ChatPromptTemplate.from_messages([
                ('system', 'You are a helpful assistant for question-answering tasks about amazon web service.'),
                ('human', "Use the following pieces of retrieved context to answer the question. \
                and keep the answer concise. \
                 If the provided context has no information about the question \
                 then just reply politely that you don't have the information about it.\
                \nQuestion: {question} \nContext: {context} \nAnswer:")
            ])
            if os.environ.get('USE_FINE_TUNED_MODEL', 'false').lower() == 'true':
                client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
                model = list(client.fine_tuning.jobs.list())[0].fine_tuned_model
                llm = ChatOpenAI(model_name=model, temperature=0, streaming=True)
            else:        
                llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, streaming=True)
                
            rag_chain = prompt | llm | StrOutputParser()
            response = rag_chain.invoke({'question':question, 'context':docs})
            return {"messages": [response]}
        self.generate_node = generate_node

    def init_graph(self):
        class AgentState(TypedDict):
            messages: Annotated[Sequence[BaseMessage], add_messages]
        workflow = StateGraph(AgentState)
        workflow.add_node("agent", self.agent_node)
        workflow.add_node("tools", ToolNode(self.tools))
        workflow.add_node("generate", self.generate_node)

        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges("agent", tools_condition, {"tools":"tools", END: END})
        workflow.add_edge('tools', 'generate')
        workflow.add_edge('generate', END)
        self.graph = workflow.compile(checkpointer=MemorySaver())

    def __init__(self) -> None:
        if self.check_for_vector_store():
            self.init_tools()
            self.init_nodes_and_edges()
            self.init_graph()
            self.config = {"configurable": {"thread_id": "1"}}
        

    def invoke(self, query):
        response = self.graph.invoke({"messages":query}, config=self.config)
        response = response['messages'][-1].content
        return response