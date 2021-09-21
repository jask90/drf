from django.db import models


class Hotel(models.Model):
    code = models.CharField(max_length=32, unique=True, verbose_name=u'código')
    name = models.CharField(max_length=255, verbose_name=u'nombre')

    class Meta:
        ordering = ['name']
        verbose_name = u'Hotel'
        verbose_name_plural = u'Hoteles'

    def __str__(self):
        return f'{self.name}'


class Room(models.Model):
    code = models.CharField(max_length=32, unique=True, verbose_name=u'código')
    name = models.CharField(max_length=255, verbose_name=u'nombre')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, verbose_name=u'hotel')

    class Meta:
        ordering = ['name']
        verbose_name = u'Habitación'
        verbose_name_plural = u'Habitaciones'

    def __str__(self):
        return f'{self.hotel} - {self.name}'


class Rate(models.Model):
    code = models.CharField(max_length=32, unique=True, verbose_name=u'código')
    name = models.CharField(max_length=255, verbose_name=u'nombre')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name=u'room')

    class Meta:
        ordering = ['name']
        verbose_name = u'Tarifa'
        verbose_name_plural = u'Tarifas'

    def __str__(self):
        return f'{self.room} - {self.name}'


class Inventory(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'nombre')
    rate = models.ForeignKey(Rate, on_delete=models.CASCADE, verbose_name=u'tarifa')
    date = models.DateField(verbose_name='fecha')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name='precio')
    quota = models.PositiveIntegerField(default=0, verbose_name=u'cupo')

    class Meta:
        ordering = ['name']
        verbose_name = u'Inventario'
        verbose_name_plural = u'Inventarios'

    def __str__(self):
        return f'{self.rate} - {self.name}'
