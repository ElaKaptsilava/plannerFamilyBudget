"""
URL configuration for core project.

The `urlpatterns` list routes URLs to planer_views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function planer_views
    1. Add an import:  from my_app import planer_views
    2. Add a URL to urlpatterns:  path('', planer_views.home, name='home')
Class-based planer_views
    1. Add an import:  from other_app.planer_views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from accounts.views import HomeView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "home/<int:user_id>/",
        HomeView.as_view(),
        name="home",
    ),
    path("auth/", include("accounts.urls"), name="accounts"),
    path("incomes/", include("incomes.urls"), name="incomes"),
    path("expenses/", include("expenses.urls"), name="expenses"),
    path("running-costs/", include("runningCosts.urls"), name="running-costs"),
    path("targets/", include("targets.urls"), name="target"),
    path("manager/", include("budgets_manager.urls"), name="manager"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
