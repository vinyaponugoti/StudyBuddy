from django.db import models

# Create your models here.
class Class(models.Model):
    course_mnemonic = models.CharField(max_length=5)
    course_number = models.CharField(max_length=5)
    other_info = models.CharField(max_length=300)

class Mnemonics(models.Model):
    course_mnemonics = models.CharField(max_length=5)


