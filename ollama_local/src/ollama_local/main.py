#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from ollama_local.crew import Ollama_Local

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
import os

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
# def run():
#     """
#     Run the crew.
#     """
    
#     question = input("Please ask something: ")
#     inputs = {
#     "pdf_path": "C:/Users/dohuu/Desktop/TestPDF/BCMS.pdf",
#     #"pdf_path": pdf_path,
#     "question":question,
#     "read_path": "C:/Users/dohuu/Desktop/Crew project Test/new_project/src/new_project/tools/text_temp/extracted_images_to_text.txt"
#     }
        
#     try:
#         Ollama_Local().crew_qa().kickoff(inputs=inputs)  
#     except Exception as e:
#         raise Exception(f"An error occurred while running the crew: {e}")

def run(pdf_path: str):
    """
    Run the crew.
    """
    
    
    inputs = {
    #"pdf_path": "C:/Users/dohuu/Desktop/TestPDF/BCMS.pdf",
    "pdf_path": pdf_path,
    #"question":question,
    "read_path": "C:/Users/dohuu/Desktop/Ollama_Host/ollama_local/src/ollama_local/tools/text_temp/extracted_images_to_text.txt"
    }
        
    try:
        Ollama_Local().crew_pdf_extract().kickoff(inputs=inputs)  
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def run_sec(pdf_path: str, question: str):
    """
    Run the crew.
    """
    
    
    inputs = {
    #"pdf_path": "C:/Users/dohuu/Desktop/TestPDF/BCMS.pdf",
    "pdf_path": pdf_path,
    "question":question,
    "read_path": "C:/Users/dohuu/Desktop/Ollama_Host/ollama_local/src/ollama_local/tools/text_temp/extracted_images_to_text.txt"
    }
        
    try:
        Ollama_Local().crew_qa().kickoff(inputs=inputs)  
        result_file = "C:/Users/dohuu/Desktop/Ollama_Host/answer_output.txt"
        if os.path.exists(result_file):
            with open(result_file, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return "⚠️ Task completed but no answer found."
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        Ollama_Local().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Ollama_Local().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        Ollama_Local().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
