from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import date


# Create your models here.
class MyAccountManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        try:
            user = self.model(
                email=self.normalize_email(email),
                **extra_fields
            )
            user.is_active = True

            user.set_password(password)
            user.save(using=self._db)
        except Exception as e:
            print(e)
        return user


class Users(AbstractBaseUser):
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False
    )
    date_of_birth = models.CharField(max_length=30, blank=False, null=False, default=None)
    name = models.CharField(max_length=30, blank=False, null=False)
    surname = models.CharField(max_length=30, blank=False, null=False)
    objects = MyAccountManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["name", "surname", "date_of_birth"]

    class Meta:
        db_table = "tbl_users"

    def __str__(self):
        return str(self.email)


class SingleExpense(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    user = models.ForeignKey(Users, related_name='singleexpenses', on_delete=models.CASCADE, null=False)
    value = models.DecimalField(max_digits=65, decimal_places=2, blank=False, null=False)
    sign = models.BooleanField()
    date = models.DateField(default=date.today)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.value) + " " + str(self.sign)


class RecurringExpense(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    user = models.ForeignKey(Users, related_name='multipleexpenses', on_delete=models.CASCADE, null=False)
    value = models.DecimalField(max_digits=65, decimal_places=2, blank=False, null=False)
    sign = models.BooleanField()
    start_date = models.DateField(default=date.today)
    end_date = models.DateField()
    unit = models.CharField(max_length=1, blank=False, null=False, default="m")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.value) + " " + str(self.sign) + " " + str(self.start_date) + " " + str(
            self.end_date) + " " + str(self.unit)


class PatchExpense(models.Model):
    rec_exp = models.ForeignKey(RecurringExpense, related_name='patchexpense', on_delete=models.CASCADE)
    user = models.ForeignKey(Users, related_name='patchexpenses', on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=64, blank=False, null=False)
    value = models.DecimalField(max_digits=65, decimal_places=2, blank=False, null=False)
    sign = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)

    index = models.IntegerField()

    def __str__(self):
        return str(self.value) + " " + str(self.sign)
