import requests

url = "http://localhost:5000"
response = requests.get(url)

res = requests.post(url + "/user", json = {
    "username": "test_user1",
    "first_name": "test",
    "last_name": "user1",
    "password": "user1",
    "email": "testuser1@test.com"
}, headers={
    "Content-Type": "application/json"
})
print(res)