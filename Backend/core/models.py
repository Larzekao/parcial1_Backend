from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    telefono = models.CharField(max_length=30, blank=True)
    estado = models.BooleanField(default=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Residencia(TimestampedModel):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


class Residente(TimestampedModel):
    TIPOS = [
        ('propietario', 'Propietario'),
        ('inquilino', 'Inquilino'),
        ('otro', 'Otro'),
    ]

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='residente', blank=True, null=True)
    residencia = models.ForeignKey(Residencia, on_delete=models.CASCADE, related_name='residentes')
    nombre = models.CharField(max_length=150)
    sexo = models.CharField(max_length=10, blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPOS)

    def __str__(self):
        return self.nombre


class Mascota(TimestampedModel):
    residencia = models.ForeignKey(Residencia, on_delete=models.CASCADE, related_name='mascotas')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Vehiculo(TimestampedModel):
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='vehiculos')
    placa = models.CharField(max_length=20, unique=True)
    modelo = models.CharField(max_length=100)
    color = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.placa


class Visitante(TimestampedModel):
    residente = models.ForeignKey(Residente, on_delete=models.SET_NULL, null=True, related_name='visitantes')
    nombre = models.CharField(max_length=150)
    motivo = models.CharField(max_length=255, blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    foto = models.ImageField(upload_to='visitantes/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.fecha})"


class AreaComun(TimestampedModel):
    nombre = models.CharField(max_length=150)
    costo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=50, default='disponible')

    def __str__(self):
        return self.nombre


class Horario(TimestampedModel):
    area = models.ForeignKey(AreaComun, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=50)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        unique_together = ('area', 'dia', 'hora_inicio', 'hora_fin')

    def __str__(self):
        return f"{self.area.nombre} - {self.dia}"


class Regla(TimestampedModel):
    area = models.ForeignKey(AreaComun, on_delete=models.SET_NULL, null=True, blank=True, related_name='reglas')
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo


class Reserva(TimestampedModel):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='reservas')
    area = models.ForeignKey(AreaComun, on_delete=models.CASCADE, related_name='reservas')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    costo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    referencia_pago = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['-fecha', '-hora_inicio']
        unique_together = ('area', 'fecha', 'hora_inicio', 'hora_fin')

    def __str__(self):
        return f"{self.area.nombre} - {self.fecha}"


class ConceptoPago(TimestampedModel):
    TIPOS = [
        (1, 'Cuota de mantenimiento'),
        (2, 'Multa'),
        (3, 'Reserva de area comun'),
        (4, 'Otro'),
    ]

    nombre = models.CharField(max_length=150)
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Factura(TimestampedModel):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida'),
        ('anulada', 'Anulada'),
    ]

    residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='facturas')
    fecha = models.DateField()
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    notas = models.TextField(blank=True)

    def __str__(self):
        return f"Factura {self.id} - {self.residente.nombre}"


class DetalleFactura(TimestampedModel):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    concepto = models.ForeignKey(ConceptoPago, on_delete=models.PROTECT, related_name='detalles')
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.monto * self.cantidad

    def __str__(self):
        return f"{self.concepto.nombre} ({self.factura_id})"


class Personal(TimestampedModel):
    nombre = models.CharField(max_length=150)
    cargo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.nombre


class Tarea(TimestampedModel):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    personal = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha_programada = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return self.nombre
