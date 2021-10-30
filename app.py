from flask import Flask, Response, request, jsonify
from http import HTTPStatus

from db_tools import get_connection as getcon

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
    head = request.headers
    if "UserId" in head and "AuthToken" in head:
        user_id = head["UserId"]
        con = getcon()
        cur = con.cursor()
        cur.execute(f"SELECT login, fullname, isDoctor FROM users WHERE id=={user_id}")
        user = cur.fetchone()
        try:
            user_data = dict(user)
        except TypeError:
            return Response("Queried user not found", status=HTTPStatus.NOT_FOUND)
        else:
            if user_data["isDoctor"]:
                user_data.update({"patients": []})
                cur.execute(f"SELECT login, fullname FROM users AS u INNER JOIN patients AS p WHERE p.id==u.id AND p.doctorId=={user_id}")
                for patient in cur.fetchall():
                    user_data["patients"].append(dict(patient))
            else:
                cur.execute(f"SELECT doctorId FROM patients WHERE id={user_id}")
                user_data.update(dict(cur.fetchone()))
            return jsonify(user_data)
        finally:
            con.close()
    else:
        return Response("Incorrect request", status=HTTPStatus.BAD_REQUEST)


@app.get('/medical/getDoctors')
def get_doctors():
    return Response()


@app.get('/medical/getMessages')
def get_messages():
    return Response()


@app.post('/medical/sendMessage')
def send_message():
    return Response()
