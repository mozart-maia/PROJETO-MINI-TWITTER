from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'twitter'

urlpatterns = [
    path('timeline/', views.PubList.as_view()),
    path('detalhe/<int:pk>/', views.PubDetalhe.as_view()),
    path('registrar/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('tweetar/', views.AdicionarPub.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)