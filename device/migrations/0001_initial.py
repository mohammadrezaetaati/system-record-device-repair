# Generated by Django 4.0.6 on 2022-10-30 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('place', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial', models.CharField(max_length=50)),
                ('request_date', models.CharField(editable=False, max_length=20)),
                ('problem', models.CharField(max_length=255)),
                ('delivery', models.CharField(max_length=30)),
                ('description_cancel', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(choices=[('confirmation', 'Confirmation'), ('waiting', 'Waiting'), ('cancel', 'Cancel')], max_length=12)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='place.branch')),
                ('brand_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='device.brandcategory')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='device.category')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='place.place')),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.category')),
            ],
        ),
        migrations.CreateModel(
            name='NumberPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SmallIntegerField(default=1)),
                ('part', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='device.part')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceSave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_order_number', models.CharField(max_length=30)),
                ('entry_date', models.CharField(editable=False, max_length=20)),
                ('exit_date', models.CharField(default='-', editable=False, max_length=20)),
                ('provide_date', models.CharField(default='-', editable=False, max_length=20)),
                ('repair_city_date', models.CharField(default='-', editable=False, max_length=20)),
                ('delivery_operator', models.CharField(blank=True, default='-', max_length=100, null=True)),
                ('transferee', models.CharField(blank=True, default='-', max_length=30, null=True)),
                ('transferee_operator', models.CharField(max_length=100)),
                ('seal_number', models.CharField(blank=True, default='-', max_length=30, null=True)),
                ('description', models.CharField(blank=True, default='-', max_length=255, null=True)),
                ('status', models.CharField(choices=[('unrepairable', 'غیرقابل تعمیر'), ('finished', 'تحویل داده شده'), ('provide', 'آماده به تحویل'), ('repair_city', 'تعمیردرشهر'), ('ngoing', 'دردست اقدام')], max_length=12)),
                ('device_request', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='device.devicerequest')),
                ('parts', models.ManyToManyField(blank=True, default='-', null=True, to='device.numberpart')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.AddField(
            model_name='brandcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.category'),
        ),
    ]
