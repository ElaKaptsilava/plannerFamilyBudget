from accounts.factories import CustomUserFactory
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from targets.tests.factories import TargetFactory


class CommandsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserFactory.create()

    def test_update_target_deadlines_command(self):
        deadline = timezone.now().date() - timezone.timedelta(days=1)
        target = TargetFactory.create(user=self.user, deadline=deadline)

        call_command("update_target_deadlines")

        target.refresh_from_db()

        self.assertGreater(target.deadline, timezone.now().date())
        self.assertEqual(target.deadline, deadline + timezone.timedelta(days=30))
