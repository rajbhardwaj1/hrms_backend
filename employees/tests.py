from rest_framework.test import APITestCase
from rest_framework import status
from .models import Employee

class EmployeeAPITest(APITestCase):

    def test_create_employee(self):
        payload = {
            "employee_id": "EMP001",
            "full_name": "Raj Bhardwaj",
            "email": "raj@example.com",
            "department": "IT",
        }

        response = self.client.post("/api/employees/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_employee_id(self):
        Employee.objects.create(
            employee_id="EMP002",
            full_name="Test User",
            email="test1@example.com",
            department="HR",
        )

        payload = {
            "employee_id": "EMP002",
            "full_name": "Another User",
            "email": "test2@example.com",
            "department": "HR",
        }

        response = self.client.post("/api/employees/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_employees(self):
        response = self.client.get("/api/employees/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_employee(self):
        Employee.objects.create(
            employee_id="EMP003",
            full_name="Delete Me",
            email="delete@example.com",
            department="Marketing",
        )

        response = self.client.delete("/api/employees/EMP003/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
