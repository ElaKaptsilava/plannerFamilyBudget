from accounts.views.profile.home import HomeView
from budgets_manager.views import dash_app
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "home",
        HomeView.as_view(),
        name="home",
    ),
    path("auth/", include("accounts.urls"), name="accounts"),
    path("incomes/", include("incomes.urls"), name="incomes"),
    path("expenses/", include("expenses.urls"), name="expenses"),
    path("running-costs/", include("runningCosts.urls"), name="running-costs"),
    path("targets/", include("targets.urls"), name="target"),
    path("manager/", include("budgets_manager.urls"), name="manager"),
    path("earnings-data/", dash_app.earnings_data, name="earnings_data"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
