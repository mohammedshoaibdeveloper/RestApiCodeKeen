# from django.contrib.auth.base_user import BaseUserManager


# class UserManager(BaseUserManager):

#     use_in_migrations = True

#     def _create_user(self, email, password, **extra_fields):
#         """
#         Creates and saves a user with the given email and password.
#         """
#         if not email:
#             raise ValueError('The given email must be set')

#         email = self.normalize_email(email)

#         user = self.model(email=email, **extra_fields)

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email, password=None, **extra_fields):
       
#         if not email:
#             raise ValueError(_('The Email must be set'))

#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()


from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user