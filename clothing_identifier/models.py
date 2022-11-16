from django.db import models

# Create your models here.

class TempVideo(models.Model):
   image = models.FileField(upload_to="temp/Image/")
   class Meta :
      db_table = "Temporary Images"