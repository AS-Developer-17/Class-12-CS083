from InquirerPy import inquirer,prompt

# Simple Dropdown Selection
frameWork=inquirer.select(message="Select a framework: ",choices=["Vanilla", "Vue","React","Svelete"],default="React",).execute()
projectName= inquirer.text(message="Project Name", default="My-App",).execute()
installDep= inquirer.confirm(message="Install Dependecies: ",default=True ).execute()
print(f'''
Summary
Frameworks: {frameWork}
projectName: {projectName}
Dependencies: {installDep}     
      ''')

from InquirerPy import prompt

questions = [
    {
        "type": "input",
        "name": "username",
        "message": "Enter your username:",
    },
    {
        "type": "password",
        "name": "password",
        "message": "Enter your password:",
    },
    {
        "type": "checkbox",
        "name": "features",
        "message": "Select features to enable:",
        "choices": ["Auth", "Database", "Docker", "CI/CD Pipeline"],
    },
]

# Run the form
answers = prompt(questions)

# Result is returned as a clean dictionary
print(answers)
# Output: {'username': 'alex', 'password': '...', 'features': ['Auth', 'Docker']}
'''
What you wantDirect Object (inquirer.xxx)Dictionary Key ("type": "...")Text Inputinquirer.text()"input"Single Selectinquirer.select()"list" or "select"Multi Selectinquirer.checkbox()"checkbox"Passwordinquirer.secret()"secret" or "password"Yes / Noinquirer.confirm()"confirm"Fuzzy Searchinquirer.fuzzy()"fuzzy"File Pathinquirer.filepath()"filepath"
'''