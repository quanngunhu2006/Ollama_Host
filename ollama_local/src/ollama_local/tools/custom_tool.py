from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from .read import PDF_Read
import os
from langchain_ollama import OllamaLLM, ChatOllama
from langchain_anthropic import AnthropicLLM
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from crewai import LLM
from langchain_openai import ChatOpenAI



load_dotenv()

#Begining of CustomPDFTool
class PDFToolInput(BaseModel):
    """Input schema for PDF extraction tool."""
    pdf_path: str = Field(..., description="Full path to the PDF file.")

class CustomPDFTool(BaseTool):
    name: str = "PDF Text/Table/Image Extractor"
    description: str = (
        "Extracts text, tables, and images from a given PDF. "
        "Returns the structured text content for further analysis."
    )
    args_schema: Type[BaseModel] = PDFToolInput

    def _run(self, pdf_path: str) -> str:
        try:
            
            # Validate PDF file exists
            if not os.path.exists(pdf_path):
                return f"Error: PDF file not found at path: {pdf_path}"
            
            # Create output directories if they don't exist
            text_dir = "C:/Users/dohuu/Desktop/Crew project Test/new_project/src/new_project/tools/text_temp"
            image_dir = "C:/Users/dohuu/Desktop/Crew project Test/new_project/src/new_project/tools/image_temp"
            
            os.makedirs(text_dir, exist_ok=True)
            os.makedirs(image_dir, exist_ok=True)
            
            # Initialize PDF reader with paths
            reader = PDF_Read(
                pdf_path=pdf_path,
                text_output_path=os.path.join(text_dir, "extracted_text.txt"),
                #image_to_text_path=os.path.join(text_dir, "extracted_images_to_text.txt"),
                image_output_dir=image_dir
            )

            # Extract all data
            text_store = reader.extract_text()
            table_store = reader.extract_table()
            reader.image_extract()  
            reader.store_text(text_store, table_store)
            reader.read_images(reader.image_store)  # Extract text from images

            # Combine text + tables for LLM-friendly output
            combined_text = "\n\n".join(text_store)
            table_texts = [table.to_string(index=False) for table in table_store]
            combined_table_text = "\n\n".join(table_texts)

            result = f"Successfully extracted from PDF: {pdf_path}\n\n"
            result += f"Extracted Text:\n{combined_text}\n\n"
            result += f"Extracted Tables:\n{combined_table_text}\n\n"
            result += f"Images saved to: {image_dir}\n"
            result += f"Text saved to: {text_dir}/extracted_text.txt"
            
            return result
            
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
#End of CustomPDFTool
    


#Begining of custom_qa
class QuerryInput(BaseModel):
    question: str = Field(...,description = "The user's question")
    read_path: str = Field(...,description = "Path to the txt file extracted from the PDF")

class CustomQA(BaseTool):
    name:str = "Custom QA Tool"
    description:str = "Answer questions based on the extracted PDF content."
    args_schema: Type[BaseModel] = QuerryInput

    def _run(self, question: str, read_path: str) -> str:
        try:
            with open(read_path, "r", encoding="utf-8") as file:
                text = file.read()

            # Optionally append image-based text if available
            # Change the file path if needed
            image_text_path = "C:/Users/dohuu/Desktop/Crew project Test/new_project/src/new_project/tools/text_temp/extracted_images_to_text.txt"
            if os.path.exists(image_text_path):
                with open(image_text_path, "r", encoding="utf-8") as img_file:
                    image_text = img_file.read()
                    text += f"\n\n=== OCR from Images ===\n{image_text}"

            prompt = (
                "You are given the following extracted text from a PDF:\n"
                f"{text}\n\n"
                f"Please answer this question based on the content: {question}"
            )

            # llm = ChatAnthropic(
            #    model="claude-3-haiku-20240307",
            #    api_key=os.getenv("ANTHROPIC_API_KEY")
            # )
            
            llm = ChatOllama(
                model = "qwen2.5:7b",
                #api_key = os.getenv("API_BASE"),
                base_url = os.getenv("API_BASE")
            )


            response = llm.invoke(prompt)
            answer = response.content if hasattr(response, "content") else str(response)
            
            with open("C:/Users/dohuu/Desktop/Crew project Test/answer_output.txt", "w", encoding="utf-8") as f:
                f.write(answer)

            return answer

        except Exception as e:
            return f"Error reading extracted text files: {str(e)}"
#End of custom_qa

                
                

            



