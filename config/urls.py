from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('empresas/', include('apps.empresa.urls')),
    path('refeicoes/', include('apps.refeicoes.urls')),
    path('gestao-pessoas/', include("apps.gestao_pessoas.urls"))
]

if settings.DEBUG:    
    import debug_toolbar
    from django.urls import include, path

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
