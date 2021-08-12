from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User


class UserManager(BaseUserManager):

    def create_user(self, email, firstname=None, lastname=None, password=None):

        if not email:
            raise ValueError("Please Enter Email")

        if User.objects.filter(email=self.normalize_email(email).lower()).exists():
            raise ValueError("Email Id Already Exists")

        user = self.model(
            firstname=firstname,
            lastname=lastname,
            email=self.normalize_email(email).lower()
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self.db)

        return user

    def create_superuser(self, email, firstname, lastname, password):

        if User.objects.filter(email=self.normalize_email(email).lower()).exists():
            raise ValueError("Email Id Already Exists")

        user = self.create_user(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password
        )

        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_admin = True

        print(user)
        breakpoint()

        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    firstname = models.CharField(max_length=255, blank=True, null=True)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(
        max_length=255, blank=False, null=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', ]

    objects = UserManager()

    def __str__(self):
        return self.email


class Skill(models.Model):
    employeeinfo = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="empdata")
    skillname = models.CharField(max_length=255, blank=False, null=False)
    percentage = models.IntegerField()

    def __str__(self):
        return self.skillname
