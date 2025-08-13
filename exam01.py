from flask import Flask, render_template, request, redirect, make_response
from aws import detect_labels_local_file, compare_faces
from werkzeug.utils import secure_filename

import os

# Ensure the static directory exists
if not os.path.exists("static"):
    os.makedirs("static")
    
app = Flask(__name__)
@app.route("/")
def exam01():
    # return render_template("exam01.html")
    return render_template("index.html")

@app.route("/compare", methods=["POST"])
def compare():
    if request.method == "POST":
        file1 = request.files["file1"]
        file2 = request.files["file2"]
        if file1 and file2:
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            file_path1 = f"static/{filename1}"
            file_path2 = f"static/{filename2}"
            file1.save(file_path1)
            file2.save(file_path2)

            result = compare_faces(file_path1, file_path2)
            return result
    return "No 응애 uploaded."

@app.route("/detect", methods=["POST"])
def detect_label():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            file_path = f"./static/{filename}"
            file.save(file_path)
            return detect_labels_local_file(file_path)

@app.route("/secret", methods=["POST"])
def box():
    try:
        if request.method == "POST":
            # secret = request.form.get("secret")
            hidden = request.form["hidden"]
            return f"{hidden}"
    except:
        return "fail"

@app.route("/login", methods=["GET"])
def login():
    if request.method == "GET":
        
        # redirect to login page
        if "username" not in request.args or "password" not in request.args:
            return redirect("/")
        
        username = request.args.get("username")
        password = request.args.get("password")
        if username == "admin" and password == "1234":
            response = make_response(redirect("/login/success"))
            response.set_cookie("username", username)
            return response
        else:
            return "가라"
    return f"{username} 게빵식 login complete </br> password: {password}"
        
@app.route("/login/success", methods=["GET"])
def login_success():
        username = request.cookies.get("username")
        return f"{username} 게빵식 login success"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)