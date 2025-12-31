import streamlit as st
from langchain_core.messages import AIMessage, SystemMessage, ToolMessage, HumanMessage
from langgraph.graph import StateGraph
import json

class DisplayResultStreamlit:
    def __init__(self, usecase, graph:StateGraph, user_message):
        self.usecase=usecase
        self.graph=graph
        self.user_message=user_message
    
    def display_result_on_ui(self):
        usecase=self.usecase
        graph=self.graph
        user_message=self.user_message
        
        if usecase == "Basic Chatbot":
            for event in graph.stream({'messages':("user", user_message)}):
                print(event.values())
                for values in event.values():
                    print(values['messages'])
                    with st.chat_message("user"):
                        st.write(user_message)
                    with st.chat_message("assistant"):
                        st.write(values['messages'].content)
        
        if usecase == "Chatbot with tool":
            # Prepare state and invoke the graph
            initial_state = {"messages":[user_message]}
            print(initial_state)
            
            res = graph.invoke(initial_state)
            
            for message in res["messages"]:
                if str(type(message)) == "<class 'langchain_core.messages.human.HumanMessage'>":
                    with st.chat_message("user"):
                        st.write(message.content)
                elif str(type(message)) == "<class 'langchain_core.messages.tool.ToolMessage'>":
                    with st.chat_message("ai"):
                        st.write("Tool Call Start")
                        st.write(message.content)
                        st.write("Tool Call End")
                elif str(type(message)) == "<class 'langchain_core.messages.ai.AIMessage'>" and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)  
            
        if usecase == "AI News":
                frequency=self.user_message
                with st.spinner("Fetching and Summarizing news...."):
                    result=graph.invoke({'messages': frequency})
                    try:
                        AI_NEWS_PATH = f"./AINews/{frequency.lower()}_summary.md"
                        with open(AI_NEWS_PATH, "r") as file:
                            markdown_content=file.read()
                        # Display the markdown content in streamlit
                        st.markdown(markdown_content, unsafe_allow_html=True)
                    except FileNotFoundError:
                        st.error("News file not found")
                    except Exception as e:
                        st.error(e.with_traceback())    
                            

                
                
                        
            