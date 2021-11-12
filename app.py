from flask import Flask, Response, request

from utils.db_tools import IntegrityError, get_connection as getcon
from utils.security_tools import get_auth_token

AUTH_TOKEN = get_auth_token()

app = Flask(__name__)


@app.route('/')
def index():
    return "Walking Health"


@app.post('/user/register')
def register():
    data = request.json
    try:
        login = data["login"]
        password = data["password"]
        fullname = data["fullname"]
        doctor_login = data["doctorLogin"]
    except (TypeError, KeyError):
        return {"code": 400, "message": "Incorrect request", "isDoctor": None, "result": None}
    else:
        con = getcon()
        cur = con.cursor()
        try:
            cur.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)", (login, password, fullname, doctor_login))
        except IntegrityError:
            return {"code": 403, "message": "User already exists", "isDoctor": None, "result": None}
        else:
            con.commit()
            return {"code": 200, "message": "User successfully registered",
                    "isDoctor": True if doctor_login is None else False, "result": AUTH_TOKEN}
        finally:
            con.close()


@app.post('/user/login')
def log_in():
    data = request.json
    try:
        login = data["login"]
        password = data["password"]
    except (TypeError, KeyError):
        return {"code": 400, "message": "Incorrect request", "isDoctor": None, "result": None}
    else:
        con = getcon()
        cur = con.cursor()
        cur.execute(f"SELECT password, doctorLogin FROM users WHERE login=='{login}'")
        fetched_data = cur.fetchone()
        try:
            actual_password = fetched_data["password"]
        except TypeError:
            return {"code": 404, "message": "There is no user with such login", "isDoctor": None, "result": None}
        else:
            is_doctor = True if fetched_data["doctorLogin"] is None else False
            if password == actual_password:
                return {"code": 200, "message": "Success", "isDoctor": is_doctor, "result": AUTH_TOKEN}
            else:
                return {"code": 403, "message": "Incorrect password", "isDoctor": is_doctor, "result": None}
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
    cur.execute("SELECT login, fullname FROM users WHERE doctorLogin IS NULL")
    doctors = list(map(dict, cur.fetchall()))
    con.close()
    return {"code": 200, "message": "OK", "result": doctors}


@app.get('/medical/getMessages')
def get_messages():
    return Response()


@app.post('/medical/sendMessage')
def send_message():
    return Response()
