from django.urls import path
from .api.views import CompraAPIView
from .views import CompraView, CompraRapidaView, compra_rapida_fbv

urlpatterns = [
    # PASO 1: FBV Spaghetti (Antipatrón)
    path('compra-rapida-fbv/<int:libro_id>/', compra_rapida_fbv, name='compra_rapida_fbv'),
    
    # PASO 2: CBV (Mejor separación de responsabilidades)
    path('compra-rapida-cbv/<int:libro_id>/', CompraRapidaView.as_view(), name='compra_rapida_cbv'),
    
    # PASO 3: CBV con inyección de dependencias y Service Layer
    path('compra/<int:libro_id>/', CompraView.as_view(), name='finalizar_compra'),
    
    # API REST
    path('api/v1/comprar/', CompraAPIView.as_view(), name='api_comprar'),
]