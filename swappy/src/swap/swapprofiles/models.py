from django.db import models

from actives.models import Active


class Contact(models.Model):
    user_login = models.ForeignKey(Active, related_name='Contact.user_login')
    contact_link = models.CharField(max_length=50)
    contact_name = models.CharField(max_length=10)

    class Meta:
        unique_together = ('user_login', 'contact_link')
        db_table = 'contacts'
        managed = False


class Location(models.Model):
    user_login = models.ForeignKey(Active, primary_key=True, related_name='Location.user_login')
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    department = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=20)

    class Meta:
        db_table = 'locations'
        managed = False


class Professional(models.Model):
    user_login = models.ForeignKey(Active, primary_key=True, related_name='Professionals.user_login')
    resume_pdf = models.CharField(max_length=50)
    current_job = models.CharField(max_length=20)
    current_org = models.CharField(max_length=20)

    class Meta:
        db_table = 'professionals'
        managed = False


class Profile(models.Model):
    user_login = models.ForeignKey(Active, primary_key=True, related_name='Profule.user_login')
    status = models.CharField(max_length=50, null=True, blank=True)
    biography = models.CharField(max_length=1000, null=True, blank=True)
    avatar = models.CharField(max_length=50, null=True, blank=True)
    currency = models.CharField(max_length=1)
    age = models.IntegerField()
    last_active = models.DateTimeField()

    class Meta:
        db_table = 'profiles'
        managed = False