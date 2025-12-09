from src.langgraphagenticai.state.state import State

class BasicChatBotNodesBuilder:
    """
    Basic chatbot logic implementation
    """
    
    def __init__(self, model):
        self.llm=model
    
    def process(self, state:State)->dict:
        return {"messages":self.llm.invoke(state["messages"])}
    