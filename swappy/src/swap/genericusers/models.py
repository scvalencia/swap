from django.db import models


class GenericUser(models.Model):
    """
    This class represents the object conversion from the 
    users relation presented in the Oracle database.
    """
    login = models.CharField(max_length=20, primary_key=True)
    user_id = models.CharField(max_length=20)
    user_pass = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    class Meta:
        db_table = 'users'
        managed = False


class Legal(models.Model):
    """
    This class represents the object conversion from the 
    users relation presented in the Oracle database.
    """
    legal_id = models.CharField(max_length=20, primary_key=True)
    legal_name = models.CharField(max_length=20)
    user_login = models.ForeignKey(GenericUser, related_name='Legal.user_login', db_column='user_login')

    class Meta:
        db_table = 'legals'
        managed = False

class GenericUserDump(object):

    def __init__(self, login, user_id, user_pass, first_name, last_name, email, phone):
        self.login = login
        self.user_id = user_id
        self.user_pass = user_pass
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

    def create_object(self, arg_login, arg_user_id, arg_user_pass, 
        arg_first_name, arg_last_name, arg_email, arg_phone):
        generic_user_object = GenericUser(login = arg_login, user_id = arg_user_id, 
            user_pass = arg_user_pass, first_name = arg_first_name, last_name = arg_last_name,
            email = arg_email, phone = arg_phone)
        generic_user_object.save()

    def __str__(self):
        ans = '('
        ans += str(self.login) + ', '
        ans += str(self.user_id) + ', '
        ans += str(self.user_pass) + ', '
        ans += str(self.first_name) + ', '
        ans += str(self.last_name) + ', '
        ans += str(self.email) + ', '
        ans += str(self.phone)
        ans += ')'
        return ans

class LegalDump(object):

    def __init__(self, legal_id, legal_name, user_login):
        self.legal_id = legal_id
        self.legal_name = legal_name
        self.user_login = user_login

    def create_object(self, arg_legal_id, arg_legal_name, arg_user_login):
        legal_object = Legal(legal_id = arg_legal_id, legal_name = arg_legal_name,
            user_login = arg_user_login)
        legal_object.save()

    def __str__(self):
        ans = '('
        ans += str(self.legal_id) + ', '
        user_id = str(self.legal_name) + ', '
        user_pass = str(self.user_login)
        ans += ')'
        return ans