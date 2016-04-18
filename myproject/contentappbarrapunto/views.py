from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from models import Put_App
from xmlbarrapunto import getNews
from django.core.cache import caches

cache = caches['default']

def updateNews(request):
    news = getNews()
    cache.set('news', news) #lo que tenemos ya parseado lo metenmos en cache
    return HttpResponse("News update<br>")


@csrf_exempt
def processRequest(request, resource):
    if request.method == "GET":
        try:
            content = Put_App.objects.get(titulo=resource)
            news = cache.get('news')  #cogemos de la cache
            respuesta = ""
            if news == None:

                news = getNews()
                cache.set('news', news)
                respuesta += content.contenido + news
            else:
                respuesta +=content.contenido + news
        except Put_App.DoesNotExist:
            return HttpResponse(resource + " not found")
    elif request.method =="PUT":
        newContent = Put_App(titulo=resource, contenido=request.body)
        newContent.save()
        return HttpResponse(resource + " added to the list")
    else:
        return HttpResponse(status=403)

    context = {'contenido': respuesta}
    return render(request, 'plantilla.html', {'context': context})
