import pdfplumber, pytesseract
import pandas as pd
from langchain_community.llms.ollama import Ollama
from langchain_ollama import OllamaLLM
import cv2 #pip install opencv-python
import pytesseract
import os
from .read_image import read_image




#PDF_PATH ="C:/Users/dohuu/Desktop/TestPDF/3D_NKH.pdf"
PDF_PATH = "C:/Users/dohuu/Desktop/TestPDF/BCMS 03 mtinh phục vụ lập trình ktg.pdf"


image_store = []


class PDF_Read:
    def __init__(self, pdf_path, text_output_path=None, image_output_dir=None):
        self.PDF_PATH = pdf_path
        self.text_output_path = text_output_path
        self.image_output_dir = image_output_dir
        self.image_store = []

    def extract_text(self):
        """Extracts text from a PDF file and prints each page with its number."""
        text_store = []

        with pdfplumber.open(self.PDF_PATH) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                formatted_text = f"\n=== Page {page_number} ===\n{text.strip()}"
                print(formatted_text)
                print("\n" + "=" * 50 + "\n")  # Separator for clarity
                text_store.append(formatted_text)
        return text_store



    def extract_table(self):
        """Extracts tables from a PDF file and stores them in a list of DataFrames."""
        table_store = []
        with pdfplumber.open(self.PDF_PATH) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables()
                if tables:
                    for table_index, table in enumerate(tables, start=1):
                        # Clean each cell by removing newlines
                        clean_table = [[cell.replace('\n', ' ') if cell else '' for cell in row] for row in table]
                        df = pd.DataFrame(clean_table)
                        print(f"\n=== Table {table_index} on Page {page_number} ===\n")
                        print(df.to_string(index=False, header=False))  # display like a nice table
                        table_store.append(df)
        return table_store

    def store_text(self,text_store,table_store):
        with open("C:/Users/dohuu/Desktop/Ollama_Host/ollama_local/src/ollama_local/tools/text_temp/extracted_text.txt", "w", encoding="utf-8") as f:
            f.write("\t\t\t=== Extracted Text from PDF ===\n\n")
            f.write("\n".join(text_store))
            f.write("\t\t\t=== Extracted Table from PDF ===\n\n")
            for i, table in enumerate(table_store):
                f.write(table.to_string(index=False))

    def image_extract(self):
        """Extracts images from a PDF file and saves them to the specified directory."""
        with pdfplumber.open(self.PDF_PATH) as pdf:
            folder_path = "C:/Users/dohuu/Desktop/Ollama_Host/ollama_local/src/ollama_local/tools/image_temp"
            for page_number, page in enumerate(pdf.pages, start=1):
                images = page.images
                for image_index, image in enumerate(images, start=1):
                    x0, y0, x1, y1 = image['x0'], image['top'], image['x1'], image['bottom']
                    im = page.within_bbox((x0, y0, x1, y1)).to_image(resolution=300) #Modify the resolution as needed
                    file_name=(f"image_page_{page_number}_img_{image_index}.png")
                    full_path = f"{folder_path}/{file_name}"
                    im.save(full_path)
                    self.image_store.append(full_path)

    def read_images(self, image_store):
        """Loop through all images in image_store and extract text from each"""
        # Clear the existing file content before writing new extractions
        with open("C:/Users/dohuu/Desktop/Ollama_Host/ollama_local/src/ollama_local/tools/text_temp/extracted_images_to_text.txt", "w", encoding="utf-8") as f:
            f.write("=== Extracted Text from Images ===\n\n")
        
        print(f"Total images to process: {len(image_store)}")
        for i, image_path in enumerate(image_store, 1):
            print(f"Processing image {i}/{len(image_store)}: {image_path}")
            try:
                # Check if image file exists
                if not os.path.exists(image_path):
                    print(f"Warning: Image file not found: {image_path}")
                    continue
                    
                # Create an instance of read_image class
                from .read_image import read_image
                image_reader = read_image(image_path)
                image_reader.extract_image()
                print(f"Successfully processed: {image_path}")
            except Exception as e:
                print(f"Error processing {image_path}: {str(e)}")
                import traceback
                traceback.print_exc()
                continue
                





if __name__ == "__main__":
    pdf_read_tool = PDF_Read(PDF_PATH)
    text_store=pdf_read_tool.extract_text()
    table_store=pdf_read_tool.extract_table()
    pdf_read_tool.image_extract()
    pdf_read_tool.store_text(text_store,table_store)
    

    #Convert to strings for LLM processing
    table_texts = [table.to_string(index=False) for table in table_store]

    #Create ollama LLM instance for Q&A
    llm = OllamaLLM(model="llava")
    querry = (f"Hãy tìm kiếm thông tin ứngng dụng phần mềm thiết kế vào quy trình thiết kế mô hình bay trong những file đã được"
              "trích xuất từ file PDF này và trả lời câu hỏi của tôi về mô hình ứng dụng phần mềm thiết kế vào quy trình thiết kế mô hình bay hoạt động như nào")
    
    pdf_read_tool.read_image(image_store)
    
    
    

    



    


