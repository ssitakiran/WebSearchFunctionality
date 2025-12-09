from configparser import ConfigParser
import os

class Config:
    def __init__(self, config_file="src/langgraphagenticai/UI/uiconfigfile.ini"):
        self.config=ConfigParser()
        x=os.path.exists(config_file)
        if(x):
            self.config.read(config_file)
        else:
            return
    
    
    def get_llm_options(self):
        value=self.config.get("DEFAULT", "LLM_OPTIONS")
        values=value.split(", ")
        return values
    
    def get_usecase_options(self):
        return self.config["DEFAULT"].get("USECASE_OPTIONS").split(", ")
    
    def get_groq_model_options(self):
        return self.config["DEFAULT"].get("GROQ_MODEL_OPTIONS").split(", ")
    
    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE")
    