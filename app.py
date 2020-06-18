from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/spotify/callback')
def spotify_handler() -> str:
    return "YOU DID IT!"


if __name__ == '__main__':
    app.run()
