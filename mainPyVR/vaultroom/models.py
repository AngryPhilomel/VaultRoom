from django.db import models

class Storages(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название склада')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "%s" % self.pk

    class Meta:
        verbose_name_plural = 'Склады'
        verbose_name = 'Склад'
        ordering = ['name']


class Products(models.Model):
    LM = models.IntegerField(verbose_name='LM код')
    barcode = models.IntegerField(verbose_name='Штрихкод')
    name = models.CharField(max_length=100, verbose_name='Наименование')
    department = models.IntegerField(verbose_name='Номер отдела')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Товар'
        verbose_name = 'Товар'
        ordering = ['name']


class Stock(models.Model):
    storage = models.ForeignKey('Storages', on_delete=models.PROTECT, verbose_name='Склад')
    product = models.ForeignKey('Products', on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.IntegerField(verbose_name='Количество')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name_plural = 'Товар на стоке'
        verbose_name = 'Товар на стоке'
        ordering = ['storage']


class Done(models.Model):
    product = models.ForeignKey('Products', on_delete=models.PROTECT, verbose_name='Выданный товар')
    quantity = models.IntegerField(verbose_name='Количество выданного товара')
    time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время выдачи')

    class Meta:
        verbose_name_plural = 'Выданный товар'
        verbose_name = 'Выданный товар'
        ordering = ['-time']

class Control(models.Model):
    POSTS = (
        ('Доставка', 'Доставка'),
        ('Выдача', 'Выдача'),
    )
    check = models.IntegerField(verbose_name='Номер чека', unique=True)
    post = models.CharField(verbose_name='Пост', choices=POSTS, blank=False, max_length=10)
    comment = models.CharField(verbose_name='Коментарий', blank=True, max_length=50)
    pallet = models.IntegerField(verbose_name='Кол-во паллет', default=0)
    time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Время выдачи')

    class Meta:
        verbose_name_plural = 'Выданные чеки'
        verbose_name = 'Выданный чек'
        ordering = ['-time']