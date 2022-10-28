
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('product.urls')),
    # path('c/', include('deliver.urls')),
    path('account/', include("authapp.urls")),
    path('action/', include("cart.urls")),
    path('checkout/', include("checkout.urls")),
    path('user/', include('dashboard.urls')),
    path('payment/', include('payments.urls')),
    path('admin/', admin.site.urls),
]


urlpatterns += static(settings.MEDIA_URL,
                     document_root = settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL,
                     document_root = settings.STATIC_ROOT)
