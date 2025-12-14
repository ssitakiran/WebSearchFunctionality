from langchain_community.tools import TavilySearchResults
from langgraph.prebuilt import ToolNode


def get_tools():
    
    """
    return the list of tools used in chat bot
    
    """
    tools=[TavilySearchResults(max_results=2)]    
    return tools



def create_tool_node(tools):
    """
        Args:
        tools (_type_): _description_
    """
    return ToolNode(tools=tools)