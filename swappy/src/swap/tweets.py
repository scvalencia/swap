# Post tweets
# Return tweets given hashtag

from twython import Twython
from datetime import datetime
import urllib, urllib2
import tweepy, json
import time

OAUTH_TOKEN = '716680344-ahbgchi0AbseVA4KJqEqwvi89vX6TFkd4EaZZyH9'
OAUTH_SECRET = 'tIlUT5Tz4TrVjKSm1xCwtEww5vCP1tefRpjvJrM3peUXJ'
CONSUMER_KEY = 'K43bBhVihgtt7RBOqTeYb36Yw'
CONSUMER_SECRET = 'fEQwIFtMPWmMHvSjoUQuGtrNYM0efYQeaT8fUCfn6CBEpKvyxd'
HASH_TAG = "#SwapStockEchange"

class Tweet(object):

    def __init__(self, user, body):
        self.username = user['screen_name'].encode('ascii','ignore')
        self.text = body.encode('ascii','ignore')

    def __str__(self):
        ans = ''
        ans += self.username + ' : '
        ans += self.text
        return ans

class TwitterHandler(object):    

    def __init__(self):
        self.consumer_key = CONSUMER_KEY
        self.consumer_secret = CONSUMER_SECRET
        self.access_token = OAUTH_TOKEN
        self.access_token_secret = OAUTH_SECRET
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth)
        self.twython = Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET)

    def post(self, message):
        if len(message) <= 140:
            try:
                self.api.update_status(message)
            except:
                pass

    def get_data(self, keyword, length):
        ans = []
        try:
            result_set = self.twython.search(q = keyword, count = length)
            tweets = result_set['statuses']
            for tweet in tweets:
                body = tweet['text']
                user_object = tweet['user']
                new_object = Tweet(user_object, body)
                ans.append(new_object)
            return ans
        except:
            return ans

class MessageGenerator(object):

    FLAG_COMPRA = 0
    FLAG_VENTA = 1
    FLAG_DINERO = 0
    FLAG_MONTO = 1

    def __init__(self):
        pass

    def register_value(self, value, user):
        value = str(value)
        user = str(user)
        date = time.strftime('%Y/%m/%d %H:%M:%S')
        formatting_values = (value, user, str(date))
        msg = 'Nuevo valor %s agregado por %s en %s.' % formatting_values
        msg += ' ' + HASH_TAG
        return msg

    def register_rent(self, rent, value, user):
        rent = str(rent)
        value = str(value)
        user = str(user)
        date = time.strftime('%Y/%m/%d %H:%M:%S')
        formatting_values = (rent, value, user, str(date))
        msg = 'Tipo de rentabilidad %s del valor %s agregado por %s, fecha : %s.' \
            % formatting_values
        msg += ' ' + HASH_TAG
        return msg

    def register_passive(self, name, register):
        name = str(name)
        register = str(register)
        date = time.strftime('%Y/%m/%d %H:%M:%S')
        formatting_values = (name, register, str(date))
        msg = 'Nuevo intermediadio registrado en Swap: [%s, %s], fecha : %s.' \
            % formatting_values
        msg += ' ' + HASH_TAG
        return msg

    def register_offerant(self, name):
        name = str(name)
        date = time.strftime('%Y/%m/%d %H:%M:%S')
        formatting_values = (name, str(date))
        msg = 'Nuevo oferente registrado en Swap: %s, fecha : %s.' \
            % formatting_values
        msg += ' ' + HASH_TAG
        return msg

    def register_investor(self, name):
        name = str(name)
        date = time.strftime('%Y/%m/%d %H:%M:%S')
        formatting_values = (name, str(date))
        msg = 'Nuevo inversionista registrado en Swap: %s, fecha : %s.' \
            % formatting_values
        msg += ' ' + HASH_TAG
        return msg

    def register_operation(self, investor, value, quantity, quantity_type, operation_type):
        investor = str(investor)
        value = str(value)
        quantity = str(quantity)
        try:
            quantity_type = int(quantity_type)
            operation_type = int(operation_type)
            msg = ''
            date = time.strftime('%Y/%m/%d %H:%M:%S')
            operation_kind = 'DINERO' if quantity_type == self.FLAG_DINERO else 'MONTO'
            if operation_type == self.FLAG_COMPRA:
                msg = 'El usuario %s desea comprar '
                if operation_kind == 'DINERO':
                    msg += '$%s en acciones del valor %s'
                else:
                    msg += '%s unidades del valor %s'
                
            else:
                msg = 'El usuario %s desea vender '
                if operation_kind == 'DINERO':
                    msg += '$%s en acciones del valor %s'
                else:
                    msg += '%s unidades del valor %s'
                pass
            msg += ', registrado en %s.'
            msg = msg % (investor, quantity, value, str(date))
            msg += ' ' + HASH_TAG
            return msg
        except:
            return ''

    def ring(self, seller, buyer, value):
        seller = str(seller)
        buyer = str(buyer)
        value = str(value)
        msg = 'El usuario %s ha comprado el valor %s de %s el %s.'
        date = time.strftime('%Y/%m/%d %H:%M:%S')
        formatting_values = (buyer, value, seller, str(date))
        msg += ' ' + HASH_TAG
        return msg % formatting_values

def example():
    swap_twitter = TwitterHandler()
    messaging = MessageGenerator()
    messages = []
    # Cada mensaje se debe generar al realizar un movimiento!!
    messages.append(messaging.register_value('Pepsi', 'scvalencia'))
    messages.append(messaging.register_rent('Pepsi', 'Coca', 'scvalencia'))
    messages.append(messaging.register_passive('wer', '234234234'))
    messages.append(messaging.register_offerant('jcbages'))
    messages.append(messaging.register_investor('wer'))
    messages.append(messaging.register_operation('scvalencia', 'Coca', '1233', 0, 0))
    messages.append(messaging.register_operation('scvalencia', 'Coca', '1233', 0, 1))
    messages.append(messaging.register_operation('scvalencia', 'Coca', '1233', 1, 0))
    messages.append(messaging.register_operation('scvalencia', 'Coca', '1233', 1, 1))
    messages.append(messaging.ring('jcbages', 'scvalencia', 'Coca'))
    for message in messages:
        swap_twitter.post(message)
    
    swap_tweets = swap_twitter.get_data(HASH_TAG, 100)
    for swap_tweet in swap_tweets:
        print swap_tweet


if __name__ == '__main__':
    example()