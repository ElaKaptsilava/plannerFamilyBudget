import datetime

from accounts.factories import CustomUserFactory
from django.contrib.messages import get_messages
from django.test import TestCase, tag
from django.urls import reverse_lazy
from django.utils import timezone

from .factories import TargetContributionFactory, TargetFactory
from .models import Target


class TargetTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory()

        self.target_build = TargetFactory.build(
            user=self.user, deadline=datetime.date(3000, 1, 1)
        )
        self.contribution_build = TargetContributionFactory.build(
            target=self.target_build
        )

        self.target_cleand_data = self.target_build.__dict__

        del self.target_cleand_data["id"]

    def test_user_create_target_success(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse_lazy("targets:targets-list"), data=self.target_cleand_data
        )

        get_targets_by_user = Target.objects.filter(user=self.user)
        messages = list(get_messages(response.wsgi_request))
        get_target = Target.objects.get(pk=get_targets_by_user[0].id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(get_targets_by_user), 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "The target added successfully!")
        self.assertFalse(get_target.total_contributions)

    def test_user_create_target_with_invalid_data(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse_lazy("targets:targets-list"), data={})

        messages = list(get_messages(response.wsgi_request))
        form = response.context["form"]

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0].message, "Failed to add target. Please check the form."
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["target"][0], "This field is required.")
        self.assertEqual(form.errors["amount"][0], "This field is required.")

    def test_user_multiple_delete_target_success(self):
        self.client.force_login(self.user)

        target = TargetFactory.create(
            user=self.user, deadline=datetime.date(3000, 1, 1)
        )
        target1 = TargetFactory.create(
            user=self.user, deadline=datetime.date(3000, 1, 1)
        )
        target2 = TargetFactory.create(
            user=self.user, deadline=datetime.date(3000, 1, 1)
        )
        target3 = TargetFactory.create(
            user=self.user, deadline=datetime.date(3000, 1, 1)
        )

        self.assertEqual(Target.objects.count(), 4)

        list_to_delete = [target.pk, target1.pk, target3.pk]

        response = self.client.post(
            reverse_lazy("targets:targets-list-delete-multiple"),
            {"selected_targets": list_to_delete},
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0].message, "Selected targets were deleted successfully."
        )
        self.assertEqual(Target.objects.count(), 1)
        self.assertEqual(Target.objects.first().pk, target2.pk)

    def test_user_multiple_delete_target_with_empty_data(self):
        self.client.force_login(self.user)

        target = TargetFactory.create(
            user=self.user, deadline=datetime.date(3000, 1, 1)
        )

        response = self.client.post(
            reverse_lazy("targets:targets-list-delete-multiple"),
            {"selected_targets": []},
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "No targets were selected.")
        self.assertEqual(Target.objects.count(), 1)
        self.assertEqual(Target.objects.first().pk, target.pk)

    def test_user_update_target_success(self):
        self.client.force_login(self.user)

        target = TargetFactory.create(
            user=self.user, deadline=datetime.date(3000, 1, 1)
        )
        cleaned_data = {
            "pk": target.pk,
            "user": self.user.id,
            "target": "updated-target",
            "amount": 10,
            "description": target.description,
            "deadline": target.deadline,
        }

        response = self.client.post(
            reverse_lazy("targets:targets-list-create", kwargs={"pk": target.pk}),
            data=cleaned_data,
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "The target updated successfully!")
        self.assertEqual(Target.objects.count(), 1)

    def test_user_update_target_with_invalid_data(self):
        self.client.force_login(self.user)
        target = TargetFactory.create(
            user=self.user, deadline=datetime.date(3000, 1, 1)
        )

        response = self.client.post(
            reverse_lazy("targets:targets-list-create", kwargs={"pk": target.pk}),
            data={},
        )

        message = list(get_messages(response.wsgi_request))
        form = response.context["form"]

        self.assertEqual(len(message), 1)
        self.assertEqual(
            message[0].message, "Failed to update target. Please check the form."
        )
        self.assertEqual(Target.objects.count(), 1)
        self.assertEqual(form.errors["target"][0], "This field is required.")
        self.assertEqual(form.errors["amount"][0], "This field is required.")


class TargetContributionTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory()

    @tag("x")
    def test_user_add_contribution_success(self):
        self.client.force_login(self.user)

        target = TargetFactory.create(
            user=self.user, deadline=datetime.date(3000, 1, 1)
        )

        contribution = TargetContributionFactory.create(
            target=target, date=timezone.now().date(), amount=2050
        )

        contribution_clean_data = {
            "amount": 1000.0,
        }

        response = self.client.post(
            reverse_lazy("targets:contributions-list-create", kwargs={"pk": target.pk}),
            data={"amount": 1000.0},
        )

        messages = list(get_messages(response.wsgi_request))
        expected_total_contributions = (
            contribution.amount + contribution_clean_data["amount"]
        )
        expected_progres = int(expected_total_contributions * 100 / target.amount)

        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].message, "The contribution added successfully!")
        self.assertEqual(target.total_contributions, expected_total_contributions)
        self.assertEqual(target.progress_percentage, expected_progres)

    def test_user_add_contribution_with_invalid_data(self):
        self.client.force_login(self.user)

        target = TargetFactory.create(
            user=self.user, deadline=datetime.date(3000, 1, 1)
        )
        response = self.client.post(
            reverse_lazy("targets:contributions-list-create", kwargs={"pk": target.pk}),
            data={},
        )

        messages = list(get_messages(response.wsgi_request))
        form = response.context["form"]

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0].message,
            "Failed to add target contribution. Please check the form.",
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["amount"][0], "This field is required.")

    def test_user_multiple_delete_target_contributions_with_empty_data(self):
        self.client.force_login(self.user)

        target = TargetFactory.create(
            user=self.user, deadline=datetime.date(3000, 1, 1)
        )

        contributions = TargetContributionFactory.create(
            target=target, date=timezone.now().date()
        )
        contributions1 = TargetContributionFactory.create(
            target=target, date=timezone.now().date()
        )
        contributions2 = TargetContributionFactory.create(
            target=target, date=timezone.now().date()
        )
        contributions3 = TargetContributionFactory.create(
            target=target, date=timezone.now().date()
        )

        selected_contributions = [
            contributions.pk,
            contributions1.pk,
            contributions2.pk,
        ]

        response = self.client.post(
            reverse_lazy(
                "targets:contributions-list-delete-multiple", kwargs={"pk": target.pk}
            ),
            {"selected_contributions": selected_contributions},
        )

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            messages[0].message, "Target Contributions were deleted successfully."
        )
        self.assertEqual(len(target.targetcontribution_set.all()), 1)
        self.assertEqual(target.targetcontribution_set.first().pk, contributions3.pk)
