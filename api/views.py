# ModelViewSet CRUDを全て使いたい場合は、こちらを使うと便利
# 単一モデルに対するCRUD(Create, Read, Update, Delete)を標準装備

# 汎用APIView CRUDのどれかに特化した機能を使いたい場合に使用
# CreateAPIView
# ListAPIView
# DestroyAPIView
# UpdateAPIView... etc
# Create your views here.

# 必要なモジュールをインポートする
# generics汎用のview
from rest_framework import generics
from rest_framework import viewsets
# jwtの認証に全体に適応させているため必ず認証を通らないといけない設定になるため
# 新規でユーザーを作成するところはユーザーができていないのでその人はユーザーviewにアクセスできるようにする必要がある
# そのためのAllowAnyで上書きを実施する
from rest_framework.permissions import AllowAny
# シリアライズ
from . import serializers
# モデル
from .models import Profile, Post, Comment


# 新規ユーザーを作成するために作成に特化したもの
# 作成するだけなのでCreateAPIViewを呼び出す
class CreateUserView(generics.CreateAPIView):
    # ユーザーを作成するためにDBの中継のシリアライザーはUserSerializerが必要
    serializer_class = serializers.UserSerializer
    # 誰でもアクセスできるようにする
    permission_classes = (AllowAny,)


# プロフィールに関するView
# 新規作成や更新などができるようにするなのでCRUDが全て入っているModelViewSetを使用している
class ProfileViewSet(viewsets.ModelViewSet):
    # 全件取得する
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    # プロフィールを新規で作成する時に呼び出されるメソッド
    # userProfileに対して現在ログインしているユーザーを当てはめる処理
    def perform_create(self, serializer):
        serializer.save(userProfile=self.request.user)


# ログインしているユーザーのプロフィール情報を返すView
class MyProfileListView(generics.ListAPIView):
    # プロフィールを全件取得する
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    # ログインしているユーザーのみを取得する
    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)


# 投稿に対するView
class PostViewSet(viewsets.ModelViewSet):
    # Postに関して全件取得する
    queryset = Post.objects.all()
    # シリアライザーはPostSerializerを当てはめている
    serializer_class = serializers.PostSerializer

    # 現在ログインしているユーザーを取得する
    def perform_create(self, serializer):
        serializer.save(userPost=self.request.user)


# コメントに対するView
class CommentViewSet(viewsets.ModelViewSet):
    # 全件取得
    queryset = Comment.objects.all()
    # コメントシリアライザーを取得
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        # ログインしているユーザーを取得する
        serializer.save(userComment=self.request.user)
