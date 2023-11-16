from flask import Flask, request, render_template
from flask_cors import CORS 
import subprocess
import sys

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')  # Assuming you have an HTML file with the editor and other elements

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    user_code = data.get('userCode', '')
    input_text = data.get('inputText', '')
    language = request.headers.get('X-Language')

    # Define the file name based on the language
    file_extension = {
        'c': 'c',
        'cpp': 'cpp',
        'python': 'py',
        'Java': 'java',
        'node': 'js'
    }.get(language, 'txt')

    file_name = f'user_code.{file_extension}'

    # Write the user's code to a file
    with open(file_name, 'w') as file:
        file.write(user_code)

    # Execute the code using subprocess
    if(language == "python"):
        try:
            result = subprocess.check_output([sys.executable, file_name],input = input_text, stderr=subprocess.STDOUT, text=True)
            return result
        except subprocess.CalledProcessError as e:
            return str(e.output)
    elif(language == "c"):
        try:
            compile_result = subprocess.run(['gcc', file_name, '-o', 'compiled_code'], capture_output=True, text=True)
            if compile_result.returncode != 0:
                return f"Compilation Error:\n{compile_result.stderr}"
            result = subprocess.run(['./compiled_code'], input=input_text, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Runtime Error:\n{result.stderr}"

        except Exception as e:
            return f"Exception: {str(e)}"
    elif(language == "cpp"):
        try:
            compile_result = subprocess.run(['g++', file_name, '-o', 'compiled_code_cpp'], capture_output=True, text=True)
            if compile_result.returncode != 0:
                return f"Compilation Error:\n{compile_result.stderr}"
            result = subprocess.run(['./compiled_code_cpp'], input=input_text, capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Runtime Error:\n{result.stderr}"

        except Exception as e:
            return f"Exception: {str(e)}"
    elif(language == "Java"):
        compile_result = subprocess.run(['javac', file_name], capture_output=True, text=True)
        if compile_result.returncode != 0:
            return f"Compilation Error:\n{compile_result.stderr}"
        class_name = file_name.replace(".java", "")
        result = subprocess.run(['java', class_name], input=input_text, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Runtime Error:\n{result.stderr}"
    elif(language == "node"):
        result = subprocess.run(['node', file_name], input=input_text, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Runtime Error:\n{result.stderr}"
    else:
        return "Unsupported language"
    

if __name__ == '__main__':
    app.run(port=3000, debug=True)

