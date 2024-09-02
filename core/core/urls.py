from accounts.views.profile import HomeView
from budgets_manager.views.dash_app import EarningsDataView, RevenueSourcesView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from subscription.views import PaymentView
from subscription.views.payment.create import PaymentFailureView, PaymentSuccessView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "dashboard/",
        HomeView.as_view(),
        name="home",
    ),
    path("", include("communication.urls"), name="communication"),
    path("auth/", include("accounts.urls"), name="accounts"),
    path("incomes/", include("incomes.urls"), name="incomes"),
    path("expenses/", include("expenses.urls"), name="expenses"),
    path("running-costs/", include("runningCosts.urls"), name="running-costs"),
    path("targets/", include("targets.urls"), name="target"),
    path("manager/", include("budgets_manager.urls"), name="manager"),
    path("subscription/", include("subscription.urls"), name="subscription"),
    path("earnings-data/", EarningsDataView.as_view(), name="earnings-data"),
    path(
        "revenue-sources/",
        RevenueSourcesView.as_view(),
        name="revenue-sources",
    ),
    path("payment/<int:payment_id>/", PaymentView.as_view(), name="payment"),
    path(
        "payment/success/<int:payment_id>/",
        PaymentSuccessView.as_view(),
        name="payment_success",
    ),
    path(
        "payment/failure/<int:payment_id>/",
        PaymentFailureView.as_view(),
        name="payment_failure",
    ),
    path("multiuser/", include("multi_user.urls"), name="multiuser"),
    # path("stripe_webhooks", my_webhook_view, name="stripe-webhooks"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
