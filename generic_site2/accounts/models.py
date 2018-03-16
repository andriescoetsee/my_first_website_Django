from django.contrib import auth
from django.db import models
from django.utils import timezone
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class User(auth.models.User, auth.models.PermissionsMixin):
    # userType = models.TextField(default='NA', max_length=20)

    class Meta:
        pass
        permissions = (("conference_participant", "Can view Conference"), 
                        ("bible_study_participant", "Can view Bile Study"), 
                        ("tutor_participant", "Can view Tutoring"), 
                        ("is_bible_study_admin", "Has Bible Study administrator rights"), 
                        ("is_tutor_admin", "Has Tutor administrator rights"), 
                        ("is_conference_admin", "Has Conference administrator rights"), 
                    )
    
    def __str__(self):
        return "@{}".format(self.username)

# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
#         if not email:
#             raise ValueError("User must have an email address")
#         user_obj = self.model(
#             email = self.normalize_email(email)
#             )
#         user_obj.set_password(password)
#         user_obj.staff = is_staff
#         user_obj.admin = is_admin
#         user_obj.active = is_active
#         user_obj.save(using=self._db)
#         return user_obj

#     def create_staffuser(self, email, password=None):
#         user = self.create_user(
#                 email,
#                 password=password,
#                 is_staff=True
#             )
#         return user

#     def create_superuser(self, email, password=None):
#         user = self.create_user(
#                 email,
#                 password=password,
#                 is_staff=True,
#                 is_admin=True,
#                 is_superuser=True
#             )
#         return user

# class User(AbstractBaseUser, auth.models.PermissionsMixin):
#     email = models.EmailField(max_length=255, unique=True)
#     active = models.BooleanField(default=True) # can login
#     staff = models.BooleanField(default=False) # staff user non superuser
#     admin = models.BooleanField(default=False) # superuser
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     objects = UserManager()

#     @property
#     def is_staff(self):
#         return self.staff

#     @property
#     def is_admin(self):
#         return self.admin

#     @property
#     def is_active(self):
#         return self.active

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         return True

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True

#     class Meta:
#       permissions = (("conference_participant", "Can view Conference"), 
#          				("bible_study_participant", "Can view Bile Study"), 
#          				("tutor_participant", "Can view Tutoring"), 
#          				("is_bible_study_admin", "Has Bible Study administrator rights"), 
# 						("is_tutor_admin", "Has Tutor administrator rights"), 
# 						("is_conference_admin", "Has Conference administrator rights"), 
#          			)
