from django.contrib import admin
# アドミンを作成するのに必要な機能をimportする
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
# 開発者が作成したモデルについてはインポートするだけで使用可能になる
# 階層がmodelsとadminが同階層にあるため.と記載する
from . import models


# Register your models here.

# UserAdminを追記する必要がある
# 項目はそれぞれダッシュボードと対応している
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email']
    fieldsets = (
        # (Title, 表示項目)の関係性になっている
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ()}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


# usermodelは特殊
# オーバーライドを実施しているため結構複雑になっており
# adminの画面もオーバーライドする必要がある
admin.site.register(models.User, UserAdmin)
# あとはこれだけでいける
admin.site.register(models.Profile)
admin.site.register(models.Post)
admin.site.register(models.Comment)
