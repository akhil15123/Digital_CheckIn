# Generated by Django 5.1.7 on 2025-03-11 09:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('dep_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('role', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=20)),
                ('dep', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('attendance_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')], max_length=20)),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Apology',
            fields=[
                ('apology_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('reason', models.TextField()),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Leaves',
            fields=[
                ('leave_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('reason', models.TextField()),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
