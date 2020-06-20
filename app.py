from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/spotify/callback')
def spotify_handler():
    site_args = request.args
    code = site_args.get('code')
    if code:
        with open("_auth_code.txt", "w") as file:
            file.write(code)
    return render_template("sp_callback.html")


if __name__ == '__main__':
    app.run()
