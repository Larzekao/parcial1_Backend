from django.contrib import admin

from . import models


@admin.register(models.Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'telefono', 'estado', 'rol')
    search_fields = ('username', 'email', 'telefono')
    list_filter = ('estado', 'rol')


@admin.register(models.Rol)
class RolAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(models.Residencia)
class ResidenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion')
    search_fields = ('nombre', 'direccion')


class DetalleFacturaInline(admin.TabularInline):
    model = models.DetalleFactura
    extra = 1


@admin.register(models.Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'residente', 'fecha', 'monto_total', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('residente__nombre',)
    inlines = [DetalleFacturaInline]


admin.site.register([
    models.Residente,
    models.Mascota,
    models.Vehiculo,
    models.Visitante,
    models.AreaComun,
    models.Horario,
    models.Regla,
    models.Reserva,
    models.ConceptoPago,
    models.DetalleFactura,
    models.Personal,
    models.Tarea,
])