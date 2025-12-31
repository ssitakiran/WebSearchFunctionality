from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
from pathlib import Path

class AINewsNode:
    def __init__(self, llm):
        """
        Initialize the AI news with tavily and groq API keys
        """
        self.tavily = TavilyClient()
        self.llm=llm
        
        #This is used to capture various states in this file so that later can be use for steps shown
        self.state={}
        
    def fetch_news(self, state:dict)-> dict:
        """
        Fetch the AI news based on the freequency
        
        Args:
            state(dict): The state dictionary containing freequency
        
        returns:
            dict: updated state with news_data key containing fetched news
        """
        frequency = state['messages'][0].content.lower()
        self.state['frequency']=frequency
        time_range_map = {'daily':'d', 'weekly':'w', 'monthly':'m', 'year':'y'}
        days_map={'daily':1, 'weekly':7, 'monthly':30, 'year':366}
        
        response = self.tavily.search(
            query="Top Artificial intelligenc (AI) news India and Globally",
            topic='news',
            time_range=time_range_map[frequency],
            max_results=15,
            days=days_map[frequency]
        )
        state['news_data']=response.get('results', [])
        self.state['news_data']=state['news_data']
        
        return state
    
    
    def summarize_news(self, state:dict)-> dict:
        """
        Summarize the fetched news using an LLM
        
        Args:
            state(dict): The state dictionary containing 'news_data'
        
        returns:
            dict: updated state with 'summary' key containing summarized news
            
        """
        state=self.state
        news_items = state['news_data']
        
        prompt_template=ChatPromptTemplate.from_messages(
            [('system', """Summarize AI news and articles into markdown format. For each item include:
             Date in **YYYY-MM-DD format in IST time zone
             Concise sentence summary from latest news
             Sort news by date wise (latest first)
             Source URL as link
             Use Format:
             ### [Date]
             - [Summary](URL) """),
             ('user', "Articles:\n {articles}")
            ]
        )
        
        articles_str="\n\n".join([
            f"Content:{item.get('content', '')}\nURL:{item.get('url', '')}\nDate:{item.get('published_date', '')}"
            for item in news_items
        ])
        
        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary']=response.content
        self.state['summary']=state['summary']
        return self.state
    
    def save_result(self, state):
        frequency = self.state['frequency']
        summary = self.state['summary']
        cwd = Path.cwd()
        print(cwd)
        filename = f"{cwd}/AINews/{frequency}_summary.md"
        with open(filename, 'w') as f:
            f.write(f"#{frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename']=filename
        
        return self.state
    
    
        
        
        
        