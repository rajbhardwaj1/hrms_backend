from rest_framework import serializers
from .models import Attendance
from employees.models import Employee

class AttendanceSerializer(serializers.ModelSerializer):
    employee_id = serializers.CharField(write_only=True)
    employee_name = serializers.CharField(
        source="employee.full_name",
        read_only=True
    )

    class Meta:
        model = Attendance
        fields = [
            "id",
            "employee_id",
            "employee_name",
            "date",
            "status",
            "created_at",
        ]

    def validate_employee_id(self, value):
        if not Employee.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee does not exist")
        return value

    def create(self, validated_data):
        employee_id = validated_data.pop("employee_id")
        employee = Employee.objects.get(employee_id=employee_id)
        return Attendance.objects.create(employee=employee, **validated_data)
