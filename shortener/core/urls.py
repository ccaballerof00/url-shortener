from django.urls import path
from .views import CreateShortener, LinkPage, RedirectLink

app_name = 'core'
urlpatterns = [
    path('', CreateShortener.as_view(), name='index'),
    path('<int:pk>/', LinkPage.as_view(), name='detail'),
    path('<str:idurl>/', RedirectLink.as_view(), name='redirect')
]

