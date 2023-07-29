from django.db import models


class CrossingPoint(models.Model):
    crossing_point_name = models.CharField(max_length=100, db_index=True, unique=True)

    def __str__(self):
        return self.crossing_point_name

    class Meta:
        verbose_name = 'Пропускной пункт'
        verbose_name_plural = 'Пропускные пункты'


class CustomStatus(models.Model):
    custom_status = models.CharField(max_length=100, db_index=True, unique=True)

    def __str__(self):
        return self.custom_status

    class Meta:
        verbose_name = 'Кастомизируемый статус'
        verbose_name_plural = 'Кастомизируемые статусы'


class Document(models.Model):
    status_choices = (
        ('W', 'В работе'),
        ('P', 'В ожидании'),
        ('A', 'В архиве'),
        ('N', 'Не использован')
    )

    status = models.CharField('Статус', max_length=1, choices=status_choices, blank=True)
    number_of_document = models.CharField('Номер документа', max_length=100, db_index=True)
    custom_status = models.ForeignKey('CustomStatus', on_delete=models.CASCADE, verbose_name='Кастомизируемый статус')
    title = models.CharField('Название документа', max_length=100)
    date_start = models.DateField('Дата начала')
    date_end = models.DateField('Дата окончания', blank=True)
    comment_for_access_office = models.TextField('Комментарий бюро пропусков', blank=True)
    comment_for_security = models.TextField('Комментарий охраны', blank=True)
    comment_import = models.TextField('Комментарий ввоза | вноса', blank=True)
    comment_export = models.TextField('Комментарий вывоза | выноса', blank=True)
    crossing_point_name = models.ManyToManyField('CrossingPoint', verbose_name='Пропускной пункт')
    document_file = models.FileField('Файл документа', upload_to='documents/')
    auto = models.ForeignKey('Automobile', on_delete=models.CASCADE, verbose_name='Автомобиль', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class Automobile(models.Model):
    license_plate = models.CharField(max_length=9, db_index=True)
    car_registration_number = models.CharField(max_length=10)
    car_brand = models.CharField(max_length=40)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE, verbose_name='Водитель')

    def __str__(self):
        return self.license_plate + ' - ' + self.driver.full_name

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'


class Driver(models.Model):
    full_name = models.CharField(max_length=120, db_index=True)
    passport_details = models.CharField(max_length=10)
    date_of_birth = models.DateField('Дата рождения')
    driver_license_number = models.CharField(max_length=12)

    def __str__(self):
        return f'{self.full_name} - {self.passport_details}'

    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'
