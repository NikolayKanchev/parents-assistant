import datetime

from dateutil.relativedelta import relativedelta
from django.test import TestCase
from home.factories import ChildFactory


class ChildTestCase(TestCase):

    def test_age(self):
        alex = ChildFactory(date_of_birth=datetime.date(2016, 4, 26))
        emma = ChildFactory(date_of_birth=datetime.date(2018, 4, 21))

        self.assertEqual(alex.age, relativedelta(years=+2, months=+8, days=+22))
        self.assertEqual(emma.age, relativedelta(months=+8, days=+27))

