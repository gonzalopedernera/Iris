from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.contrib.contenttypes.models import ContentType

class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
class UserAccounts(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
def get_full_name(self):
    return self.name
def get_short_name(self):
    return self.name
def __str__(self):
    return self.email
class Business_Data(models.Model):
    id = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)
    name_business = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    social_media = models.CharField(max_length=100, default="Instagram")
    def __str__(self):
        return self.name_business
class CollaboratorAccounts(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    id_business_data = models.ForeignKey(Business_Data, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserAccountManager()
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='collaborator_accounts',
        blank=True,
        help_text='The groups this collaborator belongs to. A collaborator will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='collaborator_accounts',
        blank=True,
        help_text='Specific permissions for this collaborator.',
        verbose_name='user permissions',
    )
    def save(self, *args, **kwargs):
        created = not self.pk
        super(CollaboratorAccounts, self).save(*args, **kwargs)
        if created:
            collaborator_group = Group.objects.get_or_create(name='Collaborators')[0]
            self.groups.add(collaborator_group)
            content_type = ContentType.objects.get_for_model(Calendar)
            permissions = Permission.objects.filter(content_type=content_type)

            for perm in permissions:
                if perm.codename == "view_calendar":
                    collaborator_group.permissions.add(perm)
    def __str__(self):
        return self.name
class Services(models.Model):
    id = models.AutoField(primary_key=True)
    id_collaborator = models.ForeignKey(CollaboratorAccounts, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    price = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Clients(models.Model):
    id = models.AutoField(primary_key=True)
    id_business_data = models.ForeignKey(Business_Data, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    notes = models.TextField()
    def __str__(self):
        return self.name
class calendar(models.Model):
    id = models.AutoField(primary_key=True)
    id_collaborator = models.ForeignKey(CollaboratorAccounts, on_delete=models.CASCADE)
    def __str__(self):
        return f"Calendar {self.id}"
class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    id_service = models.ForeignKey(Services, on_delete=models.CASCADE)
    id_client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    startTime = models.CharField(max_length=50)
    endTime = models.CharField(max_length=50)
    def __str__(self):
        return f"Appointment {self.id}"

