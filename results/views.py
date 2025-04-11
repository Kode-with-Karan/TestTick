from django.shortcuts import render
from .models import TestSummary
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.http import HttpResponse

@login_required
def user_results(request):
    summaries = TestSummary.objects.filter(student=request.user)
    return render(request, 'results/user_results.html', {'summaries': summaries})

@login_required
def download_results_excel(request):
    summaries = TestSummary.objects.filter(student=request.user)
    data = [summary.get_result_excel_data() for summary in summaries]
    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="results.xlsx"'
    df.to_excel(response, index=False)
    return response
