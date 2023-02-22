from django.core.validators import MinLengthValidator,RegexValidator
from django.db import models
import re
# Create your models here.
class User(models.Model ):
        phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the correct format ")
        
        name=models.CharField(max_length=30,blank=True,null=True)
        number=models.CharField(max_length=30,blank=False,unique=True,validators=[MinLengthValidator(11),phone_regex])   
        password=models.CharField(max_length=30,blank=True,null=True)
        create_at=models.DateTimeField(auto_now_add=True,null=True)

        def __str__(self):
            return self.number


class Log(models.Model):
      type=[ ("otp","otp"),("pass","pass")]
      
      num=models.ForeignKey('User',on_delete=models.CASCADE,related_name="log_user",verbose_name="user")
      time_log=models.DateTimeField(auto_now_add=True)
      type_log=models.CharField(choices=type,max_length=10)


      def __str__(self):
            return self.num.number           