from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/spotify/callback')
def spotify_handler():
    site_args = request.args
    print(site_args)
    code = site_args.get('code')
    if code:
        with open("spot_comm.txt", "w") as file:
            file.write(f"CODE {code}")
        response = "Spotify Authentication Received"
    else:
        error = site_args.get('error').upper()
        with open("spot_comm.txt", "w") as file:
            file.write(error)
        response = f"Spotify Authentication Not Received, Reason: {error}"
    return render_template("spotify_callback.html", message=response)


@app.route('/twitch/callback')
def twitch_handler():
    site_args = request.args
    error = site_args.get("error")
    print(request.form)
    if error:
        pass
    else:
        pass
    return render_template("twitch_callback.html", message="Twitch")


if __name__ == '__main__':
    app.run()
