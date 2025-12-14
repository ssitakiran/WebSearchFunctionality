from src.langgraphagenticai.state.state import State


class ChatBotToolNode:
    """
    chatbot logic enhanced with tool integration
    """
    def __init__(self, model):
        self.llm=model
    
    
    def process(self, state:State)->dict:
        
        """
         process the input and generate chatbot response
        """
        
        return {"messages": self.llm.invoke(state["messages"])}
    
    def create_chatbot(self, tools):
       llm_with_tools = self.llm.bind_tools(tools)
       
       def chatbot_node(state:State):
            return {"messages":[llm_with_tools.invoke(state["messages"])]}
       
       return chatbot_node