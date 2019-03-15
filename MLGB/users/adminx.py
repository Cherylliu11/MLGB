import xadmin
from xadmin import views
from .models import UserProfile,  UserAddr

class GlobalSetting(object):
    site_title = 'MLGB在线订餐管理系统'
    site_footer = "My Life's Getting Better"
    menu_style = "accordion"

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class UserProfileAdmin(object):
    list_display = ['user_id', 'name', 'mobilephone']
    search_fields = ['user_id', 'mobilephone']
    readonly_fields = ['user_id']

class UserAddrAdmin(object):
    list_display = ['user', 'mobilephone','business', 'address']
    search_fields = ['user', 'mobilephone']
    list_filter = ['user', 'mobilephone']
    model_icon = 'fa fa-users'

xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(UserAddr, UserAddrAdmin)
