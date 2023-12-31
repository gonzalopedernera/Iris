# Generated by Django 4.2.6 on 2023-11-06 12:17

import IrisApp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business_Data',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name_business', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('business_type', models.CharField(max_length=100)),
                ('social_media', models.CharField(default='Instagram', max_length=100)),
                ('opening_hours', models.TimeField(default='08:00')),
                ('closing_hours', models.TimeField(default='18:00')),
                ('time_range', models.JSONField(default=IrisApp.models.default_time)),
            ],
        ),
        migrations.CreateModel(
            name='CollaboratorAccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this collaborator belongs to. A collaborator will get all permissions granted to each of their groups.', related_name='collaborator_accounts', to='auth.group', verbose_name='groups')),
                ('id_business_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IrisApp.business_data')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this collaborator.', related_name='collaborator_accounts', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(max_length=100)),
                ('price', models.CharField(max_length=100)),
                ('id_business_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IrisApp.business_data')),
                ('id_collaborator', models.ManyToManyField(to='IrisApp.collaboratoraccounts')),
            ],
        ),
        migrations.AddField(
            model_name='business_data',
            name='id_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('days', models.DateField(validators=[IrisApp.models.validate_days])),
                ('startTime', models.CharField(default='', max_length=100)),
                ('name', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('phone', models.CharField(default='', max_length=100)),
                ('id_collaborator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IrisApp.collaboratoraccounts')),
                ('id_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IrisApp.services')),
            ],
        ),
    ]
