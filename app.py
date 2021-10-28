from flask import Flask, Response


app = Flask(__name__)


@app.route('/')
def index():
    return "Walking Health"


@app.post('/user/register')
def register():
    return Response()


@app.post('/user/login')
def login():
    return Response()


@app.get('/user/getData')
def get_data():
    return Response()


@app.get('/medical/getDoctors')
def get_doctors():
    return Response()


@app.get('/medical/getMessages')
def get_messages():
    return Response()


@app.post('/medical/sendMessage')
def send_message():
    return Response()
