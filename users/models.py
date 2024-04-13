from django.db import models
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError('Users must have a valid email')
        if not password:
            raise ValueError("You must enter a password")
        
        email=self.normalize_email(email)
        user_obj=self.model(email=email)
        user_obj.set_password(password)
        user_obj.staff=is_staff
        user_obj.admin=is_admin
        user_obj.active=is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,email,password=None):
        user=self.create_user(email,password=password,is_staff=True)
        return user

    def create_superuser(self,email,password=None):
        user=self.create_user(email,password=password,is_staff=True,is_admin=True)
        return user
        

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    active=models.BooleanField(default=True)
    staff=models.BooleanField(default=False)
    admin=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects= UserManager()

    groups = models.ManyToManyField(
        "auth.Group", blank=True, related_name="custom_user_set", related_query_name="user"
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        blank=True,
        related_name="custom_user_set",
        related_query_name="user",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active
    
class Appointment(models.Model):
    names = models.CharField(max_length=255,null=True, blank=True)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20,null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    appointment_type = models.CharField(max_length=100 ,null=True, blank=True)
    insurance = models.CharField(max_length=100 ,null=True, blank=True)
    message = models.TextField(null=True,blank=True)
    confirmed = models.BooleanField(default=False,null=True, blank=True)
    rejected = models.BooleanField(default=False,null=True, blank=True)
    requested = models.BooleanField(default=True,null=True, blank=True)

    @property
    def appointment_status(self):
        if self.requested and self.confirmed:
            return 'Confirmed'
        elif self.requested and self.rejected:
            return 'Rejected'
        else:
            return 'Requested'

    def __str__(self):
        return f"{self.names} - {self.date}"