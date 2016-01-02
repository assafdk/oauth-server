import json

import flask
import httplib2
#import ParseAPI
#from apiclient import discovery
from oauth2client import client
#import ParseAPI as Parse

#HOME_PAGE_3TARGETING = "http://3Targeting.com?status="
HOME_PAGE_3TARGETING = "http://localhost:8000/settings.php"

# Parse
APPLICATION_ID = "zEw8OuVGoLit8vfLuofQZuKAJa6TIWTgKmInIt1F"
REST_API_KEY = "VZWgc30TFeResXW0oOHW21haVMSkiZXugm2hO72L"

app = flask.Flask(__name__)


@app.route('/')
def index():
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return flask.redirect(flask.url_for('oauth2callback'))
  else:
    http_auth = credentials.authorize(httplib2.Http())
    #drive_service = discovery.build('drive', 'v2', http_auth)
    #files = drive_service.files().list().execute()
    return 'seccess' #json.dumps(files)

@app.route('/google-adwords/oauth2callback')
def oauth2callback():
  # check if got an error back
  error = flask.request.args.get('error','') 
  if error != '':
    return "Sorry dude, Google returned the following error: " + error
  #code = flask.request.args.get('code','')
  #ret_str = 'Hello Google! Your code is ' + code
  #return ret_str
  #user_id = flask.request.args.get('state')
  flow = client.OAuth2WebServerFlow(
    '280160838890-kjhls6qlss26fj1f2kr7v61fh5esmmuk.apps.googleusercontent.com',
    client_secret='ZQLzF8TadPS3Zpk52rACGsKG',
    scope='https://www.googleapis.com/auth/adwords',
    redirect_uri='https://x3targeting.herokuapp.com/google-adwords/oauth2callback',
    user_agent='3Targeting')

  #flow = client.flow_from_clientsecrets(
  #    'client_secrets.json',
  #    scope='https://www.googleapis.com/auth/adwords')
  
  #if 'code' not in flask.request.args:
  #  auth_uri = flow.step1_get_authorize_url()
  #  return flask.redirect(auth_uri)
  #else:
  auth_code = flask.request.args.get('code')
  credentials = flow.step2_exchange(auth_code)
  #return "yay, got credentials"
  ##flask.session['credentials'] = credentials.to_json()
  access_token = credentials.access_token
  #return "Access token is: " + access_token
  refresh_token = credentials.refresh_token
  return "Refresh token is: " + refresh_token
  #Parse.register(APPLICATION_ID, REST_API_KEY)
  #Parse.pushTokens(userId = user_id, gglAccessToken = access_token, gglRefreshToken = refresh_token)

  return_url = HOME_PAGE_3TARGETING + "?status=ok"
  #return redirect(return_url)
  return ("Access token for user " + user_id + " is " + access_token)

  #"Access token = " + access_token + "Refresh token = " + refresh_token
  #return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = False
  app.run()