# coding:utf-8
from django.conf.urls import include, url
from django.contrib import admin
from stumanage import urls as stu_urls
from django.views.static import serve  # 和static文件不一样,媒体文件需配置一个url,用到此API
from django.conf import settings  # 导入项目的settings,目的是引用媒体文件的文件目录给document_root

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stumanage/', include(stu_urls, namespace='stumanage')),
    url(r'^upload/(.*)', serve, {'document_root': settings.MEDIA_ROOT}),
]
