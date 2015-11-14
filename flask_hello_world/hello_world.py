from flask import Flask,  render_template

app = Flask(__name__)

@app.route("/")
@app.route("/hello")
def say_hi():
    return "Hello World!"

@app.route("/hello/<name>")
def hello_person(name):
    return render_template('template_hello.html', username = name)

    
@app.route("/jedi/<first_name>/<last_name>")
def jedi_name(first_name, last_name):
    return render_template('template.html')
   
'''   
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
'''


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)