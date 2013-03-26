from bottle import run

@route('/')
def index():
    return "Hello world"

run(host='localhost', port=8080)
