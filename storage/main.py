"""
Sample Google App Engine application that lists the objects in a Google Cloud
Storage bucket.
"""

import os
import json
import StringIO

import googleapiclient.discovery
import googleapiclient.http
import webapp2


# The bucket that will be used to list objects.
BUCKET_NAME = os.environ.get('STORAGE_NAME')

storage = googleapiclient.discovery.build('storage', 'v1')


class MainPage(webapp2.RequestHandler):
    def upload_object(self, bucket, file_object):
        body = {
            'name': 'storage-api-client-sample-file.txt',
        }
        req = storage.objects().insert(
            bucket=bucket, body=body,
            media_body=googleapiclient.http.MediaIoBaseUpload(
                file_object, 'application/octet-stream'))
        resp = req.execute()
        return resp

    def delete_object(self, bucket, filename):
        req = storage.objects().delete(bucket=bucket, object=filename)
        resp = req.execute()
        return resp

    def get(self):
        string_io_file = StringIO.StringIO('Hola Mundo!')
        self.upload_object(BUCKET_NAME, string_io_file)

        response = storage.objects().list(bucket=BUCKET_NAME).execute()
        self.response.write(
            '<h3>Objects.list raw response:</h3>'
            '<pre>{}</pre>'.format(
                json.dumps(response, sort_keys=True, indent=2)))

        self.delete_object(BUCKET_NAME, 'storage-api-client-sample-file.txt')


app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
