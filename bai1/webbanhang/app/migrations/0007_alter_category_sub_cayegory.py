# Generated by Django 4.2.4 on 2023-10-23 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='sub_cayegory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='app.category'),
        ),
    ]
