from flask import Flask
from os import environ

app = Flask(__name__)

@app.route("/")
@app.route("/hello")
def say_hi():
    return "Hello World!"

@app.route("/hello/<name>")
def hello_person(name):
    html = """
        <h1>
            Hello {}!
        </h1>
        <p>
            Here's a picture of a kitten.  Awww...
        </p>
        <img src="http://placekitten.com/g/200/300">
    """
    return html.format(name.title())
        
    
@app.route("/jedi/<first_name>/<last_name>")
def jedi_name(first_name, last_name):
    html = """
        <h1>
            Hello {}!
        </h1>
        <p>
            Your Jedi Name is {}
        </p>
     """
    jedi_full_name = last_name[:3] + first_name[:2]
    return html.format(first_name.title(), jedi_full_name.title())

if __name__ == "__main__":
    app.run(host=environ['IP'],
            port=int(environ['PORT']))