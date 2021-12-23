from flask import Flask, request
from time import time

from utils.db_tools import IntegrityError, get_connection as getcon
from utils.security_tools import get_auth_token
from utils.handlers import preflight_request_handler


app = Flask(__name__)


@app.route('/')
def index():
    return "Walking Health"


@app.route('/user/register', methods=['POST', 'OPTIONS'])
@preflight_request_handler
def register():
    data = request.json
    try:
        password = data["password"]
        if password is None or not password:
            return {"code": 400, "message": "Empty password",
                    "result": {"isDoctor": None, "AuthToken": None, "stepLength": None}}
        login = data["login"]
        fullname = data["fullname"]
        doctor_id = data["doctorId"]
        step_length = data["stepLength"]
    except (TypeError, KeyError):
        return {"code": 400, "message": "Incorrect request",
                "result": {"isDoctor": None, "AuthToken": None, "stepLength": None}}
    else:
        is_doctor = True if doctor_id is None else False
        con = getcon()
        cur = con.cursor()
        try:
            token = get_auth_token()
            cur.execute("INSERT INTO users (login, password, fullname, doctorId, stepLength, token) VALUES (?, ?, ?, ?, ?, ?)",
                        (login, password, fullname, doctor_id, step_length, token))
        except IntegrityError as error:
            return {"code": 409, "message": str(error),
                    "result": {"isDoctor": is_doctor, "AuthToken": None, "stepLength": step_length}}
        else:
            con.commit()
            return {"code": 200, "message": "User successfully registered",
                    "result": {"isDoctor": is_doctor, "AuthToken": token, "stepLength": step_length}}
        finally:
            con.close()


@app.route('/user/login', methods=['POST', 'OPTIONS'])
@preflight_request_handler
def log_in():
    data = request.json
    try:
        password = data["password"]
        if password is None or not password:
            return {"code": 400, "message": "Empty password",
                    "result": {"isDoctor": None, "AuthToken": None, "stepLength": None}}
        login = data["login"]
    except (TypeError, KeyError):
        return {"code": 400, "message": "Incorrect request", "result": {"isDoctor": None, "AuthToken": None}}
    else:
        con = getcon()
        cur = con.cursor()
        cur.execute("SELECT password, doctorId, stepLength FROM users WHERE login=?", (login,))
        fetched_data = cur.fetchone()
        try:
            actual_password = fetched_data["password"]
        except TypeError:
            return {"code": 404, "message": "There is no user with such login",
                    "result": {"isDoctor": None, "AuthToken": None, "stepLength": None}}
        else:
            is_doctor = True if fetched_data["doctorId"] is None else False
            if password == actual_password:
                token = get_auth_token()
                cur.execute("UPDATE users SET token=? WHERE login=?", (token, login))
                con.commit()
                return {"code": 200, "message": "Success",
                        "result": {"isDoctor": is_doctor, "AuthToken": token, "stepLength": fetched_data["stepLength"]}}
            else:
                return {"code": 403, "message": "Incorrect password",
                        "result": {"isDoctor": None, "AuthToken": None, "stepLength": None}}
        finally:
            con.close()


@app.route('/user/login/google', methods=['POST', 'OPTIONS'])
@preflight_request_handler
def log_in_google():
    data = request.json
    try:
        email = data["email"]
        fullname = data["fullname"]
    except KeyError:
        return {"code": 400, "message": "Incorrect request"}
    else:
        con = getcon()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE login=?", (email,))
        token = get_auth_token()
        if cur.fetchone() is None:
            cur.execute("INSERT INTO users (login, fullname, token) VALUES (?, ?, ?)", (email, fullname, token))
        else:
            cur.execute(f"UPDATE users SET token=? WHERE login=?", (token, email))
        con.commit()
        con.close()
        return {"code": 200, "message": "Success", "AuthToken": token}


