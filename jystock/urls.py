from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('usuarios.urls')),
    path('estoque/', include('estoque.urls')),
    path('plataforma/', include('plataforma.urls')),
    path('vendas/', include('vendas.urls')),
    path('clientes/', include('clientes.urls')),
    path('cupons/', include('cupons.urls')),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)