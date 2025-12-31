from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from src.langgraphagenticai.tools.search_tools import get_tools, create_tool_node
from src.langgraphagenticai.state.state import State

from src.langgraphagenticai.node.basic_chatbot_node import BasicChatBotNodesBuilder
from src.langgraphagenticai.node.chatbot_with_Tool_Node import ChatBotToolNode

from src.langgraphagenticai.node.ai_news_node import AINewsNode

class GraphBuilder:
    def __init__(self, model):
        self.llm=model
        self.graph_builder = StateGraph(State)


    def basic_chatbot_build_graph(self):
        """
            Builds a basic chatbot using LangGraph
            This method initiates a chatbot node using the 'BasicChatBotNode' class
            and integrates into a graph. The chatbot is set as both entry and exit point of the graph        
        """
        
        self.basic_chatbot_node = BasicChatBotNodesBuilder(self.llm)
        
        
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)
    
    
    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanced chatbot graph with tools integration
        This method creates a chatbot graph that includes both a chatbot node
        and a tool node. it defines tools, initializes the chatbot with tool capabilities, 
        and sets up conditional and direct edges between nodes.
        The chatbot node is set as entry point
        """
        
        llm=self.llm
        self.chatbot_with_tools = ChatBotToolNode(self.llm)
        tools = get_tools()
        
        chatbotToolsDecisionStartNode = self.chatbot_with_tools.create_chatbot(tools=tools)
        
        self.graph_builder.add_node("chatbot", chatbotToolsDecisionStartNode)
        node=create_tool_node(tools=tools)
        self.graph_builder.add_node("tools", node)
        
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        
    
    def ai_news_builder_graph(self):
        llm=self.llm
        
        aiNewsObject=AINewsNode(llm=self.llm)
        
        
        # Added the nodes 
        self.graph_builder.add_node("fetch_news", aiNewsObject.fetch_news)
        self.graph_builder.add_node("summarize_news", aiNewsObject.summarize_news)
        self.graph_builder.add_node("save_results", aiNewsObject.save_result)
        
        #Added the edges  
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_results")
        self.graph_builder.add_edge("save_results", END)
        
        #self.graph_builder.add_node("chatbot", chatbotToolDecisionStartNode)
        #node=create_tool_node(tools=tools)
        #self.graph_builder.add_node("tools", node)
        
        #self.graph_builder.add_node("summarize", "")
        #self.graph_builder.add_node("saveresult", "")
    
        #self.graph_builder.add_edge(START, "chatbot")
        #self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        #self.graph_builder.add_edge("tools", "summarize")
        #self.graph_builder.add_edge("summarize", END)
    
    def setup_graph(self, usecase:str):
        """
        Sets up the graph for selected usecase
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        
        if usecase == "Chatbot with tool":
            self.chatbot_with_tools_build_graph()
        
        if usecase == "AI News":
            self.ai_news_builder_graph()
            
        
        graph1 = self.graph_builder.compile()
        
        return graph1