@app.route('/user/getData', methods=['GET', 'OPTIONS'])
@preflight_request_handler
def get_user_data():
    try:
        current_user_id = int(request.headers["CurrentUserId"])
        auth_token = request.headers["AuthToken"]
        id = int(request.args["id"])
    except KeyError:
        return {"code": 400, "message": "Incorrect request"}
    else:
        con = getcon()
        cur = con.cursor()
        cur.execute("SELECT token FROM users WHERE id=?", (current_user_id,))
        try:
            token = cur.fetchone()["token"]
        except TypeError:
            return {"code": 404, "message": "Current user not found"}
        else:
            if auth_token != token:
                return {"code": 403, "message": "Wrong AuthToken"}
            cur.execute("SELECT fullname, doctorId, stepLength FROM users WHERE id=?", (id,))
            user = cur.fetchone()
            try:
                user_fullname = user["fullname"]
                user_doctor_id = user["doctorId"]
            except TypeError:
                return {"code": 404, "message": "Queried user not found"}
            else:
                if current_user_id in (id, user_doctor_id):
                    result = {"id": id, "fullname": user_fullname}
                    if user_doctor_id is None:
                        result["isDoctor"] = True
                        cur.execute("SELECT id, fullname FROM users WHERE doctorId=?", (id,))
                        result["patients"] = list(map(dict, cur.fetchall()))
                    else:
                        result["isDoctor"] = False
                        cur.execute("SELECT id, fullname FROM users WHERE id=?", (user_doctor_id,))
                        result["doctor"] = dict(cur.fetchone())
                        result["stepLength"] = user["stepLength"]
                    return {"code": 200, "message": "Success", "result": result}
                else:
                    return {"code": 403, "message": "Current user has no access to the queried user"}
        finally:
            con.close()


@app.route('/medical/getDoctors', methods=['GET', 'OPTIONS'])
@preflight_request_handler
def get_doctors():
    con = getcon()
    cur = con.cursor()
    cur.execute("SELECT id, fullname FROM users WHERE doctorId IS NULL")
    doctors = list(map(dict, cur.fetchall()))
    con.close()
    return {"code": 200, "message": "OK", "result": doctors}


@app.route('/medical/getMessages', methods=['GET', 'OPTIONS'])
@preflight_request_handler
def get_messages():
    try:
        current_user_id = int(request.headers["CurrentUserId"])
        auth_token = request.headers["AuthToken"]
        patient_id = int(request.args["PatientId"])
    except KeyError:
        return {"code": 400, "message": "Incorrect request"}
    else:
        con = getcon()
        cur = con.cursor()
        cur.execute("SELECT fullname, token FROM users WHERE id=?", (current_user_id,))
        current_user = cur.fetchone()
        try:
            current_user_fullname = current_user["fullname"]
            token = current_user["token"]
        except TypeError:
            return {"code": 404, "message": "Current user not found"}
        else:
            if auth_token != token:
                return {"code": 403, "message": "Wrong AuthToken"}
            cur.execute("SELECT doctorId FROM users WHERE id=?", (patient_id,))
            try:
                patient_doctor_id = cur.fetchone()["doctorId"]
            except TypeError:
                return {"code": 404, "message": "Queried user not found"}
            else:
                if patient_doctor_id is None:
                    return {"code": 403, "message": "Queried user is not a patient"}
                else:
                    if current_user_id != patient_id:
                        if current_user_id != patient_doctor_id:
                            return {"code": 403, "message": "Current user has no access to the queried user"}
                    cur.execute("SELECT doctorId as id, message, timestamp FROM messages WHERE patientId=?", (patient_id,))
                    messages = list(map(dict, cur.fetchall()))
                    return {"code": 200, "message": "Success",
                            "result": {"doctorFullname": current_user_fullname, "messages": messages}}
        finally:
            con.close()


@app.route('/medical/sendMessage', methods=['POST', 'OPTIONS'])
@preflight_request_handler
def send_message():
    try:
        current_user_id = int(request.headers["CurrentUserId"])
        auth_token = request.headers["AuthToken"]
        patient_id = int(request.json["PatientId"])
        message = request.json["message"]
    except (KeyError, TypeError):
        return {"code": 400, "message": "Incorrect request"}
    else:
        con = getcon()
        cur = con.cursor()
        cur.execute("SELECT doctorId, token FROM users WHERE id=?", (current_user_id,))
        current_user = cur.fetchone()
        try:
            token = current_user["token"]
            current_user_doctor_id = current_user["doctorId"]
        except TypeError:
            return {"code": 404, "message": "Current user not found"}
        else:
            if auth_token != token:
                return {"code": 403, "message": "Wrong AuthToken"}
            if current_user_doctor_id is None:
                cur.execute("SELECT doctorId FROM users WHERE id=?", (patient_id,))
                try:
                    patient_doctor_id = cur.fetchone()["doctorId"]
                except TypeError:
                    return {"code": 404, "message": "Queried user not found"}
                else:
                    if patient_doctor_id == current_user_id:
                        timestamp = int(time())
                        cur.execute(
                            "INSERT INTO messages (doctorId, patientId, message, timestamp) VALUES (?, ?, ?, ?)",
                            (current_user_id, patient_id, message, timestamp))
                        con.commit()
                        return {"code": 200, "message": "Success", "result": {"id": patient_id,
                                                                              "message": message,
                                                                              "timestamp": timestamp}}
                    else:
                        return {"code": 403, "message": "Current user has no access to the queried user"}
            else:
                return {"code": 403, "message": "Current user is not a doctor"}
        finally:
            con.close()


