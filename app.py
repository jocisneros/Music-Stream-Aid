from flask import Flask, request, render_template

app = Flask(__name__)
num_login = 0


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/spotify/callback')
def spotify_handler():
    site_args = request.args
    code = site_args.get('code')
    if code:
        with open("inter_comm.txt", "w") as file:
            file.write(f"CODE {code}")
        global num_login
        num_login += 1
        response = "Spotify Authentication Received"
    else:
        error = site_args.get('error').upper()
        with open("inter_comm.txt", "w") as file:
            file.write(error)
        response = f"Spotify Authentication Not Received, Reason: {error}"
    return render_template("api_callback.html", message=response)


@app.route('/twitch/callback')
def twitch_handler():
    return render_template("api_callback.html", message="Twitch")


def end_web():
    if num_login >= 2:
        quit()


if __name__ == '__main__':
    app.run()
