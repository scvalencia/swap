from urllib import urlencode
import base64
import urlfetch

def get_access_token(cid, secret, api_url='https://api.vimeo.com/oauth/authorize/client'):
 
    encoded = base64.b64encode("%s:%s" % (cid, secret)) 
    payload = {
                "grant_type": "client_credentials",
                "scope": "public create"
            }
    headers = {
                "Accept": "application/vnd.vimeo.*+json; version=3.0",
                "Authorization": "basic %s" % encoded
              }
    response = urlfetch.fetch(api_url,
                          method="POST",
                          headers=headers,
                          payload=urlencode(payload),
                          )
    if response.status_code != 200:
        raise ValueError(response.status_code)
    else:
        return json_loads(response.content)

cid = '9e294bd6d65205f53a583c4c733ad50b2126fe18'
secret = 'e96e11b5353292fa9ca91caa5662dd45ca553da0'

print get_access_token(cid, secret)