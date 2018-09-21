from django.conf.urls import include, url
from django.contrib import admin
from json_parser import api

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/parse-json/$', api.JsonParserView.as_view()),
]
