import streamlit as st

from src.langgraphagenticai.UI.streamlitui.loadui import LoadStreamLitUI
from src.langgraphagenticai.LLMs.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.UI.streamlitui.display_result import DisplayResultStreamlit
from langgraph.graph import StateGraph, START, END

def load_langgraph_agenticai_app():
    """
    Loads and rums the langgraph AgenticAI with Streamlit UI.
    This function initializes the ui, handles user input, configures the LLM model,
    sets up the graph based on the selected use case, and displays the output while
    implementing exception handling for robustness
    """
    
    ## Load UI
    
    ui=LoadStreamLitUI()
    user_input=ui.load_streamlit_ui()
    
    if not user_input:
        st.error("Error: Failed to load user input from UI")
        return 
    else:
        user_message = st.chat_input("Enter your message:")
    
        if user_message:
            try:
                #Configure LLM
                obj_llm_config = GroqLLM(user_controls_input=user_input)
                model=obj_llm_config.get_llm_model()
         
                if not model:
                    st.error("Error: LLM model cannot be initialized")
                    return
                
                #initialize the set up and graph based on the case
                usecase = user_input.get("selected_usecase")
                
                if not usecase:
                    st.error("Error: No usecase selected")
                
                ## Create the graph builder
                graph_builder=GraphBuilder(model=model)
                try:
                    returned_graph = graph_builder.setup_graph(usecase)
                    DisplayResultStreamlit(usecase=usecase, graph=returned_graph, user_message=user_message).display_result_on_ui()
                except Exception as e:
                    st.error(e)
                    return  
            except Exception as e:
                st.error(e)
                
