import subprocess
import sys

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"Use port redirect"]