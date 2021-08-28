from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # api/profileみたいな形でアクセスできます。
    path('api/', include('api.urls')),
    # jwtをdjoserを使う場合authen/と呼び出すとjwtトークンを取得することができます。
    path('authen/', include('djoser.urls.jwt')),
]
# アバターの画像等をmediaの中に保存しているのでアクセスできるようにする
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
