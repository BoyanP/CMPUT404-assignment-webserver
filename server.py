#  coding: utf-8 
import SocketServer
import datetime

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        noSlashFlag = "false" 
        httpCommand = ""
        requestedPage =""
        httpHeader ="HTTP/1.1 "
        mimeType = ""

        for char in self.data:

            if char != "\n":
                httpCommand+=char
            else:
                break

        httpCommandSplit = httpCommand.split()
        requestedPage = httpCommandSplit[1]
        
        if(requestedPage =="/" or requestedPage == "/deep/"):
            requestedPage +="index.html"
        if(requestedPage=="/deep.css" and noSlashFlag == "true"):
            requestedPage = "/deep/deep.cs"
       
        if(requestedPage in ['/index.html','/base.css','/deep/deep.css','/deep/index.html']):
            readFrom = "www"+requestedPage
            fileToRead = open(readFrom, 'r')
            contentToSend = fileToRead.read()
            fileToRead.close()
            mimeType = requestedPage.split('.')[1]
            if(mimeType == "html"):
                mimeType+="; charset=utf-8"
            #print "mimeType : " + mimeType 
            httpHeader += """200 OK
Server: Boyan's bad server
Date:"""+str(datetime.datetime.now())+"""
Content-length:"""+str(len(contentToSend))+"""
Content-Type:text/""" + mimeType + " \r\n\r\n"

        else:
            if (requestedPage == "/deep"):
                #need to redirect
                #otherwise deep.css tries to get served from www/
                #and not www/deep
                contentToSend ="""<html> redirected to <a href=/deep/>here</a></html>"""
                httpHeader = """HTTP/1.1 302 FOUND
Location: /deep/
Content-length: """ + str(len(contentToSend))+"""
Content-type: text/html; charset=utf-8 \r\n\r\n"""
            else:
                contentToSend ="""<html><h2> error: 404  page not found</h3></html>"""
                httpHeader = """HTTP/1.1 404 NOT FOUND
Content-length:"""+str(len(contentToSend))+"""
Content-Type:text/html; charset=utf-8 \r\n\r\n"""

        self.request.sendall(httpHeader  + contentToSend)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
