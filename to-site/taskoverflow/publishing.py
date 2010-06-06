
from twitteroauth import *
from datetime import datetime
import dataLayer

class PublisherApi(TwitterClient):
    
    __public__ = ('callback', 'cleanup', 'login', 'logout', 'publish')   
    
    def __init__(self, service, request, response, consumer_key, consumer_secret,oauth_callback=None, **request_params):
        TwitterClient.__init__(self, service, request, response, consumer_key, consumer_secret, oauth_callback=None, **request_params)
        self.datalayer = dataLayer.DataLayer()

    def publish(self):
        # check twitter authorisation
        access_token = self.get_access_token()
        
        if access_token is None:
            raise TwitterNotAuthorisedError()
            
        tasks = self.datalayer.GetTasks()
        text = ''
        if tasks:
            text = 'There are now %d tasks available' % len(tasks)
        else:
            text = 'There are no new tasks'
        
        now = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
            
        self.post_update(access_token, 'Status :: %s - %s' % (now, text))
        return 'Published'
            
        #
        # put code here to gather the data from the database
        # and formulate the 
        
    def publish_to_email(self):
        #
        s = ''
    	
    def get_data(self):
        return None
    	
    def get_access_token(self):
        key = self.consumer_key
        query = OAuthAccessToken.gql("WHERE consumer_key = :1", key)
        return query.get()
        
    
    