# API methods
> ### POST user/register

**Description:**\
Method used to register a user in the system.

**Query parameters:**\
None

**Custom headers:**\
None

**Request body:**
```json lines
{
  "login": string, // user login
  "password": string, // user password
  "fullname": string, // user fullname
  "doctorId": integer|null, // user's doctor id (null if user is a doctor)
  "stepLength": float|null // user's step length (null if user is a doctor)
}
```

**Response body:**
```json lines
{
  "code": integer, // response status code
  "message": string, // response message
  "result": {
    "isDoctor": boolean, // true if the user is a doctor, otherwise false
    "AuthToken": string, // 32-byte authentication token
    "stepLength": float|null // the user's step length (null if user is a doctor)
  }
}
```
**Example:**\
Request:
```http request
POST http://localhost:5000/user/register
Content-Type: application/json

{
  "login": "test_doctor",
  "password": "12345678",
  "fullname": "Doctor Doctorov",
  "doctorId": null,
  "stepLength": null
}
```
Response:
```
POST http://localhost:5000/user/register

HTTP/1.0 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 166
Server: Werkzeug/2.0.2 Python/3.10.0
Date: Thu, 23 Dec 2021 19:25:40 GMT

{
  "code": 200,
  "message": "User successfully registered",
  "result": {
    "AuthToken": "pL-wr5nM8Qlc-HsBaxlJO3bo8FPOrdvLiJZPAymnK94",
    "isDoctor": true,
    "stepLength": null
  }
}
```
> ### POST user/login

**Description:**\
Method used for a user to log in to the system using their login and password.

**Query parameters:**\
None

**Custom headers:**\
None

**Request body:**
```json lines
{
  "login": string, // user login
  "password": string, // user password
}
```
**Response body:**
```json lines
{
  "code": integer, // response status code
  "message": string, // response message
  "result": {
    "isDoctor": boolean, // true if the user is a doctor, otherwise false
    "AuthToken": string, // 32-byte authentication token
    "stepLength": float|null // the user's step length (null if user is a doctor)
  }
}
```
**Example:**\
Request:
```http request
POST http://localhost:5000/user/login
Content-Type: application/json

{
  "login": "test_doctor",
  "password": "12345678"
}
```
Response:
```
POST http://localhost:5000/user/login

HTTP/1.0 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 145
Server: Werkzeug/2.0.2 Python/3.10.0
Date: Thu, 23 Dec 2021 19:40:59 GMT

{
  "code": 200,
  "message": "Success",
  "result": {
    "AuthToken": "IWcbyQ3mtxJtesFctysFsHL5SQwEP22QQ8bi-XXfvzI",
    "isDoctor": true,
    "stepLength": null
  }
}
```
> ### POST user/login/google

**Description:**\
Method used for a doctor to log in (or register) to the system using their Google account.

**Query parameters:**\
None

**Custom headers:**\
None

**Request body:**
```json lines
{
  "email": string, // user email (retrieved on the front end)
  "fullname": string, // user fullname
}
```
**Response body:**
```json lines
{
  "code": integer, // response status code
  "message": string, // response message
  "AuthToken": string // 32-byte authentication token
}
```
**Example:**\
Request:
```http request
POST http://localhost:5000/user/login/google
Content-Type: application/json

{
  "email": "mr_doctor@clinic.com",
  "fullname": "Google Doctor"
}
```
Response:
```
POST http://localhost:5000/user/login/google

HTTP/1.0 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 95
Server: Werkzeug/2.0.2 Python/3.10.0
Date: Thu, 23 Dec 2021 19:56:48 GMT

{
  "AuthToken": "ltIIGCrcOAAZhRQCd5QcPVqcEzjcETYKMg-0YKDItfs",
  "code": 200,
  "message": "Success"
}
```
> ### GET user/getData

**Description:**\
Method used to retrieve user data

**Query parameters:**
```json lines
id //id of the user whose data is retrieved
```
**Custom headers:**
```json lines
CurrentUserId //id of the current user who wants to access the user's data
AuthToken //current user's authentication token
```

**Request body:**\
None

