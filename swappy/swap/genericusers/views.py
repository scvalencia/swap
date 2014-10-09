from django.shortcuts import render


def userzone(request):
    return render(request, 'genericusers/userzone.html')