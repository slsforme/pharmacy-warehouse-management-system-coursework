from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # JWT
    path("api/token/",         TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(),    name="token_refresh"),
    path("api/token/verify/",  TokenVerifyView.as_view(),     name="token_verify"),

    # API
    path("api/users/",     include("apps.users.urls")),
    path("api/catalog/",   include("apps.catalog.urls")),
    path("api/inventory/", include("apps.inventory.urls")),
    path("api/sales/",     include("apps.sales.urls")),
    path("api/reports/",   include("apps.reports.urls")),

    # Документация
    path("api/schema/",         SpectacularAPIView.as_view(),     name="schema"),
    path("api/schema/swagger/", SpectacularSwaggerView.as_view(), name="swagger-ui"),
    path("api/schema/redoc/",   SpectacularRedocView.as_view(),   name="redoc"),

] + static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns