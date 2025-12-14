import streamlit as st
import os

from src.langgraphagenticai.UI.uiconfigfile import Config

class LoadStreamLitUI:
    
    def __init__(self):
        self.config=Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title=self.config.get_page_title(), layout='wide')
        st.header(self.config.get_page_title())

        with st.sidebar:
            #Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()
            
            #LLM Selection
            self.user_controls["selected_llm"]=st.selectbox("Select LLM", llm_options)
            
            if self.user_controls["selected_llm"]=="Groq":
                model_options = self.config.get_groq_model_options()
                self.user_controls["selected_groq_model"]=st.selectbox("select model", model_options)
                self.user_controls["GROQ_API_KEY"]=st.session_state["GROQ_API_KEY"]=st.text_input("API KEY", type="password")
                
                self.user_controls["GROQ_API_KEY"]="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"
                
                # Validate API Key
                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter your groq api key to proceed. don't have? Refer: groq") 
            
            ## use case selection
            self.user_controls["selected_usecase"]=st.selectbox("select usecases", usecase_options)   
            
            if(self.user_controls["selected_usecase"]=="Chatbot with tool"):
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]=st.text_input("TAVILY_API_KEY", type="password")
                
                os.environ["TAVILY_API_KEY"]=self.user_controls["TAVILY_API_KEY"]=st.session_state["TAVILY_API_KEY"]="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"
                
                
                if not self.user_controls["TAVILY_API_KEY"]:
                    st.warning("Please enter your tavily API key. If not, please visit tayily.com")       
        
        return self.user_controls

