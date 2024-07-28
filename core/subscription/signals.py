from dateutil.relativedelta import relativedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from subscription.models import Payment, Status, Subscription


@receiver(post_save, sender=Subscription)
def create_payment_with_subscription(sender, instance, created, **kwargs):
    if created:
        if not hasattr(instance, "payment"):
            Payment.objects.create(
                subscription=instance,
                due_date=instance.start_date - relativedelta(days=1),
                amount=instance.plan.price,
            )
            if instance.plan.price == 0:
                instance.payment.status = Status.COMPLETED
            instance.payment.save()
