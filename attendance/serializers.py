from rest_framework import serializers
from .models import Attendance
from employees.models import Employee


class AttendanceSerializer(serializers.ModelSerializer):
    # INPUT FIELD (write-only)
    employee_id = serializers.CharField(write_only=True)

    # OUTPUT FIELDS (read-only)
    employee = serializers.SerializerMethodField()

    class Meta:
        model = Attendance
        fields = [
            "id",
            "employee_id",
            "employee",
            "date",
            "status",
        ]

    def get_employee(self, obj):
        """
        Safe employee representation for frontend
        """
        if not obj.employee:
            return {
                "employee_id": None,
                "full_name": "Deleted Employee",
            }

        return {
            "employee_id": obj.employee.employee_id,
            "full_name": obj.employee.full_name,
        }

    def validate_employee_id(self, value):
        """
        Convert employee_id -> Employee instance
        """
        try:
            employee = Employee.objects.get(employee_id=value)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("Employee does not exist")

        return employee

    def create(self, validated_data):
        employee = validated_data.pop("employee_id")

        return Attendance.objects.create(
            employee=employee,
            **validated_data
        )
