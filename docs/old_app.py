from flask import Flask, render_template

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)