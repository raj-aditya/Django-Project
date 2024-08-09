from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    access_token = models.CharField(max_length=50, null=True)
    access_token_created_at = models.DateTimeField(null=True)
    
    def formatted_date(self):
        return self.created_at.strftime('%B %d, %Y at %I:%M %p')


    # def __str__(self):
    #     return self.first_name + " " + self.last_name
