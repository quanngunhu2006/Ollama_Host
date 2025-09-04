# Description
- This program is use for automatically reading new email and download PDF work file 
- 3 main function:
    + Download PDF automatically from email/outlook (need change)
    + Allow user to ask local host AI about the working PDF
    + Allow user to push the PDF information to the Excel

# How to Use


## 1. Create a venv
- Command: `python -m venv nameofyourchoice`
- Activate venv command: `./nameofyourchoice/Scripts/activate`
- Deactivate venv command: `deactivate`
- This is just a temp venv for now




## 2. Set up the env and package
- env file should include these:
    + `MODE=ollama/qwen2.5:7b` or other ollama model you want            
    + `API_BASE`     default can be `http://localhost:11434`
    + `EMAIL_ADDRESS`
    + `EMAIL_PASSWORD` (Not the email password but the the security key that is for the 2-Step verification one)
    + `FILE_TO_EXTRACT` (Something like C:/Users/your_user/Desktop/Ollama_Host/ollama_local/src/ollama_local/tools/text_temp/extracted_images_to_text.txt)

- You can try to change Email address and Email password to outlook address and outlook password (the security key one). I have not try it yet, but it might be able to work just fine with STMP and IMAP like email, so you can try to tweak that env a bit.
- Download all of the tools from requirements.txt file
- Download pytesseract for image scan from this git https://github.com/tesseract-ocr/tesseract


## 3. How to run
- Change the file path that is being hardcode to your file path
- Cd into `run_w_email` and run the `main.py` in there
- If you want to just run the crew then just use crewai run but change the argument or remove it
- When you run the first time it will automatically create another venv inside the ollam_local folder, deactivate your current venv and use that one. It will be the one you will need to use later on





## 4. Some error or work need to be fix:
- Still need to fix the file path since it is hardcode right now, have to change it to dynamically so that multiple user can use
- My laptop can not handle big ollama model since it is only 16GB (there are some better model like `nqduc/mixsura:mixsura-q6_K` that might work better with Vietnamese text but require 32GB RAM), therefore need to be test on a bigger model with a better spec
- JSON file extract for excel upload might need some tweak on the prompt that you give to the AI, since it has to match the name of the JSON file in order for it to upload to the Excel
- Gradio (the website you see when run main.py inside `run_w_email`) is just for demo, it does not automatically run your gmail checking. Instead, if you want to run it automatically you have to run it on the terminal which is the code I put as a comment you see down below the `demo.launch()` line
- Right now it is also only detect new email that has the title "PROCESS DOCUMENT" can be change to another if needed
- Messy code :))








# Cách sử dụng

## 1. Tạo một venv
- Lệnh: python `-m venv nameofyourchoice`
- Lệnh kích hoạt venv: `./nameofyourchoice/Scripts/activate`
- Lệnh dừng venv: `deactivate`
- Đây chỉ là một venv tạm thời

## 2. Thiết lập env và các công cụ khác
- Tệp env nên bao gồm các mục sau:
+ `MODE=ollama/qwen2.5:7b` hoặc mô hình ollama khác mà người dùng muốn
+ `API_BASE` mặc định sẽ là `http://localhost:11434`
+ `EMAIL_ADDRESS`
+ `EMAIL_PASSWORD` (Không phải mật khẩu email mà là khóa bảo mật dùng cho xác minh 2 bước)
+ `FILE_TO_EXTRACT` (Ví dụ: C:/Users/your_user/Desktop/Ollama_Host/ollama_local/src/ollama_local/tools/text_temp/extracted_images_to_text.txt)

- Người dùng có thể thử thay đổi địa chỉ Email và nhập mật khẩu email vào địa chỉ Outlook và mật khẩu Outlook (khóa bảo mật). Tôi chưa thử, nhưng có thể nó hoạt động ok với STMP và IMAP như email, vì vậy người dùng có thể thử điều chỉnh file env.
- Tải tất cả các công cụ từ requirements.txt file 
- Tải pytesseract cho việc phân tích và đọc hình ảnh từ https://github.com/tesseract-ocr/tesseract

## 3. Cách chạy
- Thay đổi file path đang được mã hóa cứng thành đường dẫn tệp của bạn
- Cd vào `run_w_email` và chạy `main.py` trong đó
- Nếu bạn chỉ muốn chạy crew thì chỉ cần sử dụng crewai run nhưng thay đổi các giá trị được truyền vào hàm hoặc xóa nó trc khi dùng
- Khi bạn chạy lần đầu tiên, nó sẽ tự động tạo một venv khác bên trong thư mục ollam_local, hãy hủy kích hoạt venv hiện tại của bạn và sử dụng venv đó. Đây sẽ là phiên bản bạn cần sử dụng sau này.

## 4. Một số lỗi hoặc công việc cần sửa:
- Vẫn cần sửa đường dẫn tệp vì hiện tại nó đang được mã hóa cứng, phải thay đổi thành dạng động để nhiều người dùng có thể sử dụng.
- Máy tính của tôi không thể xử lý mô hình ollama lớn vì nó chỉ có 16GB (có một số mô hình tốt hơn như `nqduc/mixsura:mixsura-q6_K` có thể hoạt động tốt hơn với văn bản tiếng Việt nhưng yêu cầu 32GB RAM), do đó cần phải thử nghiệm trên một mô hình lớn hơn với thông số kỹ thuật tốt hơn.
- Trích xuất tệp JSON để tải lên Excel có thể cần một số điều chỉnh về lời nhắc mà bạn cung cấp cho AI, vì nó phải khớp với tên của tệp JSON để tải lên Excel.
- Gradio (trang web bạn thấy khi chạy main.py bên trong `run_w_email`) chỉ mang tính chất demo, nó không tự động chạy kiểm tra Gmail của bạn. Thay vào đó, nếu bạn muốn chạy nó tự động, bạn phải chạy nó trên terminal, đó là phần code mà tôi đã để trong phần bình luận mà bạn thấy bên dưới dòng `demo.launch()`.
- Hiện tại, nó chỉ phát hiện email mới có tiêu đề "PROCESS DOCUMENT" và người dùng có thể chỉnh sửa để đổi thành tiêu đề khác nếu cần.
- Code hơi lộn xộn :))



