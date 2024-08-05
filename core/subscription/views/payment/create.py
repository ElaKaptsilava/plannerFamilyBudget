import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from subscription.models import Payment, Status

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        payment_id = kwargs.get("payment_id")
        payment = get_object_or_404(Payment, id=payment_id)
        context = {"payment": payment, "stripe_public_key": settings.STRIPE_PUBLIC_KEY}
        return render(request, "payment.html", context)

    def post(self, request, *args, **kwargs):
        payment_id = kwargs.get("payment_id")
        payment = get_object_or_404(Payment, id=payment_id)
        token = request.POST.get("stripeToken")

        try:
            stripe.Charge.create(
                amount=int(payment.amount * 100),
                currency="usd",
                description=f"Payment for subscription {payment.subscription.id}",
                source=token,
            )
            payment.status = Status.COMPLETED
            payment.save()
            return redirect(
                reverse("payment_success", kwargs={"payment_id": payment.id})
            )
        except stripe.error.StripeError:
            payment.status = Status.FAILED
            payment.save()
            return redirect(
                reverse("payment_failure", kwargs={"payment_id": payment.id})
            )


class PaymentSuccessView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        payment_id = kwargs.get("payment_id")
        payment = get_object_or_404(Payment, id=payment_id)
        return render(request, "payment_success.html", {"payment": payment})


class PaymentFailureView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        payment_id = kwargs.get("payment_id")
        payment = get_object_or_404(Payment, id=payment_id)
        return render(request, "payment_failure.html", {"payment": payment})


# @csrf_exempt
# def my_webhook_view(request):
#     payload = request.body
#     # event = None
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     if event.type == 'payment_intent.succeeded':
#         payment_intent = event.data.object  # contains a stripe.PaymentIntent
#         print('Payment intent succeeded')
#         # Then define and call a method to handle the successful payment intent.
#         # handle_payment_intent_succeeded(payment_intent)
#     elif event.type == 'payment_method.attached':
#         payment_method = event.data.object  # contains a stripe.PaymentMethod
#         # Then define and call a method to handle the successful attachment of a PaymentMethod.
#         # handle_payment_method_attached(payment_method)
#     # ... handle other event types
#     else:
#         print('Unhandled event type {}'.format(event.type))
#
#     return HttpResponse(status=200)
