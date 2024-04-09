"""
Load Testing with Locus:
    locust -f locustfile.py

    locust -f locustfile.py --headless -u 10 -r 5 --run-time 30

Reference: https://github.com/locustio/locust/blob/master/examples/basic.py
"""

from locust import HttpUser, task, between, TaskSet


class UserTasks(TaskSet):
    """Task Set"""

    @task
    def index(self):
        """GET: index test task"""
        self.client.get("/")

    @task
    def predict(self):
        """POST: Testing ml prediction task"""
        headers = {"Content-Type": "application/json"}
        data = {
            "CHAS": {"0": 0},
            "RM": {"0": 6.575},
            "TAX": {"0": 296.0},
            "PTRATIO": {"0": 15.3},
            "B": {"0": 396.9},
            "LSTAT": {"0": 4.98},
        }
        self.client.post("/predict", json=data, headers=headers)


class WebsiteUser(HttpUser):
    """a class used in locust load testing to represent a user"""

    wait_time = between(1, 3)

    host = "https://flask145.azurewebsites.net:443"

    def on_start(self):
        """Called when simulated user starts"""
        print("Starting user")

    def on_stop(self):
        """Called when simulated user stops"""
        print("Stopping user")

    tasks = [UserTasks]
