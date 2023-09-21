from django.shortcuts import render


def lending_page(request):
    print(request.user.is_authenticated)
    return render(request, 'landing_page.html')