import cv2
import pytesseract
import numpy as np

#image_path = 'C:/Users/dohuu/Desktop/Crew project Test/new_project/src/new_project/tools/image_temp/image_page_1_img_1.png'

class read_image:
    #Optional: Resize if image is too large for OCR
    def __init__(self, image_path):
        self.image_path = image_path

    @staticmethod
    def resize_image(image, max_width=2000):
        h, w = image.shape[:2]
        if w > max_width:
            scale = max_width / w
            return cv2.resize(image, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
        return image

    #Load the image



    def extract_image(self):
        img = cv2.imread(self.image_path)

        #C:/Users/dohuu/Downloads/test-image.png test if need
        if img is None:
            raise FileNotFoundError(f"Image not found: {self.image_path}")

        #Preprocess: grayscale and resize (safely)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = self.resize_image(gray)

        #OCR configuration
        custom_config = r'--oem 3 --psm 6'

        #Extract text in Vietnamese
        extracted_text = pytesseract.image_to_string(gray, lang='vie', config=custom_config)
        print("Extracted Text:\n")
        print(extracted_text)

        #Get character bounding boxes
        h, w = gray.shape[:2]
        boxes = pytesseract.image_to_boxes(gray, lang='vie', config=custom_config)

        #Draw each bounding box
        img_boxed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # Convert back to BGR for drawing
        for b in boxes.splitlines():
            b = b.split()
            if len(b) >= 5:
                x1, y1, x2, y2 = int(b[1]), int(b[2]), int(b[3]), int(b[4])
                cv2.rectangle(img_boxed, (x1, h - y2), (x2, h - y1), (0, 255, 0), 1)
        

        #Show the result
        #cv2.imshow('OCR Result with Boxes', img_boxed)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        #Store the text
        with open("C:/Users/dohuu/Desktop/Ollama_Host/ollama_local/src/ollama_local/tools/text_temp/extracted_images_to_text.txt", "a", encoding="utf-8") as f:
           f.write(f"\n--- Image: {self.image_path} ---\n")
           f.write(extracted_text)
           f.write("\n" + "="*50 + "\n")


