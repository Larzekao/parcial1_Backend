from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import models

Usuario = get_user_model()


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rol
        fields = '__all__'


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'telefono', 'estado', 'rol', 'password', 'first_name', 'last_name']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class ResidenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Residencia
        fields = '__all__'


class ResidenteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(required=False, allow_null=True)

    class Meta:
        model = models.Residente
        fields = ['id', 'usuario', 'residencia', 'nombre', 'sexo', 'fecha_nacimiento', 'tipo', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        user_data = validated_data.pop('usuario', None)
        residente = models.Residente.objects.create(**validated_data)
        if user_data:
            serializer = UsuarioSerializer(data=user_data)
            serializer.is_valid(raise_exception=True)
            usuario = serializer.save()
            residente.usuario = usuario
            residente.save()
        return residente

    def update(self, instance, validated_data):
        user_data = validated_data.pop('usuario', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if user_data is not None:
            if instance.usuario:
                serializer = UsuarioSerializer(instance=instance.usuario, data=user_data, partial=True)
            else:
                serializer = UsuarioSerializer(data=user_data)
            serializer.is_valid(raise_exception=True)
            usuario = serializer.save()
            instance.usuario = usuario
            instance.save()
        return instance


class MascotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mascota
        fields = '__all__'


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Vehiculo
        fields = '__all__'


class VisitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Visitante
        fields = '__all__'


class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Horario
        fields = '__all__'


class ReglaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Regla
        fields = '__all__'


class AreaComunSerializer(serializers.ModelSerializer):
    horarios = HorarioSerializer(many=True, read_only=True)
    reglas = ReglaSerializer(many=True, read_only=True)

    class Meta:
        model = models.AreaComun
        fields = ['id', 'nombre', 'costo', 'descripcion', 'estado', 'horarios', 'reglas', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'horarios', 'reglas']


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reserva
        fields = '__all__'


class ConceptoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ConceptoPago
        fields = '__all__'


class DetalleFacturaSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = models.DetalleFactura
        fields = ['id', 'factura', 'concepto', 'monto', 'cantidad', 'subtotal', 'created_at', 'updated_at']
        read_only_fields = ['id', 'subtotal', 'created_at', 'updated_at']


class FacturaSerializer(serializers.ModelSerializer):
    detalles = DetalleFacturaSerializer(many=True, required=False)

    class Meta:
        model = models.Factura
        fields = ['id', 'residente', 'fecha', 'monto_total', 'estado', 'notas', 'detalles', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        factura = models.Factura.objects.create(**validated_data)
        self._sync_detalles(factura, detalles_data)
        return factura

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if detalles_data is not None:
            instance.detalles.all().delete()
            self._sync_detalles(instance, detalles_data)
        return instance

    def _sync_detalles(self, factura, detalles_data):
        for detalle in detalles_data:
            models.DetalleFactura.objects.create(factura=factura, **detalle)


class PersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Personal
        fields = '__all__'


class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tarea
        fields = '__all__'