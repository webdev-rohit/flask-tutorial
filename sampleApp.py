from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/home")  # / and /home will redirect to the same page
def home():
    return "<h1>Hello, Rohit!</h1>"

@app.route("/about")
def about():
    return "<h1>About Rohit!</h1>"


if __name__ == "__main__":
    app.run(debug=True)