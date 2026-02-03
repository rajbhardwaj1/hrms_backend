from rest_framework.test import APITestCase
from rest_framework import status
from employees.models import Employee
from .models import Attendance

class AttendanceAPITest(APITestCase):

    def setUp(self):
        self.employee = Employee.objects.create(
            employee_id="EMP100",
            full_name="Test Employee",
            email="test@company.com",
            department="IT"
        )

    def test_mark_attendance(self):
        payload = {
            "employee_id": "EMP100",
            "date": "2026-02-03",
            "status": "Present"
        }

        response = self.client.post("/api/attendance/", payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_attendance_same_day(self):
        Attendance.objects.create(
            employee=self.employee,
            date="2026-02-03",
            status="Present"
        )

        payload = {
            "employee_id": "EMP100",
            "date": "2026-02-03",
            "status": "Absent"
        }

        response = self.client.post("/api/attendance/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_by_date(self):
        response = self.client.get("/api/attendance/?date=2026-02-03")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_attendance_summary(self):
        response = self.client.get("/api/attendance/summary/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
