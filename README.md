## RESTful API for user authentication


### Stack
- Django
- Django REST Framework
- PyJWT
- SQLite


### Endpoints

*User Registration*
```
Endpoint: /api/register/
Method: POST
Body: {"password": "password", "email": "user@example.com"}
Response: {"id": 1, "email": "user@example.com"}
```

*Authentication (Obtaining Access and Refresh Token)*
```
Endpoint: /api/login/
Method: POST
Body: {"email": "user@example.com", "password": "password"}
Response: {"access_token": "eyJhbGciOiJIUzI1NiIsInR5...", "refresh_token": "d952527b-caef-452c-8c93-1100214f82e5"}
```

*Access Token Refresh*
```
Endpoint: /api/refresh/
Method: POST
Body: {"refresh_token": "d952527b-caef-452c-8c93-1100214f82e5"}
Response: {"access_token": "eyJhbGciOiJIUzI1NiIsIn...", "refresh_token": "eb0464c2-ed6e-4346-a709-042c33946154"}
```

*Logout (Invalidating Refresh Token)*
```
Endpoint: /api/logout/
Method: POST
Body: {"refresh_token": "eb0464c2-ed6e-4346-a709-042c33946154"}
Response: {"success": "User logged out."}
```

*Retrieving Personal Information*
```
Endpoint: /api/me/
Method: GET
Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiZXhhbXBsZVVzZXIiLCJleHAiOjE3MTIxNDYxNDd9.zKobBlRuOiJSxCmi-iYap1bejfnvK6M3qtnkT0ssDKA
Response: {"id": 1, "username": "user@example.com", "email": "user@example.com"}
```

*Updating Personal Information*
```
Endpoint: /api/me/
Method: PUT
Header: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMjMsInVzZXJuYW1lIjoiZXhhbXBsZVVzZXIiLCJleHAiOjE3MTIxNDYxNDd9.zKobBlRuOiJSxCmi-iYap1bejfnvK6M3qtnkT0ssDKA
Body: {"username": "John Smith"}
Response: {"id": 1, "username": "John Smith", "email": "user@example.com"}
```

Queries to each of the endpoints can be performed either using curl or Postman, or from the browser GUI by going to the corresponding URL.


### Local running
```
./build.sh
python -m gunicorn restful_auth.asgi:application -k uvicorn.workers.UvicornWorker
```


### Tests
```
python manage.py test users
```
