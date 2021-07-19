from django.db import models

# Create your models here.
# db table make
class Error(models.Model):
    equip_name = models.CharField(max_length=30)
    error_content = models.TextField()
    def __str__(self):
        return f'{self.id},{self.error_content}'