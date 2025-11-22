from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    # Aqui dizemos: qualquer URL vazia ou que comece com o app, vai para o urls do app
    path('', include('educamais_app.urls')), 
]