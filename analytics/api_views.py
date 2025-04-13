from rest_framework import generics, permissions, filters
from rest_framework.views import APIView
from django.utils.dateparse import parse_datetime
from django_filters.rest_framework import DjangoFilterBackend
from .models import QuestionPerformance, UserActivityLog, InstitutionStats
from .serializers import (
    QuestionPerformanceSerializer,
    UserActivityLogSerializer,
    InstitutionStatsSerializer
)

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
import csv

class ExportInstitutionStatsPDF(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica", 14)
        p.drawString(100, 800, "Institution Summary Report")

        stats = InstitutionStats.objects.filter(
            institution=request.user.institution
        ).first()

        if stats:
            p.setFont("Helvetica", 12)
            p.drawString(50, 770, f"Total Tests: {stats.total_tests}")
            p.drawString(50, 750, f"Total Students: {stats.total_students}")
            p.drawString(50, 730, f"Average Score: {stats.average_score}")
        else:
            p.drawString(50, 770, "No statistics available.")

        p.showPage()
        p.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')

class ExportInstitutionStatsCSV(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="institution_stats.csv"'

        writer = csv.writer(response)
        writer.writerow(['Institution', 'Total Tests', 'Total Students', 'Average Score'])

        stats = InstitutionStats.objects.filter(
            institution=request.user.institution
        ).first()

        if stats:
            writer.writerow([
                stats.institution.name,
                stats.total_tests,
                stats.total_students,
                stats.average_score
            ])
        else:
            writer.writerow(['No data available', '-', '-', '-'])

        return response


class ExportQuestionPerformanceCSV(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="question_performance.csv"'

        writer = csv.writer(response)
        writer.writerow(['Question', 'Quiz', 'Attempts', 'Correct'])

        performances = QuestionPerformance.objects.filter(
            question__quiz__created_by__institution=request.user.institution
        ).select_related('question', 'question__quiz')

        for perf in performances:
            writer.writerow([
                perf.question.text,
                perf.question.quiz.title,
                perf.times_attempted,
                perf.times_correct
            ])

        return response

class ExportQuestionPerformancePDF(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        p.setFont("Helvetica", 14)
        p.drawString(100, 800, "Question Performance Report")

        performances = QuestionPerformance.objects.filter(
            question__quiz__created_by__institution=request.user.institution
        ).select_related('question', 'question__quiz')

        y = 770
        for perf in performances:
            if y < 100:
                p.showPage()
                y = 800
            text = f"{perf.question.text[:60]}... | Attempts: {perf.times_attempted}, Correct: {perf.times_correct}"
            p.drawString(50, y, text)
            y -= 20

        p.showPage()
        p.save()
        buffer.seek(0)

        return HttpResponse(buffer, content_type='application/pdf')


class QuestionPerformanceList(generics.ListAPIView):
    serializer_class = QuestionPerformanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['question__quiz__id']
    search_fields = ['question__text']

    def get_queryset(self):
        user = self.request.user
        queryset = QuestionPerformance.objects.filter(
            question__quiz__created_by__institution=user.institution
        )
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')
        if start:
            queryset = queryset.filter(question__quiz__created_at__gte=parse_datetime(start))
        if end:
            queryset = queryset.filter(question__quiz__created_at__lte=parse_datetime(end))
        return queryset

class UserActivityList(generics.ListAPIView):
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [permissions.IsAdminUser]

class InstitutionStatsDetail(generics.RetrieveAPIView):
    serializer_class = InstitutionStatsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return InstitutionStats.objects.get(institution=self.request.user.institution)
