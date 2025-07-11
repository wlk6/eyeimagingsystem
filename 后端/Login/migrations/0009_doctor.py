# Generated by Django 5.1.3 on 2025-01-20 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0008_delete_doctor'),
    ]

    operations = [
        migrations.CreateModel(
            name='doctor',
            fields=[
                ('doctor_id', models.AutoField(primary_key=True, serialize=False)),
                ('doctorName', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('gender', models.CharField(max_length=6)),
                ('position', models.CharField(choices=[(1, 'chief_physician'), (2, 'associate_physician'), (3, 'attending_doctor')], max_length=20)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar', verbose_name='头像')),
            ],
            options={
                'db_table': 'doctor',
            },
        ),
    ]
