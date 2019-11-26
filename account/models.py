from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, id_number, email, first_name, last_name, password=None, **kwargs):
        if not id_number:
            raise ValueError('ID Number is required')
        if not email:
            raise ValueError('Enter valid email please')
        if not first_name or not last_name:
            raise ValueError('Please enter your name')
        if not email:
            raise ValueError('You must enter password')

        user = self.model(
            id_number=id_number,
            email=self.normalize_email(email),
            username = id_number,
            first_name = first_name,
            last_name = last_name
        )
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, id_number, email, first_name, last_name, password, **kwargs):
        user = self.create_user(
            id_number=id_number,
            email=email,
            password=password,
            first_name = first_name,
            last_name = last_name
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.userlevel = None

        user.save(using=self._db)
        return user


class UserModel(AbstractUser):
    userlevels = [
        ('farmer', 'Farmer'),
        ('accounts', 'Accountant'),
        ('factory_admin', 'Factory Admin'),
        ('overadmin', 'Super Admin')
    ]
    id_number = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField()
    userlevel = models.CharField(max_length=50, choices=userlevels, default='farmer')

    USERNAME_FIELD = "id_number"
    REQUIRED_FILEDS = ['email', 'first_name', 'last_name' 'password']
    objects = UserManager()

    def __str__(self):
        return f"{self.id_number} -  {self.first_name}"

    def has_perm(self, perm, obj=None):
        return self.is_active and self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_admin


class Profile(models.Model):
    genders = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ]
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profiles", default="default.jpg")
    gender = models.CharField(max_length=20, choices=genders, default="other")

    def __str__(self):
        return f"{self.user.username} - {self.user.email}"
