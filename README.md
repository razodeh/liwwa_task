# TinyHR

## Step to run the app

1. `python -m virtualenv venv` to create app's virtual env.
2. `source venv/bin/activate` to activate app's virtual env.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to a new `.env` file with the proper values.
4. Migrate database using `flask db upgrade`.
5. Create an admin User using `flask create_admin`
6. Run the app with `flask run`

> You need to set the proper values for `.env` file, 
> otherwise it will not work properly.


> I implemented a simple authorization and authentication
> mechanism, instead of sending `X-ADMIN=1` header.

## APIs

- POST `/auth/login/` _(To Login with User Credentials)_
 
**Request Body**   
```
{
  "email": "USER_EMAIL",
  "password": "USER_PASSWORD"
}
```

**Response Body**
```
{
  "token": "JWT_TOKEN"
}
```

------------------------------------------------------

- POST `/auth/register/` _(To register a new user "Not Admin")_

**Request Body**   
```
{
  "email": "USER_EMAIL",
  "password": "USER_PASS",
  "first_name": "USER_FIRST_NAME",
  "last_name": "USER_LAST_NAME",
  "profile": {
    "date_of_birth": "USER_DATE_OF_BIRTH(YYYY-MM-DD)",
    "years_of_experience": "YEARS_OF_EXPERIENCE",
    "department": "DEPARTMENT(it, hr, finance)"
  }
}
```

**Response Body**
```
{
  "token": "USER_JWT_TOKEN"
}
```

------------------------------------------------------

- GET `/candidates/` _(To list all candidates "Non-Admin users")_
- Headers 
    - "Authorization: Bearer JWT_TOKEN"

> only admins can access this endpoint,
> it has query parameter for pagination,
> `page` and `per_page`.

**Response Body**
```
[
  {
    "full_name": "USER_FULLNAME",
    "years_of_experience": "USER_EXPERIENCE",
    "department": "USER_DEPARTMENT",
    "date_of_birth": "USER_DATE_OF_BIRTH"
  },
  ...
]
```

------------------------------------------------------

- GET `/candidates/<id>/` _(To get specific candidate details)_
- Headers 
    - "Authorization: Bearer JWT_TOKEN"

> only admins can access this endpoint.

**Response Body**
```
{
    "full_name": "USER_FULLNAME",
    "years_of_experience": "USER_EXPERIENCE",
    "department": "USER_DEPARTMENT",
    "date_of_birth": "USER_DATE_OF_BIRTH"
}
```

------------------------------------------------------

- GET `/candidates/<id>/resume/` _(To get specific candidate resume)_
- Headers 
    - "Authorization: Bearer JWT_TOKEN"

> only admins can access this endpoint.

Response will be a **PDF** file

------------------------------------------------------

- POST `/resume/` _(To upload candidate's resume)_

- Headers
    - "Authorization: Bearer JWT_TOKEN"
    - "Content-Type: multipart/form-data; boundary=\_\_TINYHR\_\_"

**Request**

```
{
    "resume": "RESUME_FILE_DATA"
}
```
