# Generated by Django 5.1.3 on 2025-04-30 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("image", "0011_imagediseaserelation_imagepatientrelation"),
    ]

    operations = [
        migrations.CreateModel(
            name="eyeImageResult",
            fields=[
                ("result_id", models.AutoField(primary_key=True, serialize=False)),
                ("image_id", models.IntegerField()),
                ("image_result", models.CharField(max_length=15)),
                ("image_desc", models.TextField()),
            ],
            options={
                "db_table": "image_result",
            },
        ),
    ]
