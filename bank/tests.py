from django.test import TestCase

from . import models


class SimpleTest(TestCase):
    def test_first_object_in_db(self):
        # The object was created in a migration step
        obj1 = models.SimpleModel.objects.first()
        self.assertEqual(obj1.just_text, 'Text 1')

    def test_second_object_in_db(self):
        # The object was created in a migration step
        obj1 = models.SimpleModel.objects.get(pk=2)
        self.assertEqual(obj1.just_text, 'Text 2')
