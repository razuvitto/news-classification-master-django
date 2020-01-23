# Coded with <3 Razuvitto
# location : apps/views.py
# April 2018

from django.shortcuts import render
from apps.classification import main

def form_index(request):
    return render(request, 'apps/welcome.html')

def classification(request):
    if request.method == 'POST':
        text = request.POST['input_text']
        cal1,cal2 = main.main(text)
        content = {'cal1': cal1, 'cal2': cal2 }
        return render(request, 'apps/index.html', content)
    return render(request, 'apps/index.html')

def report_svm(request):
    rep = main.report_svm() 
    sco = main.score_svm()
    report = {'rep': rep, 'sco' : sco}
    return render(request, 'apps/report.html', report)

def index(request):
    return render(request, 'apps/welcome.html')

