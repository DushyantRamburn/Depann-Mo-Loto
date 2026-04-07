import requests

BASE_URL = "http://127.0.0.1:8000/api"

class APIClient:
    def __init__(self):
        self.token = None

    def login(self, email, password):
        try:
            r = requests.post(f"{BASE_URL}/auth/login/",
                              json={"email": email, "password": password})
            if r.status_code == 200:
                data = r.json()
                self.token = data["access"]
                return data
            return None
        except Exception as ex:
            print(f"LOGIN ERROR: {ex}")
            return None

    def register(self, email, password, first_name, last_name):
        try:
            r = requests.post(f"{BASE_URL}/auth/register/", json={
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
            })
            print(f"REGISTER STATUS: {r.status_code}")
            print(f"REGISTER RESPONSE: {r.text}")
            if r.status_code == 201:
                data = r.json()
                self.token = data["access"]
                return data
            return None
        except Exception as ex:
            print(f"REGISTER ERROR: {ex}")
            return None

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def get_services(self):
        try:
            r = requests.get(f"{BASE_URL}/services/")
            return r.json() if r.status_code == 200 else []
        except Exception as ex:
            print(f"GET SERVICES ERROR: {ex}")
            return []

    def get_bookings(self):
        try:
            r = requests.get(f"{BASE_URL}/bookings/", headers=self._headers())
            return r.json() if r.status_code == 200 else []
        except Exception as ex:
            print(f"GET BOOKINGS ERROR: {ex}")
            return []

    def create_booking(self, data):
        try:
            r = requests.post(f"{BASE_URL}/bookings/create/",
                              json=data, headers=self._headers())
            print(f"BOOKING STATUS: {r.status_code}")
            print(f"BOOKING RESPONSE: {r.text}")
            return r.json(), r.status_code
        except Exception as ex:
            print(f"BOOKING ERROR: {ex}")
            return {"error": f"Connection error: {ex}"}, 500

    def get_branches(self):
        try:
            r = requests.get(f"{BASE_URL}/branches/")
            return r.json() if r.status_code == 200 else []
        except Exception as ex:
            print(f"GET BRANCHES ERROR: {ex}")
            return []