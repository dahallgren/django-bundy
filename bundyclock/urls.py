from django.conf.urls import include, url

from views import index, router

urlpatterns = [
    url(r'^$', index, name='bundyclock'),
    url(r'^api/', include(router.urls)),
]
