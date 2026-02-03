from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from .models import Attendance
from .serializers import AttendanceSerializer
import logging

logger = logging.getLogger(__name__)


class AttendanceListCreateView(generics.ListCreateAPIView):
    """
    GET  -> List attendance (supports ?date=YYYY-MM-DD)
    POST -> Mark attendance
    """
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.select_related("employee").all()

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get("date")

        if date:
            queryset = queryset.filter(date=date)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            attendance = serializer.save()

            logger.info(
                f"Attendance marked: {attendance.employee.employee_id} "
                f"{attendance.date} {attendance.status}"
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError:
            logger.warning("Duplicate attendance attempt")
            return Response(
                {"error": "Attendance already marked for this employee on this date"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("Unhandled exception")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AttendanceSummaryView(APIView):
    """
    GET -> Total present days per employee
    """

    def get(self, request):
        summary = {}

        records = Attendance.objects.filter(status="Present").select_related("employee")

        for record in records:
            emp = record.employee
            summary.setdefault(
                emp.employee_id,
                {
                    "employee_id": emp.employee_id,
                    "name": emp.full_name,
                    "present_days": 0,
                },
            )
            summary[emp.employee_id]["present_days"] += 1

        return Response(list(summary.values()), status=status.HTTP_200_OK)
