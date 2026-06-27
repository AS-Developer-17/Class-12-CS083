import os 
import google.genai as genai

os.environ["GOOGLE_API_KEY"] = "AIzaSyDtyi49ASpcZNdi3RR59Sck1X2GPWYgHS0"

client = genai.Client()

def notesGenerator():
    inputTopic = input("Enter the topic you want to generate notes on: ")
    def replyFunc(userPrompt):   
        response = client.models.generate_content(model="gemini-3-flash-preview", 
            contents=f"Generate Notes on the topic '{userPrompt}' in a detailed and structured way. Include key points, examples, and explanations. ")
        with open(f"{userPrompt}_Notes.txt", "w") as file:
            file.write(response.text)
        print(f"Notes on '{userPrompt}' have been generated and saved to '{userPrompt}_Notes.txt'.")

    replyFunc(inputTopic)

def FileSummarization():
    filePath = input("Type the file name: ")
    with open(filePath, "r") as file:
        data = file.read()
        response = client.models.generate_content(model="gemini-3-flash-preview", 
            contents=f"Summarize the following content in a concise and clear manner: {data}")
        print("Summary of the file:")
        print(response.text)
def CodeGenerator():
    inpProjectName = input("Type project name: ")
    inpProjectDescription= input("Describe about the project: ")
    inpProjectLang = input("Type Language 'Use File Extension': ")
    response = client.models.generate_content(model="gemini-3-flash-preview", 
    contents=f"Generate Code Only that is directly runnable  on '{inpProjectDescription}' in '.{inpProjectLang}' format .")
    with open(f"{inpProjectName}_Notes.{inpProjectLang}", "w") as file:
        file.write(response.text)
    print(f"Codes on '{inpProjectName}' have been generated and saved to '{inpProjectName}_Notes.txt'.")
        
CodeGenerator()