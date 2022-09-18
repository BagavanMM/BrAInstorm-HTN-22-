<<<<<<< HEAD
from flask import Flask, render_template, url_for, jsonify
=======
<<<<<<< HEAD
from flask import Flask, render_template, url_for, request, jsonify, abort, redirect, session
=======
from flask import Flask, render_template, url_for, request, jsonify
>>>>>>> 11c1cf7d37db099f5e7fc7e4c71e184c550ca95c
>>>>>>> 15dbdc5c8b34de4f64324e18203282ac67a8ee52
import argparse
import time

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels
from brainflow.data_filter import DataFilter
from brainflow.ml_model import MLModel, BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams

#app.py
import os
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

# google auth imports
import os
import pathlib
import requests
from google.auth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests


# app creation
# ------- google client ------- #

app = Flask(__name__)

app.secret_key = "unmol?"
# this is to set our environment to https because OAuth 2.0 only supports https environments
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# enter your client id you got from Google console
GOOGLE_CLIENT_ID = "561605353882-13ltjktdn7mtvfljfh9cgog0g4asrvb9.apps.googleusercontent.com"
# set the path to where the .json file you got Google console is
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(  # Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
            "openid"],  # here we are specifing what do we get after the authorization
    # and the redirect URI is the point where the user will end up after the authorization
    redirect_uri="http://localhost:5000/callback"
)


@app.route('/')
@app.route('/index')
def home():
    return render_template("index.html")


@app.route('/result', methods=['POST', 'GET'])
def result():
    BoardShim.enable_board_logger()
    DataFilter.enable_data_logger()
    MLModel.enable_ml_logger()

    params = BrainFlowInputParams()
    params.board_id = -1
    board_id = -1
    sampling_rate = BoardShim.get_sampling_rate(board_id)
    params = BrainFlowInputParams()
    # params.serial_port = 'COM6'

    board = BoardShim(-1, params)
    master_board_id = board.get_board_id()
    sampling_rate = BoardShim.get_sampling_rate(master_board_id)
    board.prepare_session()
    board.start_stream(45000)
    BoardShim.log_message(LogLevels.LEVEL_INFO.value,
                          'start sleeping in the main thread')
    # recommended window size for eeg metric calculation is at least 4 seconds, bigger is better
    time.sleep(5)
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()

    eeg_channels = BoardShim.get_eeg_channels(int(master_board_id))
    bands = DataFilter.get_avg_band_powers(
        data, eeg_channels, sampling_rate, True)
    feature_vector = bands[0]
    print(feature_vector)
    print(eeg_channels[0])

    mindfulness_params = BrainFlowModelParams(BrainFlowMetrics.MINDFULNESS.value,
                                              BrainFlowClassifiers.DEFAULT_CLASSIFIER.value)
    mindfulness = MLModel(mindfulness_params)
    mindfulness.prepare()
    print('Concentration: %s' % str(mindfulness.predict(feature_vector)))
    brainwave = ''
    if mindfulness.predict(feature_vector) > 0.916:
        brainwave = 0  # hi-beta
    elif mindfulness.predict(feature_vector) > 0.833:
        brainwave = 1  # beta
    elif mindfulness.predict(feature_vector) > .75:
        brainwave = 2  # lo-beta
    elif mindfulness.predict(feature_vector) > 0.5:
        brainwave = 3  # alpha
    elif mindfulness.predict(feature_vector) > 0.15:
        brainwave = 4  # theta
    else:
        brainwave = 5  # delta

    brainwave_dict = {"message": brainwave}

    mindfulness.release()

    restfulness_params = BrainFlowModelParams(BrainFlowMetrics.RESTFULNESS.value,
                                              BrainFlowClassifiers.DEFAULT_CLASSIFIER.value)
    restfulness = MLModel(restfulness_params)
    restfulness.prepare()
    print('Restfulness: %s' % str(restfulness.predict(feature_vector)))
    restfulness.release()

<<<<<<< HEAD
    return render_template(result)


app = Flask(__name__)  #naming our application
app.secret_key = "unmol?"  #it is necessary to set a password when dealing with OAuth 2.0
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  #this is to set our environment to https because OAuth 2.0 only supports https environments

GOOGLE_CLIENT_ID = "561605353882-13ltjktdn7mtvfljfh9cgog0g4asrvb9.apps.googleusercontent.com"  #enter your client id you got from Google console
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")  #set the path to where the .json file you got Google console is

flow = Flow.from_client_secrets_file(  #Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
    redirect_uri="http://127.0.0.1:5000/callback"  #and the redirect URI is the point where the user will end up after the authorization
)

def login_is_required(function):  #a function to check if the user is authorized or not
    def wrapper(*args, **kwargs):
        if "google_id" not in session:  #authorization required
            return abort(401)
        else:
            return function()

    return wrapper


@app.route("/login")  #the page where the user can login
def login():
    authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")  #this is the page that will handle the callback process meaning process after the authorization
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")  #defing the results to show on the page
    session["name"] = id_info.get("name")
    return redirect("/protected_area")  #the final page where the authorized users will end up


@app.route("/logout")  #the logout page and function
def logout():
    session.clear()
    return redirect("/")


@app.route("/")  #the home page where the login button will be located
def home():
    return render_template("index.html")


@app.route("/protected_area")  #the page where only the authorized users can go to
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"  #the logout button 

=======
    return render_template('results.html', user=brainwave_dict)
>>>>>>> 11c1cf7d37db099f5e7fc7e4c71e184c550ca95c


# a function to check if the user is authorized or not
def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:  # authorization required
            return abort(401)
        else:
            return function()

    return wrapper


@app.route("/login")  # the page where the user can login
def login():
    # asking the flow class for the authorization (login) url
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


# this is the page that will handle the callback process meaning process after the authorization
@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    # defing the results to show on the page
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    # the final page where the authorized users will end up
    return redirect("/protected_area")


@app.route("/logout")  # the logout page and function
def logout():
    session.clear()
    return redirect("/")


@app.route("/")  # the home page where the login button will be located
def home():
    return render_template("index.html")


# the page where only the authorized users can go to
@app.route("/protected_area")
@login_is_required
def protected_area():
    # the logout button
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"


app.run(debug=True)
