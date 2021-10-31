from flask import Flask, Response, request

from utils.db_tools import get_connection as getcon

AUTH_TOKEN = "25fg63278gf3bxzg6fs"

app = Flask(__name__)


@app.route('/')
def index():
    return "Walking Health"


@app.post('/user/register')
def register():
    return Response()


@app.post('/user/login')
def log_in():
    data = request.json
    try:
        login = data["login"]
        password = data["password"]
    except (TypeError, KeyError):
        return {"code": 400, "message": "Incorrect request"}
    else:
        con = getcon()
        cur = con.cursor()
        cur.execute(f"SELECT password FROM users WHERE login=='{login}'")
        try:
            actual_password = cur.fetchone()["password"]
        except TypeError:
            return {"code": 404, "message": "There is no user with such login"}
        else:
            if password == actual_password:
                return {"code": 200, "message": "Success", "result": AUTH_TOKEN}
            else:
                return {"code": 403, "message": "Incorrect password"}
        finally:
            con.close()


@app.get('/user/getData')
def get_data():
    head = request.headers
    if "UserId" in head and "AuthToken" in head:
        if head["AuthToken"] == AUTH_TOKEN:
            user_id = head["UserId"]
            con = getcon()
            cur = con.cursor()
            cur.execute(f"SELECT login, fullname, isDoctor FROM users WHERE id=={user_id}")
            user = cur.fetchone()
            try:
                user_data = dict(user)
            except TypeError:
                return {"code": 404, "message": "Queried user not found"}
            else:
                if user_data["isDoctor"]:
                    cur.execute(f"SELECT login, fullname FROM users AS u INNER JOIN patients AS p ON p.id==u.id WHERE p.doctorId=={user_id}")
                    user_data.update({"patients": list(map(dict, cur.fetchall()))})
                else:
                    cur.execute(f"SELECT login, fullname FROM users AS u INNER JOIN patients AS p ON u.id==p.doctorId WHERE p.id=={user_id}")
                    user_data.update({"doctor": dict(cur.fetchone())})
                return {"code": 200, "message": "Queried user found successfully", "result": user_data}
            finally:
                con.close()
        else:
            return {"code": 403, "message": "Wrong AuthToken"}
    else:
        return {"code": 400, "message": "Incorrect request"}


@app.get('/medical/getDoctors')
def get_doctors():
    con = getcon()
    cur = con.cursor()
    cur.execute("SELECT login, fullname FROM users WHERE isDoctor")
    doctors = list(map(dict, cur.fetchall()))
    con.close()
    return {"code": 200, "message": "OK", "result": doctors}


@app.get('/medical/getMessages')
def get_messages():
    return Response()


@app.post('/medical/sendMessage')
def send_message():
    return Response()
