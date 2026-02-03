import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Employee
from .serializers import EmployeeSerializer

logger = logging.getLogger(__name__)

class EmployeeListCreateView(APIView):
    def get(self, request):
        employees = Employee.objects.all().order_by("-created_at")
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Employee created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(f"Employee creation failed: {serializer.errors}")
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class EmployeeDeleteView(APIView):
    def delete(self, request, employee_id):
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            employee.delete()
            logger.info(f"Employee {employee_id} deleted")
            return Response(
                {"message": "Employee deleted"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Employee.DoesNotExist:
            logger.warning(f"Delete failed. Employee {employee_id} not found")
            return Response(
                {"error": "Employee not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
