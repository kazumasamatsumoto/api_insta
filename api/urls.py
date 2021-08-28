# アプリケーションごとにパスを設定する必要がある
# 必要なパッケージをインポートする
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'user'

router = DefaultRouter()
# 新しくrouterに登録します。
# viewsetsで作成したviewの登録方法はこちら
router.register('profile', views.ProfileViewSet)
router.register('post', views.PostViewSet)
router.register('comment', views.CommentViewSet)

# genericで作成したviewの登録方法はこちら
urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    # ルートのパスにきた時にrouterを読みにいく
    path('', include(router.urls))
]
