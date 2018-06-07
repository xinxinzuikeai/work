# coding:utf8
from django.conf.urls import include, url
from views import *

urlpatterns = [
    url(r'^main/', main, name='main'),
    url(r'^index/', index, name='index'),
    url(r'^help/', helps, name='helps'),
    url(r'^manage/', manage, name='manage'),
    url(r'^append/', append, name='append'),
    url(r'^saveStuToDB/(?P<id>[0-9]+)', saveStuToDB, name='saveStuToDB'),
    url(r'^deleteStuOfDB/(?P<id>[0-9]+)', deleteStuOfDB, name='deleteStuOfDB'),
    # ?P<id>意思是,引用id这个别名,然后让id携带后面匹配到的字符串
    url(r'^changeStuOfDB/(?P<id>[0-9]+)', changeStuOfDB, name='changeStuOfDB'),
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^register/', register, name='register'),
    url(r'^verifycode/', createVerifycode, name='verifycode'),
    url(r'^ajaxpage/', ajaxPage, name='ajaxpage'),
    url(r'^ajaxloadinfo/', ajaxLoadInfo, name='ajaxloadinfo'),
    url(r'^tinymce/', tinyMCE, name='tinymce'),
    url(r'^saveTinyMCE/', saveTinyMCE, name='saveTinyMCE'),
    url(r'^celery/', celeryFunc, name='celery'),
    url(r'^testpage/', testPage, name='testpage'),

]
