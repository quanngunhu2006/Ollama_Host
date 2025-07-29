How to Use

1. Create a venv
- Command: python -m venv nameofyourchoice
- Activate venv command: ./nameofyourchoice/Scripts/activate
- Deactivate venv command: deactivate
- This is just a temp venv for now

2. Set up the env
- env file should include these:
    + MODE=ollama/qwen2.5:7b or other ollama model you want            
    + API_BASE=     usually http://localhost:11434
    + EMAIL_ADDRESS
    + EMAIL_PASSWORD (Not the email password but the the security key that is for the 2-Step verification one)
    + FILE_TO_EXTRACT (Something like C:/Users/your_user/Desktop/Ollama_Host/ollama_local/src/ollama_local/tools/text_temp/extracted_images_to_text.txt)

3. How to run
- Cd into run_w_email and run the main.py in there
- If you want to just run the crew then just use crewai run but change the argument or remove it
- When you run the first time it will automatically create another venv inside the ollam_local folder, deactivate your current venv and use that one. It will be the one you will need to use later on

4. Some error or work need to be fix:
- Still need to fix the file path since it is hardcode right now, have to change it to dynamically so that multiple user can use
- My laptop can not handle big ollama model since it is only 16GB, therefore need to be test on a bigger model with a better spec
- JSON file extract for excel upload might need some tweak on the prompt that you give to the AI, since it has to match the name of the JSON file in order for it to upload to the Excel
- Gradio (the website you see when run main.py inside run_w_email) is just for demo, it does not automatically run your gmail checking. Instead, if you want to run it automatically you have to run it on the terminal which is the code I put as a comment you see down below the demo.launch() line
- Messy code :))

