# Generated by Django 2.2.4 on 2019-08-12 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_auto_20190812_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='plan_type',
            field=models.CharField(choices=[('single', 'single'), ('plus', 'plus'), ('infinite', 'infinite')], default='single', max_length=60, verbose_name='plan type'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='total_websites_allowed',
            field=models.PositiveIntegerField(default=1, help_text='not used for plan infinite'),
        ),
    ]