@app.route('/medical/getData', methods=['GET', 'OPTIONS'])
@preflight_request_handler
def get_medical_data():
    try:
        current_user_id = int(request.headers["CurrentUserId"])
        auth_token = request.headers["AuthToken"]
        patient_id = int(request.args["PatientId"])
        date = request.args["date"]
    except KeyError:
        return {"code": 400, "message": "Incorrect request"}
    else:
        con = getcon()
        cur = con.cursor()
        cur.execute("SELECT token FROM users WHERE id=?", (current_user_id,))
        try:
            token = cur.fetchone()["token"]
        except TypeError:
            return {"code": 404, "message": "Current user not found"}
        else:
            if auth_token != token:
                return {"code": 403, "message": "Wrong AuthToken"}
            cur.execute(f"SELECT fullname, doctorId FROM users WHERE id=?", (patient_id,))
            patient = cur.fetchone()
            try:
                patient_fullname = patient["fullname"]
                patient_doctor_id = patient["doctorId"]
            except TypeError:
                return {"code": 404, "message": "Queried user not found"}
            else:
                if current_user_id in (patient_id, patient_doctor_id):
                    cur.execute("SELECT timestamp, acceleration, distance, speed FROM data WHERE date=? AND id=?",
                                (date, patient_id))
                    data = cur.fetchall()
                    if data:
                        return {"code": 200, "message": "Success",
                                "result": {"patientFullname": patient_fullname, "date": date,
                                           "data": list(map(dict, data))}}
                    else:
                        return {"code": 204, "message": "No data",
                                "result": {"patientFullname": patient_fullname, "date": date, "data": []}}
                else:
                    return {"code": 403, "message": "Current user has no access to the queried user"}
        finally:
            con.close()


@app.route('/medical/sendData', methods=['POST', 'OPTIONS'])
@preflight_request_handler
def send_medical_data():
    try:
        current_user_id = int(request.headers["CurrentUserId"])
        auth_token = request.headers["AuthToken"]
        date = request.json["date"]
        data = request.json["data"]
    except (KeyError, TypeError):
        return {"code": 400, "message": "Incorrect request"}
    else:
        con = getcon()
        cur = con.cursor()
        cur.execute("SELECT token FROM users WHERE id=?", (current_user_id,))
        try:
            token = cur.fetchone()["token"]
        except TypeError:
            return {"code": 404, "message": "Current user not found"}
        else:
            if auth_token != token:
                return {"code": 403, "message": "Wrong AuthToken"}
            try:
                for m in data:
                    cur.execute(
                        "INSERT INTO data (date, id, timestamp, acceleration, distance, speed) VALUES (?, ?, ?, ?, ?, ?)",
                        (date, current_user_id, m["timestamp"], m["acceleration"], m["distance"], m["speed"]))
            except IntegrityError as error:
                return {"code": 409, "message": str(error)}
            else:
                con.commit()
                return {"code": 200, "message": "Success"}
        finally:
            con.close()


@app.route('/medical/getDates', methods=['GET', 'OPTIONS'])
@preflight_request_handler
def get_dates():
    try:
        auth_token = request.headers["AuthToken"]
        patient_id = int(request.args["PatientId"])
    except KeyError:
        return {"code": 400, "message": "Incorrect request"}
    else:
        con = getcon()
        cur = con.cursor()
        cur.execute("SELECT token, doctorId FROM users WHERE id=?", (patient_id,))
        patient = cur.fetchone()
        try:
            token = patient["token"]
            patient_doctor_id = patient["doctorId"]
        except TypeError:
            return {"code": 404, "message": "Current user not found"}
        else:
            if patient_doctor_id is None:
                return {"code": 400, "message": "Current user is not a patient"}
            if auth_token != token:
                return {"code": 403, "message": "Wrong AuthToken"}
            cur.execute("SELECT date FROM data WHERE id=?", (patient_id,))
            dates = list(set(fetched_data["date"] for fetched_data in cur.fetchall()))
            return {"code": 200, "message": "Success", "result": dates}
        finally:
            con.close()


if __name__ == "__main__":
    app.run(debug=True)
