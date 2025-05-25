from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from rag import process_document, ask_question

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

vectordb = None  # global variable to store the vector DB after upload

@app.route("/", methods=["GET", "POST"])
def index():
    global vectordb
    answer = ""
    if request.method == "POST":
        if "pdf_file" in request.files:
            file = request.files["pdf_file"]
            if file.filename != "":
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                file.save(filepath)
                vectordb = process_document(filepath)

        question = request.form.get("question")
        if question and vectordb:
            answer = ask_question(vectordb, question)

    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
