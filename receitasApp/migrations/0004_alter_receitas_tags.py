# Generated by Django 4.2.4 on 2023-10-08 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tagApp', '0002_remove_tag_content_type_remove_tag_object_id'),
        ('receitasApp', '0003_receitas_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receitas',
            name='tags',
            field=models.ManyToManyField(blank=True, default='', to='tagApp.tag'),
        ),
    ]
