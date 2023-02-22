from django.test import TestCase
from .models import User,Log
from django.db.models import Q
# Create your tests here.
class UserTest(TestCase):
        def user(self):
            User.objects.create(name='ali',number='09160714765',password='asdzxc')
        def test_user(self):
              ali=User.objects.get(name='ali')
              self.assertEqual(ali.number,'09160714765')
        def login(self):
              ali=User.objects.get(Q(name='ali') & Q(password='asdzxc'))
              self.assertIsNotNone(ali)
        def otp(self):
              pass
                      