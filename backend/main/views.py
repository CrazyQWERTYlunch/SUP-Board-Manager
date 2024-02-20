from django.shortcuts import render

def index(request):

    context = {
        'title':'НАЗВАНИЕ - Главная',
        'content': 'Сап что-то там НАЗВАНИЕ'
    }
    return render(request, 'main/index.html', context=context)


def about(request):
    context = {
        'title': 'НАЗВАНИЕ - О нас',
        'content': 'О нас',
        'text_on_page': 'Текст почему мы такие классные'
    }
    return render(request, 'main/about.html', context=context)