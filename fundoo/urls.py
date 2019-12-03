# Learn more
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
from .swagger_schema import SwaggerSchemaView
# from .routers import router
from rest_framework_simplejwt import views as jwt_views


schema_view = get_swagger_view(title='Fundoo Application')

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include(router.urls)),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('rest_framework.urls')),
    path('', schema_view),
    path('', include('login.urls')),
    path('note/', include('note.urls')),
    path('social-login/', include('sociallogin.urls')),
    # path('api/'include('rest_framework'))
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # url('', include('notes.urls')),
    # url('contacts-list', include('fun.urls')),
    url(r'^swagger-schema/', SwaggerSchemaView.as_view()),
    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

]
