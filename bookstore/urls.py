from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Bookstore API",
        default_version='v1',
        description="BookStore API for Frontend internship",
        terms_of_service="https://swagger.io/terms/",
        contact=openapi.Contact(email="puhoff.ol@yandex.ru | aleksandr.boyushenko@gmail.com"),
        license=openapi.License(name="absolutely working license"),
    ),
    url=f'{settings.URL}/',
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # noqa
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # noqa
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # noqa

    # admin panel
    path('admin/', admin.site.urls),


    # apps
    path('api/token/', include('authentication.urls')),
    path('api/users/', include('users.urls')),
    path('api/authors/', include('author.urls')),
    path('api/books/', include('books.urls')),
    path('api/genres/', include('genres.urls')),
    path('api/cart/', include('carts.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/favorites/', include('favorites.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]
