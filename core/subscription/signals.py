from django.db.models.signals import post_save
from django.dispatch import receiver
from subscription.models import Status, Subscription


@receiver(post_save, sender=Subscription)
def create_payment_with_subscription(sender, instance, created, **kwargs):
    print("Start signal create_payment_with_subscription")
    if created:
        print("Payment not exist and Subscription created")
        if not hasattr(instance, "payment"):
            instance.payment.create(
                date=instance.start_date, amount=instance.plan.price
            )
            if instance.plan.price == 0:
                instance.payment.status = Status.COMPLETED
            instance.payment.save()
            print("Payment save...")
