from django.shortcuts import render
from apps.classification import main

def form_index(request):
    return render(request, 'apps/index.html')

def classification(request):
    if request.method == 'POST':
        text = request.POST['input_text']
        cal = main.main(text)
        content = {'cal': cal}
        return render(request, 'apps/index.html', content)
    return render(request, 'apps/index.html')
