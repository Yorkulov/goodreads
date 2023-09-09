from django.shortcuts import render


def lending_page(request):
    return render(request, 'landing_page.html')