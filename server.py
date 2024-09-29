from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  
import os
import random
import string

app = Flask(__name__)
CORS(app)  

OUTPUT_DIR = "files"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CURRENT_IDS = []


def generate_id():
    isChecking = True

    for file in os.listdir(OUTPUT_DIR):
        currentfilename = os.fsdecode(file)
        CURRENT_IDS.append(str(currentfilename))

    while isChecking:
        characters = string.ascii_letters + string.digits
        new_id = ''.join(random.choices(characters, k=8))

        if f"{new_id}.html" not in CURRENT_IDS:
            isChecking = False
            return new_id
    

@app.route('/generate', methods=['POST'])
def generate_file():
    new_id = generate_id()
    filename = request.json.get('filename')
    content = request.json.get('content')

    file_path = os.path.join(OUTPUT_DIR, f"{new_id}.html")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"""
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{filename} - Pastebin Copy</title>
    <link rel="stylesheet" href="../style.css" > 
</head>
<body>
    <h1 style="text-align: center;">{filename}</h1>
    <hr style="width: 400px; margin-top: -15px;">
    <section>
        <div style="height: 300px; width: 700px; background-color: #fff; border: 2px solid #ccc; border-radius: 8px;">{content}</div>
    </section>
</body>
</html>
""")

    return jsonify({"file": f"{new_id}.html"})

@app.route('/generated_files/<path:filename>')
def serve_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
