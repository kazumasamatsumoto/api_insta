from django.db import models
# emailを使って認証を使いたい場合は以下を使用してオーバーライドする必要があります。
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


# Create your models here.

def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.userProfile.id) + str(instance.nickName) + str(".") + str(ext)])


def upload_post_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['posts', str(instance.userPost.id) + str(instance.title) + str(".") + str(ext)])


# UserManagerモデルをemailが使用できるようにオーバーライドします。
class UserManager(BaseUserManager):
    # djangoでもともとあるcreate_userの第二引数にはusernameが入っているが
    # 今回はemailとパスワードで認証できるようにするために第二引数をemailとする
    def create_user(self, email, password=None):
        # emailがないときはエラーを吐くようにする
        if not email:
            raise ValueError('email is must')

        # modelというメソッドを使ってインスタンスを作成してuserに代入する
        # この時にemailを渡すときに正規化を実施する
        # emailは小文字で表現されるため、大文字を小文字に変更したりする
        # 正規化からのインスタンス作成
        user = self.model(email=self.normalize_email(email))
        # パスワードをハッシュ化してから設定
        user.set_password(password)
        # 作成したインスタンスをデータベースに設定
        user.save(using=self._db)
        return user

    # UserManagerをオーバーライドした場合はcreate_superuserもオーバーライドする必要がある
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        # 権限を付与して保存する
        # djangoの権限は3種類ある
        # Active is_activeを指定するTrue/Falseでアカウントの有効/無効切替
        # 無効にするとログインできなくなります。
        # Staff権限 is_staffに指定するTrue/FalseでStaff権限の有効/無効切替
        # Staff権限は、AdminのDashboardにログインする権限になります
        # Superuser権限 is_superuserに指定するTrue/Falseで有効/無効切替
        # Superuserは、AdminのDashboardにログインする権限に加えデータベースの内容を変更できるなど全権限を持ちます。
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# UserModelの作成
# デフォルトの状態のusernameからemailに変更するようにする
class User(AbstractBaseUser, PermissionsMixin):
    # 文字の長さを50,emailがIDの役割も果たすのでuniqueをTrueにする（重複するemailでの登録が不可になります）
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    # Adminにログインする権限は不要なのでFalse
    is_staff = models.BooleanField(default=False)

    # Userのクラスの中にUserManagerがある状態をネストという
    # UserManagerのcreate_userのようなメソッドを呼び出すことができる
    objects = UserManager()

    # 今回はusernameではなくemailを使いたいのでオーバーライドします。
    USERNAME_FIELD = 'email'

    # __str__(Pythonの特殊関数）
    # emailの内容を文字列として返す
    # __str__ Userクラスを呼び出すときの返り値がこのメールアドレスになる
    def __str__(self):
        return self.email


class Profile(models.Model):
    nickName = models.CharField(max_length=20)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    # アバターの画像イメージを登録する
    #
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)


class Post(models.Model):
    title = models.CharField(max_length=100)
    userPost = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='userPost', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked', blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=100)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userComment', on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
