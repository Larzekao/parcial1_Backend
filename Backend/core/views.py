from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from . import models, serializers

Usuario = get_user_model()


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow read for any, write for admin users."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class RolViewSet(viewsets.ModelViewSet):
    queryset = models.Rol.objects.all()
    serializer_class = serializers.RolSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['nombre']


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.select_related('rol').all()
    serializer_class = serializers.UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['username', 'email', 'telefono']
    filterset_fields = ['estado', 'rol']


class ResidenciaViewSet(viewsets.ModelViewSet):
    queryset = models.Residencia.objects.all()
    serializer_class = serializers.ResidenciaSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['nombre', 'direccion']


class ResidenteViewSet(viewsets.ModelViewSet):
    queryset = models.Residente.objects.select_related('residencia', 'usuario').all()
    serializer_class = serializers.ResidenteSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['nombre', 'usuario__username']
    filterset_fields = ['residencia', 'tipo']


class MascotaViewSet(viewsets.ModelViewSet):
    queryset = models.Mascota.objects.select_related('residencia').all()
    serializer_class = serializers.MascotaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['residencia']


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = models.Vehiculo.objects.select_related('residente').all()
    serializer_class = serializers.VehiculoSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['placa', 'modelo']
    filterset_fields = ['residente']


class VisitanteViewSet(viewsets.ModelViewSet):
    queryset = models.Visitante.objects.select_related('residente').all()
    serializer_class = serializers.VisitanteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['residente', 'fecha']
    search_fields = ['nombre', 'motivo']


class AreaComunViewSet(viewsets.ModelViewSet):
    queryset = models.AreaComun.objects.all()
    serializer_class = serializers.AreaComunSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['nombre']
    filterset_fields = ['estado']


class HorarioViewSet(viewsets.ModelViewSet):
    queryset = models.Horario.objects.select_related('area').all()
    serializer_class = serializers.HorarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['area', 'dia']


class ReglaViewSet(viewsets.ModelViewSet):
    queryset = models.Regla.objects.select_related('area').all()
    serializer_class = serializers.ReglaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['area']


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = models.Reserva.objects.select_related('residente', 'area').all()
    serializer_class = serializers.ReservaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['estado', 'residente', 'area', 'fecha']


class ConceptoPagoViewSet(viewsets.ModelViewSet):
    queryset = models.ConceptoPago.objects.all()
    serializer_class = serializers.ConceptoPagoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['tipo']


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = models.Factura.objects.select_related('residente').prefetch_related('detalles').all()
    serializer_class = serializers.FacturaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['estado', 'residente', 'fecha']


class DetalleFacturaViewSet(viewsets.ModelViewSet):
    queryset = models.DetalleFactura.objects.select_related('factura', 'concepto').all()
    serializer_class = serializers.DetalleFacturaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['factura', 'concepto']


class PersonalViewSet(viewsets.ModelViewSet):
    queryset = models.Personal.objects.all()
    serializer_class = serializers.PersonalSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['nombre', 'cargo']


class TareaViewSet(viewsets.ModelViewSet):
    queryset = models.Tarea.objects.select_related('personal').all()
    serializer_class = serializers.TareaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['estado', 'personal', 'fecha_programada']
    search_fields = ['nombre']