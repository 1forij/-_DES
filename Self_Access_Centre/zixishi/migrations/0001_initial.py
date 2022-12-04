# Generated by Django 3.2.15 on 2022-09-21 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=100)),
                ('teacher', models.CharField(max_length=100)),
                ('classes', models.CharField(max_length=100)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='zixishi.building')),
            ],
        ),
    ]
