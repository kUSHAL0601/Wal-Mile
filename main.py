from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/admin")
def transport_admin():
    return render_template('transport_admin.html')
    
if __name__ == "__main__":
    app.run(debug=True)