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
    return render_template('template_jedi.html', lastname = last_name, firstname = first_name)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)