**Response body:**
```json lines
{
  "code": integer, // response status code
  "message": string, // response message
  "result":
  {
    "id": integer, //id of the user whose data is retrieved
    "fullname": string, //fullname of the user whose data is retrieved
    "isDoctor": boolean, // true if the user is a doctor, otherwise false
    "patients": [ //list of user's patients (not present if user is a patient)
      {
        "id": integer, //id of the patient
        "fullname": string //fullname of the patient
      }
    ],
    "doctor": { //user's doctor (not present if user is a doctor)
      "id": integer, //id of the doctor
      "fullname": string //fullname of the doctor
    },
    "stepLength": float //user's step length (not present if user is a doctor)
  }
}
```
**Example:**
Request:
```http request
GET http://localhost:5000/user/getData?id=3
CurrentUserId: 1
AuthToken: IWcbyQ3mtxJtesFctysFsHL5SQwEP22QQ8bi-XXfvzI
```
Response:
```
GET http://localhost:5000/user/getData?id=3

HTTP/1.0 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 180
Server: Werkzeug/2.0.2 Python/3.10.0
Date: Thu, 23 Dec 2021 20:22:16 GMT

{
  "code": 200,
  "message": "Success",
  "result": {
    "doctor": {
      "fullname": "Doctor Doctorov",
      "id": 1
    },
    "fullname": "Patient Patientsky",
    "id": 3,
    "isDoctor": false,
    "stepLength": 0.5
  }
}
```
> ### GET medical/getDoctors

**Description:**\
Method used to list all registered doctors

**Query parameters:**\
None

**Custom headers:**\
None

**Request body:**\
None

**Response body:**
```json lines
{
  "code": integer, // response status code
  "message": string, // response message
  "result":
  [
    { 
      "id": integer, //id of the doctor
      "fullname": string //fullname of the doctor
    }
  ]
}
```
**Example**\
Request:
```http request
GET http://localhost:5000/medical/getDoctors
```
Response:
```
GET http://localhost:5000/medical/getDoctors

HTTP/1.0 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 124
Server: Werkzeug/2.0.2 Python/3.10.0
Date: Thu, 23 Dec 2021 20:26:03 GMT

{
  "code": 200,
  "message": "OK",
  "result": [
    {
      "fullname": "Doctor Doctorov",
      "id": 1
    },
    {
      "fullname": "Google Doctor",
      "id": 2
    }
  ]
}
```
> ### POST medical/sendMessage

**Description:**\
Method used for a doctor to send a message to their patient

**Query parameters:**\
None

**Custom headers:**
```json lines
CurrentUserId // id of the doctor
AuthToken // current user's authentication token
```
**Request body**
```json lines
{
  "PatientId": integer, // id of the patient to whom the message is sent
  "message": string // text of the message
}
```
**Response body**
```json lines
{
  "code": integer, // response status code
  "message": string, // response message
  "result": {
    "id": integer, // patient's id
    "message": string, // message text
    "timestamp": integer // timestamp of the message
  }
}
```
**Example**\
Request:
```http request
POST http://localhost:5000/medical/sendMessage
Content-Type: application/json
CurrentUserId: 1
AuthToken: IWcbyQ3mtxJtesFctysFsHL5SQwEP22QQ8bi-XXfvzI

{
  "PatientId": 3,
  "message": "Test message text"
}
```
Response:
```
POST http://localhost:5000/medical/sendMessage

HTTP/1.0 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 113
Server: Werkzeug/2.0.2 Python/3.10.0
Date: Thu, 23 Dec 2021 21:09:42 GMT

{
  "code": 200,
  "message": "Success",
  "result": {
    "id": 3,
    "message": "Test message text",
    "timestamp": 1640293782
  }
}
```
> ### GET medical/getMessages

**Description:**\
Method used to list all messages sent to the patient

**Query parameters:**
```json lines
PatientId // id of the patient
```
**Custom headers:**
```json lines
CurrentUserId // id of the current user who wants to access the messages
AuthToken // current user's authentication token
```

**Request body:**\
None

**Response body:**
```json lines
{
  "code": integer, // response status code
  "message": string, // response message
  "result": {
    "doctorFullname": string, // fullname of the patient's doctor
    "messages": [
      {
        "id": integer, // id of the patient's doctor
        "message": string, // message text
        "timestamp": integer // timestamp of the message
      }
    ]
  }
}
```
**Example**\
Request:
```http request
GET http://localhost:5000/medical/getMessages?PatientId=3
CurrentUserId: 1
AuthToken: IWcbyQ3mtxJtesFctysFsHL5SQwEP22QQ8bi-XXfvzI
```
Response:
```
GET http://localhost:5000/medical/getMessages?PatientId=3

HTTP/1.0 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 166
Server: Werkzeug/2.0.2 Python/3.10.0
Date: Thu, 23 Dec 2021 21:18:00 GMT

{
  "code": 200,
  "message": "Success",
  "result": {
    "doctorFullname": "Doctor Doctorov",
    "messages": [
      {
        "id": 1,
        "message": "Test message text",
        "timestamp": 1640293782
      }
    ]
  }
}
```
> ### POST medical/sendData

