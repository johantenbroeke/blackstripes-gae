#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

#https://developers.google.com/appengine/docs/python/images/usingimages

import webapp2
from PIL import Image
import urllib
import StringIO
import cStringIO

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images

from gen_webbased_preview import WebBasedPreviews


class MainHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload')
        self.response.out.write('<html><body><h1>Blackstripes</h1>')
        self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
        self.response.out.write("""Upload File: <input type="file" name="file"><br> <input type="submit"
            name="submit" value="Submit"> </form></body></html>""")

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        blob_info = upload_files[0]

        blob_reader = blobstore.BlobReader(blob_info.key())
        img = Image.open(blob_reader)
        w,h = img.size
        if w < h:
            offset = int(round((h-w)/2.0))
            img = img.crop((0,offset,w,w+offset))
        else:
            offset = int(round((w-h)/2.0))
            img = img.crop((offset,0,h+offset,h))

        _s = int(200),int(200)
        img = img.resize(_s,Image.BICUBIC)
        
        canvas = Image.new("RGBA",(1060,1060),"black")

        centers = [15,20,25,30,35]
        contrast_settings = [1,2,3,4,5]

        counter = 0
        row_counter = 0

        for c in centers:
            for cs in contrast_settings:

                pr = WebBasedPreviews(img,int(c),int(cs))
                p = pr.getImage()

                canvas.paste(p,(counter*210 + 10,row_counter*210 + 10))
                counter += 1
                if counter%5 == 0:
                    counter = 0
                    row_counter += 1

        output = StringIO.StringIO()
        canvas.save(output, format="png")
        im_data = output.getvalue()
        output.close()

        self.response.headers["Content-Type"] = "image/png"
        self.response.out.write(im_data)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/upload', UploadHandler),
], debug=True)
