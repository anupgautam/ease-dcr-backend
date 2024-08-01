from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)



class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password, confirm_password=None,role_name=None, company_name=None):
        """
        Creates and saves a User with the given email, first_name
        last_name, phone_number and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        if password == "":
            password = "12345"
        user.set_password(password)
        user.role_name = role_name
        user.company_name = company_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, password=None,role_name=None,company_name=None):
        """
        Creates and saves a superuser with the given email, first_name, last_name, phone_number and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            role_name=role_name,
            company_name=company_name,
        )
        
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_user_with_signal(self, first_name,
                                last_name,
                                email,
                                phone_number,
                                role_name,
                                company_name,
                                password):
        
        user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    )
        user.set_password(password)        
        user.role_name = role_name
        user.company_name = company_name
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number =  models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    # address = models.CharField(max_length=500, default="kathmandu")
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name',
                        'last_name',
                        'phone_number',
                        ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        # "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        ordering = ['-id']

