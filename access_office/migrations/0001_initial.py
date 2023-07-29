# Generated by Django 4.2.1 on 2023-07-12 18:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Automobile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_plate', models.CharField(db_index=True, max_length=9)),
                ('car_registration_number', models.CharField(max_length=10)),
                ('car_brand', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'Автомобиль',
                'verbose_name_plural': 'Автомобили',
            },
        ),
        migrations.CreateModel(
            name='CrossingPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crossing_point_name', models.CharField(db_index=True, max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Пропускной пункт',
                'verbose_name_plural': 'Пропускные пункты',
            },
        ),
        migrations.CreateModel(
            name='CustomStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_status', models.CharField(db_index=True, max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Кастомизируемый статус',
                'verbose_name_plural': 'Кастомизируемые статусы',
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(db_index=True, max_length=120)),
                ('passport_details', models.CharField(max_length=10)),
                ('date_of_birth', models.DateField(verbose_name='Дата рождения')),
                ('driver_license_number', models.CharField(max_length=12)),
            ],
            options={
                'verbose_name': 'Водитель',
                'verbose_name_plural': 'Водители',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('W', 'В работе'), ('P', 'В ожидании'), ('A', 'В архиве'), ('N', 'Не использован')], max_length=1, verbose_name='Статус')),
                ('number_of_document', models.CharField(db_index=True, max_length=100, verbose_name='Номер документа')),
                ('title', models.CharField(max_length=100, verbose_name='Название документа')),
                ('date_start', models.DateField(verbose_name='Дата начала')),
                ('date_end', models.DateField(blank=True, verbose_name='Дата окончания')),
                ('comment_for_access_office', models.TextField(blank=True, verbose_name='Комментарий бюро пропусков')),
                ('comment_for_security', models.TextField(blank=True, verbose_name='Комментарий охраны')),
                ('comment_import', models.TextField(blank=True, verbose_name='Комментарий ввоза | вноса')),
                ('comment_export', models.TextField(blank=True, verbose_name='Комментарий вывоза | выноса')),
                ('document_file', models.FileField(upload_to='documents/', verbose_name='Файл документа')),
                ('auto', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='access_office.automobile', verbose_name='Автомобиль')),
                ('crossing_point_name', models.ManyToManyField(to='access_office.crossingpoint', verbose_name='Пропускной пункт')),
                ('custom_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='access_office.customstatus', verbose_name='Кастомизируемый статус')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
        migrations.AddField(
            model_name='automobile',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='access_office.driver', verbose_name='Водитель'),
        ),
    ]
