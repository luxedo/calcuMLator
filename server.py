def app(environ, start_response):
    """Simplest possible application object"""

    with open("index.html", "r") as index:
        data = index.read()
    print data

    if environ['PATH_INFO'] is not "/":
        status = '302 Found'
        response_headers = [('Location','/')]
    else:
        status = '200 OK'
        response_headers = [
            ('Content-type','text/html'),
            ('Content-Length', str(len(data)))
        ]
    start_response(status, response_headers)
    return [data]
