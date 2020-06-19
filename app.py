from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/spotify/callback')
def spotify_handler() -> str:
    site_args = request.args
    code = site_args.get('code')
    if code:
        with open("_auth_code.py", "w") as file:
            file.write(f"auth_code = '{code}'")
        #quit()
    return render_template("sp_callback.html")


if __name__ == '__main__':
    app.run()
