# clientからDBへデータを渡すときのバリデーションや
# DBからclientへデータを渡すときのJSON加工などを実施してくれる便利なもの

# get_user_modelとserializersと各モデルをインポート
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment


# 各モデルで定義した内容をシリアライザーの定義が必要。モデルごとにシリアライザーも定義する感じ
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        # エクストラキーワード
        # パスワードに関してはクライアントから読み取れないようにするために
        # write_onlyをtrueにする
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # models.pyで定義したuserモデルからオブジェクトを呼び出して
        # ネスト型になっているのでuserManagerの中のcreate_userを呼び出す
        user = get_user_model().objects.create_user(**validated_data)
        return user


# プロフィールの設定時のシリアライザー
class ProfileSerializer(serializers.ModelSerializer):
    # 読みにくいのでフォーマットして格納する
    created_on = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'nickName', 'userProfile', 'created_on', 'img')
        extra_kwargs = {'userProfile': {'read_only': True}}


# 投稿に対するシリアライザー
class PostSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'userPost', 'created_on', 'img', 'liked')
        extra_kwargs = {'userPost': {'read_only': True}}


# コメントに対するシリアライザー
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'userComment', 'post')
        extra_kwargs = {'userComment': {'read_only': True}}
