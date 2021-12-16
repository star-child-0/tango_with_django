from django.shortcuts import render


def index(request):
    context_dict = {
        'boldmessage': "This message is in bold font thanks to templates!"}
    return render(request, 'rango/index.html', context=context_dict)
