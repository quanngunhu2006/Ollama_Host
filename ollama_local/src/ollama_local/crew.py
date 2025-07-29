from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from ollama_local.tools.custom_tool import CustomPDFTool  
from ollama_local.tools.custom_tool import CustomQA
from langchain_ollama import OllamaLLM





llm_model = OllamaLLM(
            model = "qwen2.5:7b"
    )




@CrewBase
class Ollama_Local():
    """NewProject crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    @agent
    def pdf_extract_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_extract_assistant'], #like a dictionary that store the key
            verbose=True,  #Pretty much print out the log
            tools=[CustomPDFTool()] 
        )

    @agent
    def qa_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_assistant'],
            verbose = True,
            tools =[CustomQA()],
           
        )

    
    @task
    def pdf_extract_task(self) -> Task:
        return Task(
            config=self.tasks_config['pdf_extract_task'], 
            output_file='C:/Users/dohuu/Desktop/Ollama_Host/ollama_local/src/ollama_local/tools/text_temp/extracted_text.md',
            description=(
                "Extract text, tables, and images from the PDF file located at: {pdf_path}. "
                "Use the PDF Text/Table/Image Extractor tool with the exact path provided. "
                "Store the extracted text in a markdown file and images in the specified directory. "
                "The PDF path to use is: {pdf_path}"
            ),
            tools=[CustomPDFTool()],
            agent=self.pdf_extract_assistant()
        )
    
    @task
    def qa_task(self) -> Task:
        return Task(
            config=self.tasks_config['qa_task'],
            description=(
                "Answer questions based on the contents of the extracted PDF text file."
                " The file is located at {read_path}."
                " Use this file to answer the user's question accurately."
                "The user question is {question}"
            ),
            tools=[CustomQA()],
            agent=self.qa_assistant()
        )

    
    @crew
    def crew_pdf_extract(self) -> Crew:
        """Creates the AiProject crew for PDF extraction"""

        return Crew(
            agents=[self.pdf_extract_assistant()],
            tasks=[self.pdf_extract_task()],
            process=Process.sequential,
            verbose=True,
            embedder={"provider":"[ollama]"},
        )
    
    def crew_qa(self) -> Crew:
        """Creates the AiProject crew for PDF extraction"""

        return Crew(
            agents=[self.qa_assistant()],
            tasks=[self.qa_task()],
            process=Process.sequential,
            verbose=True,
            embedder={"provider":"[ollama]"},
        
        )
    