from accounts.factories import CustomUserFactory
from bills.factories import BillFactory
from bills.models import Bill
from django.contrib.messages import get_messages
from django.test import TestCase, tag
from django.urls import reverse_lazy


class BillsTests(TestCase):
    def setUp(self):
        self.user = CustomUserFactory()
        self.bill_build = BillFactory.build(user=self.user)
        self.bill_data = self.bill_build.__dict__
        del self.bill_data["id"]
        del self.bill_data["start_date"]

    def test_user_create_bill_success(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse_lazy("bills:bills-list"), data=self.bill_data
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, 25)
        self.assertTrue(Bill.objects.all().first)

    @tag("x")
    def test_user_create_bill_with_invalid_data(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse_lazy("bills:bills-list"), data={})

        messages = list(get_messages(response.wsgi_request))
        form = response.context["form"]
        errors = form.errors

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level, 40)
        self.assertFalse(Bill.objects.all())
        self.assertFalse(form.is_valid())
        self.assertEqual(errors["creditor"][0], "This field is required.")
        self.assertEqual(errors["amount"][0], "This field is required.")
        self.assertEqual(errors["deadline"][0], "This field is required.")
