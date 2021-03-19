# Generated by Django 3.1.5 on 2021-03-19 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='is_parent',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent_categ_id',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='listings.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='currency',
            field=models.CharField(choices=[('usd', 'USD'), ('lbp', 'LBP')], default='usd', max_length=10),
        ),
    ]
