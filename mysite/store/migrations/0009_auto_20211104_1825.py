# Generated by Django 3.2.8 on 2021-11-04 18:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0008_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ip_address',
            field=models.CharField(default=0, max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]