**Description:**\
Method used to send patient's medical activity on a specific day

**Query parameters:**\
None

**Custom headers:**
```json lines
CurrentUserId // id of the current user who wants to access the medical data
AuthToken // current user's authentication token
```

**Request body:**\
```json lines
{
  "date": string, // date of the activity in dd.mm.yyyy format
  "data": [
    {
      "timestamp": integer, // record timestamp (data is recorded in 5 min intervals)
      "acceleration": float, // average acceleration in 5 min
      "distance": float, // distance traveled in 5 min
      "speed": float // average speed in 5 min
      }
  ]
}
```
**Response body:**
```json lines
{
  "code": integer, // response status code
  "message": string, // response message
}
```
**Example**\
Request:
```http request
POST http://localhost:5000/medical/sendData
Content-Type: application/json
CurrentUserId: 3
AuthToken: fv888XMLDMc5iqibqGFu3yQi2ct29rLK_yDGIp5D1ZU

{
  "date": "23.12.2021",
  "data": [
    {
      "timestamp": 1640293482,
      "acceleration": 1.23,
      "distance": 103.5,
      "speed": 16.802
      },
      {
      "timestamp": 1640293782,
      "acceleration": 1.22,
      "distance": 101.99,
      "speed": 11.6
      }
  ]
}
```
Response:
```
POST http://localhost:5000/medical/sendData

HTTP/1.0 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 35
Server: Werkzeug/2.0.2 Python/3.10.0
Date: Thu, 23 Dec 2021 21:57:29 GMT

{
  "code": 200,
  "message": "Success"
}
```
> ### GET medical/getData

**Description:**\
Method used to retrieve patient's medical activity on a specific day

**Query parameters:**
```json lines
PatientId // id of the patient
date // activity date
```
**Custom headers:**
```json lines
CurrentUserId // id of the current user who wants to access the data
AuthToken // current user's authentication token
```

**Request body:**\
None

**Response body:**
```json lines
{
  "code": integer, // response status code
  "message": string, // response message
  "result": {
    "patientFullname": string, // patient's fullname
    "date": string, // date of the activity in dd.mm.yyyy format
    "data": [
      {
        "timestamp": integer, // record timestamp (data is recorded in 5 min intervals)
        "acceleration": float, // average acceleration in 5 min
        "distance": float, // distance traveled in 5 min
        "speed": float // average speed in 5 min
      }
    ]
  }
}
```
**Example**\
Request:
```http request
GET http://localhost:5000/medical/getData?PatientId=3&date=23.12.2021
CurrentUserId: 1
AuthToken: IWcbyQ3mtxJtesFctysFsHL5SQwEP22QQ8bi-XXfvzI
```
Response:
```
GET http://localhost:5000/medical/getData?PatientId=3&date=23.12.2021

HTTP/1.0 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 289
Server: Werkzeug/2.0.2 Python/3.10.0
Date: Thu, 23 Dec 2021 22:01:18 GMT

{
  "code": 200,
  "message": "Success",
  "result": {
    "data": [
      {
        "acceleration": 1.23,
        "distance": 103.5,
        "speed": 16.802,
        "timestamp": 1640293482
      },
      {
        "acceleration": 1.22,
        "distance": 101.99,
        "speed": 11.6,
        "timestamp": 1640293782
      }
    ],
    "date": "23.12.2021",
    "patientFullname": "Patient Patientsky"
  }
}
```
> ### GET medical/getDates

**Description:**\
Method used to retrieve dates on which the patient has activity recorded

**Query parameters:**
```json lines
PatientId // id of the patient whose activity dates are retrieved
```

**Custom headers:**
```json lines
AuthToken // patient's authentication token
```

**Request body:**\
None

**Response body:**
```json lines
{
  "code": integer, // response status code
  "message": string, // response message
  "result": [
    string // date in dd.mm.yyyy format
  ]
}
```
**Example**\
Request:
```http request
GET http://localhost:5000/medical/getDates?PatientId=3
AuthToken: fv888XMLDMc5iqibqGFu3yQi2ct29rLK_yDGIp5D1ZU
```
Response:
```
GET http://localhost:5000/medical/getDates?PatientId=2

HTTP/1.0 200 OK
Content-Type: application/json
Access-Control-Allow-Origin: *
Content-Length: 61
Server: Werkzeug/2.0.2 Python/3.10.0
Date: Thu, 23 Dec 2021 22:10:31 GMT

{
  "code": 200,
  "message": "Success",
  "result": [
    "23.12.2021"
  ]
}
```
