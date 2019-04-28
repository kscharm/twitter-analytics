import json
import time
import os
import pandas as pd
import http.client, urllib.request, urllib.parse, urllib.error, base64

from azure.storage.blob import BlockBlobService, PublicAccess
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Variables that contains the user credentials to access Twitter API 
access_token = "<YOUR_ACCESS_TOKEN>"
access_token_secret = "<YOUR_SECRET_ACCESS_TOKEN>"
consumer_key = "<YOUR_CONSUMER_KEY>"
consumer_secret = "<YOUR_CONSUMER_SECRET>"

# Microsoft Azure keys
cognitive_sciences_key = "<YOUR_COGNITIVE_SCIENCES_KEY>"
blob_storage_key = "<YOUR_BLOB_STORAGE_ACCOUNT_KEY>"

filtered_tweets = "filteredTweets.txt"
req = {
    "documents": []
}
MAX_COUNT = 100000
MAX_SIZE = 100000 #50Kb max size
count = 1

# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        global filtered_tweets, req, MAX_COUNT, MAX_SIZE, count
        data = json.loads(data)
        tweet = {}
        if ('lang' in data and 'text' in data and 'id' in data):
            tweet = {
                "language": data["lang"],
                "id": str(count),
                "text": data["text"]
            }
            req["documents"].append(tweet)
        count += 1
        if count % 100 == 0:
            print ('Counter: ', str(count))
            headers = {
                # Request headers
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': cognitive_sciences_key,
            }
            try:
                req_json = json.dumps(req)
                conn = http.client.HTTPSConnection('eastus2.api.cognitive.microsoft.com')
                conn.request("POST", "/text/analytics/v2.0/keyPhrases", req_json, headers)
                response = conn.getresponse()
                data = response.read().decode()
                data = json.loads(data)
                print(data)
                #time.sleep(1)
                with open(filtered_tweets, "a", encoding="utf-8") as t:
                    if ('documents' in data):
                        for doc in data["documents"]:
                            for phrase in doc["keyPhrases"]:
                                t.write(phrase + ",")
                            t.write("\n")
                conn.close()
                req = {
                    "documents": []
                }
                statinfo = os.stat(filtered_tweets)
                if statinfo.st_size > MAX_SIZE:
                    # Upload data to azure
                    self.upload_to_azure()
                    # Remove local file
                    if os.path.exists(filtered_tweets):
                        os.remove(filtered_tweets)
                    else:
                        print("The file does not exist")
                if count >= MAX_COUNT:
                    count = 1
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
        return True

    def on_error(self, status):
        print('Error during streaming:', status)

    def upload_to_azure(self):
        global filtered_tweets
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name='project3twitter', account_key= blob_storage_key)

        # Create a container called 'quickstartblobs'.
        container_name ='project3'
        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
        local_path = os.getcwd()
        full_path_to_file = os.path.join(local_path, filtered_tweets)
        print(full_path_to_file)
        print("\nUploading to Blob storage as blob: " + filtered_tweets)
        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(container_name, filtered_tweets, full_path_to_file)

if __name__ == '__main__':
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(languages=['en'], track=['a'])