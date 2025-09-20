from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'roles', views.RolViewSet)
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'residencias', views.ResidenciaViewSet)
router.register(r'residentes', views.ResidenteViewSet)
router.register(r'mascotas', views.MascotaViewSet)
router.register(r'vehiculos', views.VehiculoViewSet)
router.register(r'visitantes', views.VisitanteViewSet)
router.register(r'areas-comunes', views.AreaComunViewSet)
router.register(r'horarios', views.HorarioViewSet)
router.register(r'reglas', views.ReglaViewSet)
router.register(r'reservas', views.ReservaViewSet)
router.register(r'conceptos-pago', views.ConceptoPagoViewSet)
router.register(r'facturas', views.FacturaViewSet)
router.register(r'detalles-factura', views.DetalleFacturaViewSet)
router.register(r'personal', views.PersonalViewSet)
router.register(r'tareas', views.TareaViewSet)

urlpatterns = router.urls