__author__ = 'assafdekel'
from parse_rest.connection import register
from parse_rest.datatypes import Object
import json

# declare keys
APPLICATION_ID = "zEw8OuVGoLit8vfLuofQZuKAJa6TIWTgKmInIt1F"
REST_API_KEY = "VZWgc30TFeResXW0oOHW21haVMSkiZXugm2hO72L"
#MASTER_KEY = "PeCO4elOGe1Inreo6g9WZkmdRxCon8EkDLbxDkIv"

#class test_credentials(Object):
#    pass

class accounts(Object):
    pass

#def __init__(self):
    # 1. register to Parse.com DB
#   register(APPLICATION_ID, REST_API_KEY)

#def pushTokens(userId, gglAccessToken, gglRefreshToken):
#	adwordsCredentials = adwords(active=True, user_id = userId, google_access_token = gglAccessToken, google_refresh_token = gglRefreshToken)
#    credentials = test_credentials(user_id = userId, google_access_token = gglAccessToken, google_refresh_token = gglRefreshToken)
#    credentials.save()

def pushAdwordsCredentials(accountId, gglAccessToken, gglRefreshToken):
	adwordsCredentials = {'active':True, 'access_token':gglAccessToken, 'refresh_token':gglRefreshToken}
	# encode as a JSON-like string
	adwordsCredentials = json.loads(json.dumps(adwordsCredentials))
	adwordAccount  = accounts(objectId=accountId,adwords=adwordsCredentials)
	adwordAccount.save()