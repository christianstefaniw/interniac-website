from django.shortcuts import render


def marketplace(request):
    return render(request, template_name='marketplace/marketplace.html')