from flask import Flask, request
from time import time

from utils.db_tools import IntegrityError, get_connection as getcon
from utils.security_tools import get_auth_token
from utils.http_tools import http_response as response

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
        return response({"code": 400, "message": "Incorrect request", "result": {"isDoctor": None, "AuthToken": None}})
    else:
        is_doctor = True if doctor_login is None else False
        con = getcon()
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO users (login, password, fullname, doctorLogin) VALUES (?, ?, ?, ?)",
                        (login, password, fullname, doctor_login))
        except IntegrityError:
            return response({"code": 403, "message": "User already exists",
                             "result": {"isDoctor": is_doctor, "AuthToken": None}})
        else:
            con.commit()
            return response({"code": 200, "message": "User successfully registered",
                             "result": {"isDoctor": is_doctor, "AuthToken": AUTH_TOKEN}})
        finally:
            con.close()


@app.post('/user/login')
def log_in():
    data = request.json
    try:
        login = data["login"]
        password = data["password"]
    except (TypeError, KeyError):
        return response({"code": 400, "message": "Incorrect request", "result": {"isDoctor": None, "AuthToken": None}})
    else:
        con = getcon()
        cur = con.cursor()
        cur.execute(f"SELECT password, doctorLogin FROM users WHERE login='{login}'")
        fetched_data = cur.fetchone()
        try:
            actual_password = fetched_data["password"]
        except TypeError:
            return response({"code": 404, "message": "There is no user with such login",
                             "result": {"isDoctor": None, "AuthToken": None}})
        else:
            is_doctor = True if fetched_data["doctorLogin"] is None else False
            if password == actual_password:
                return response({"code": 200, "message": "Success",
                                 "result": {"isDoctor": is_doctor, "AuthToken": AUTH_TOKEN}})
            else:
                return response({"code": 403, "message": "Incorrect password",
                                 "result": {"isDoctor": is_doctor, "AuthToken": None}})
        finally:
            con.close()


@app.get('/user/getData')
def get_data():
    head = request.headers
    args = request.args
    if "CurrentUserLogin" in head and "AuthToken" in head and "login" in args:
        if head["AuthToken"] == AUTH_TOKEN:
            current_user_login = head["CurrentUserLogin"]
            login = args["login"]
            con = getcon()
            cur = con.cursor()
            cur.execute(f"SELECT fullname, doctorLogin FROM users WHERE login='{current_user_login}'")
            current_user = cur.fetchone()
            try:
                current_user_fullname = current_user["fullname"]
            except TypeError:
                return response({"code": 404, "message": "Current user not found"})
            else:
                if current_user_login == login:
                    result = {"login": current_user_login,
                              "fullname": current_user_fullname,
                              "doctor": None,
                              "patients": []}
                    user_doctor_login = current_user["doctorLogin"]
                    if user_doctor_login is None:
                        result["isDoctor"] = True
                        cur.execute(f"SELECT login, fullname FROM users WHERE doctorLogin='{current_user_login}'")
                        result["patients"] = list(map(dict, cur.fetchall()))
                    else:
                        result["isDoctor"] = False
                        cur.execute(f"SELECT login, fullname FROM users WHERE login='{user_doctor_login}'")
                        result["doctor"] = dict(cur.fetchone())
                    return response({"code": 200, "message": "Success", "result": result})
                else:
                    cur.execute(f"SELECT fullname, doctorLogin FROM users WHERE login='{login}'")
                    user = cur.fetchone()
                    if user is None:
                        return response({"code": 404, "message": "Queried user not found"})
                    elif current_user_login == user["doctorLogin"]:
                        result = {"login": login,
                                  "fullname": user["fullname"],
                                  "isDoctor": False,
                                  "doctor": {"login": current_user_login, "fullname": current_user_fullname},
                                  "patients": []}
                        return response({"code": 200, "message": "Success", "result": result})
                    else:
                        return response({"code": 403, "message": "Current user has no access to the queried user"})
            finally:
                con.close()
        else:
            return response({"code": 403, "message": "Wrong AuthToken"})
    else:
        return response({"code": 400, "message": "Incorrect request"})


@app.get('/medical/getDoctors')
def get_doctors():
    con = getcon()
    cur = con.cursor()
    cur.execute("SELECT login, fullname FROM users WHERE doctorLogin IS NULL")
    doctors = list(map(dict, cur.fetchall()))
    con.close()
    return response({"code": 200, "message": "OK", "result": doctors})


@app.get('/medical/getMessages')
def get_messages():
    try:
        current_user_login = request.headers["CurrentUserLogin"]
        auth_token = request.headers["AuthToken"]
        patient_login = request.args["PatientLogin"]
    except KeyError:
        return response({"code": 400, "message": "Incorrect request"})
    else:
        if auth_token == AUTH_TOKEN:
            con = getcon()
            cur = con.cursor()
            cur.execute(f"""SELECT patientLogin as login, message, timestamp FROM messages
                            WHERE doctorLogin='{current_user_login}' AND patientLogin='{patient_login}'""")
            messages = list(map(dict, cur.fetchall()))
            con.close()
            return response({"code": 200, "message": "Success", "result": messages})
        else:
            return response({"code": 403, "message": "Wrong AuthToken"})


@app.post('/medical/sendMessage')
def send_message():
    head = request.headers
    body = request.json
    if "CurrentUserLogin" in head and "AuthToken" in head and "PatientLogin" in body and "message" in body:
        if head["AuthToken"] == AUTH_TOKEN:
            current_user_login = head["CurrentUserLogin"]
            patient_login = body["PatientLogin"]
            message = body["message"]
            con = getcon()
            cur = con.cursor()
            cur.execute(f"SELECT doctorLogin FROM users WHERE login='{current_user_login}'")
            try:
                current_user_doctor_login = cur.fetchone()["doctorLogin"]
            except TypeError:
                return response({"code": 404, "message": "Current user not found"})
            else:
                if current_user_doctor_login is None:
                    cur.execute(f"SELECT doctorLogin FROM users WHERE login='{patient_login}'")
                    try:
                        patient_doctor_login = cur.fetchone()["doctorLogin"]
                    except TypeError:
                        return response({"code": 404, "message": "Queried user not found"})
                    else:
                        if patient_doctor_login == current_user_login:
                            timestamp = int(time())
                            cur.execute("INSERT INTO messages (doctorLogin, patientLogin, message, timestamp) VALUES (?, ?, ?, ?)",
                                        (current_user_login, patient_login, message, timestamp))
                            con.commit()
                            return response({"code": 200, "message": "Success", "result": {"login": patient_login,
                                                                                           "message": message,
                                                                                           "timestamp": timestamp}})
                        else:
                            return response({"code": 403, "message": "Current user has no access to the queried user"})
                else:
                    return response({"code": 403, "message": "Current user is not a doctor"})
            finally:
                con.close()
        else:
            return response({"code": 403, "message": "Wrong AuthToken"})
    else:
        return response({"code": 400, "message": "Incorrect request"})
