import json
import requests
import flask
import httplib2
#from apiclient import discovery
from oauth2client import client
import mySQLreplica as mySQL

#HOME_PAGE_3TARGETING = "http://3Targeting.com?status="
HOME_PAGE_3TARGETING = "http://localhost:8012/connectors.php"

db = mySQL.Database()

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
  account_id = flask.request.args.get('state')
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
  #return "Refresh token is: " + refresh_token

  #Parse.pushAdwordsCredentials(account_id, access_token, refresh_token)

  adwordsCred = {} # credentials dictionary
  adwordsCred['id'] = account_id
  adwordsCred['adwords_access_token'] = access_token
  adwordsCred['adwords_refresh_token'] = refresh_token
  db.pushAdwordsCredentials(adwordsCred)

  #return "Account: " + account_id + "\n Access token: " + access_token + "\nRefresh token: " + refresh_token + "\n\n were pushed to Parse"
  return_url = HOME_PAGE_3TARGETING + "?status=ok"
  return flask.redirect(return_url)
  #return ("Access token for user " + account_id + " is " + access_token)

  #"Access token = " + access_token + "Refresh token = " + refresh_token
  #return flask.redirect(flask.url_for('index'))

@app.route('/salesforce/oauth2callback')
def salesforceOauth2callback():
  consumer_key = '3MVG98_Psg5cppyYH7Cios03svOf9hpZtPg.n0yTXRIKlnjy43.MNRgdLDbmBc3T5wK2IoYOaPLNlqBzNouzE'
  consumer_secret = 2132402812325087889
  request_token_url = 'https://login.salesforce.com/services/oauth2/token'
  access_token_url = 'https://login.salesforce.com/services/oauth2/token'
  redirect_uri = 'https://x3targeting.herokuapp.com/salesforce/oauth2callback'
  #authorize_url = 'https://login.salesforce.com/services/oauth2/authorize?response_type=token&client_id='+consumer_key+'&redirect_uri='+redirect_uri

  
  #return "Salesforce page"

  # check if got an error back
  error = flask.request.args.get('error','') 
  if error != '':
    return "Sorry dude, Google returned the following error: " + error

  account_id = flask.request.args.get('state')
  auth_code = flask.request.args.get('code')
  
  data = {
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
        'code': auth_code,
        'client_id' : consumer_key,
        'client_secret' : consumer_secret
    }
  headers = {'content-type': 'application/x-www-form-urlencoded'}
  req = requests.post(access_token_url,data=data,headers=headers)
  response = req.json()

  sfCred = {} # credentials dictionary
  sfCred['id'] = account_id
  sfCred['sf_id'] = response['id']
  sfCred['access_token'] = response['access_token']
  sfCred['refresh_token'] = response['refresh_token']
  sfCred['instance_url'] = response['instance_url']
  sfCred['issued_at'] = response['issued_at']
  sfCred['scope'] = response['scope']
  sfCred['signature'] = response['signature']
  sfCred['token_type'] = response['token_type']

  db.pushSalseforceCredentials(sfCred)

  return_url = HOME_PAGE_3TARGETING + "?status=ok"
  return flask.redirect(return_url)
  # sf = Salesforce(instance_url=response['instance_url'], session_id=response['access_token'])
  
  # return 'success'
  # records = sf.query("SELECT Id, Name, Email FROM Contact")
  # records = records['records']



  # account_id = flask.request.args.get('state')
  # auth_code = flask.request.args.get('code')
  # return "OK"
  # return "Account ID: " + account_id + "Code: " + auth_code

  #flow = client.OAuth2WebServerFlow(
  #  '3MVG98_Psg5cppyYH7Cios03svOf9hpZtPg.n0yTXRIKlnjy43.MNRgdLDbmBc3T5wK2IoYOaPLNlqBzNouzE',
  #  client_secret='2132402812325087889',
  #  #scope='https://www.googleapis.com/auth/adwords',
  #  redirect_uri='https://x3targeting.herokuapp.com/salesforce/oauth2callback',
  #  user_agent='3Targeting')
  #return "OK"
  # access_token = credentials.access_token
  # #return "Access token is: " + access_token
  # refresh_token = credentials.refresh_token
  # #return "Refresh token is: " + refresh_token
  # #return "Account: " + account_id + "\n Access token: " + access_token + "\nRefresh token: " + refresh_token + "\n\n were pushed to Parse"
  # return_url = HOME_PAGE_3TARGETING + "?status=ok"
  # return flask.redirect(return_url)
  
if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = True
  app.run()