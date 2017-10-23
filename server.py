#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import re


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        auth_code = re.match(r"\/\?code=(.+)", self.path)[1]
        self.server.auth_code = auth_code

        if auth_code:
            # Send message back to client
            message = "Authenticated!<br>(you can close this window now)"
            # Write content as utf-8 data
            self.wfile.write(bytes(message, "utf8"))
        else:
            return


def fetch_auth_code():
    server_address = ('127.0.0.1', 51350)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    httpd.handle_request()

    return httpd.auth_code
