from django.conf.urls import url
from . import views

# Define URL patterns
# Each pattern triggers the corresponding view
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'index/', views.index, name='index'),
    url(r'network/', views.network, name='network'),
    url(r'cluster/', views.cluster, name='cluster'),
    url(r'timeline/', views.timeline, name='timeline'),
]