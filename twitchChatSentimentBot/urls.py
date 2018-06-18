from django.conf.urls import include, url

urlpatterns = [
    url(r'^bot/', include('sentimentBot.urls', namespace='bot')),
]
