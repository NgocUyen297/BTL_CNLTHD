from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from .models import *


class CustomUserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if obj.password:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.register(SinhVien)
admin.site.register(GiangVien)
admin.site.register(MonHoc)
admin.site.register(BangThietKeMonHoc)
admin.site.register(CotDiem)
admin.site.register(HocKy)
admin.site.register(DiemSo)
admin.site.register(LopHoc)
admin.site.register(CustomUser, CustomUserAdmin)
