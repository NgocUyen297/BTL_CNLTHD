from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % obj.image.name) if request else ''


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='avatar')

    def get_image(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            return request.build_absolute_uri('/static/%s' % obj.avatar.name) if request else ''

    def create(self, validated_data):
        data = validated_data.copy()
        u = CustomUser(**data)
        u.set_password(u.password)
        u.save()
        return u

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'avatar', 'image', 'email', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': 'True'}
        }


class SinhVienSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj.user
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }

    class Meta:
        model = SinhVien
        fields = ['ma_sv', 'user', 'lop_hoc']
        extra_kwargs = {
            'ma_sv': {'write_only': 'True'}
        }


class LopHocSerializer(serializers.ModelSerializer):

    class Meta:
        model = LopHoc
        fields = ['ma_lop', 'ten_lop', 'giang_vien']


class GiangVienSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj.user
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }

    class Meta:
        model = GiangVien
        fields = ['ma_gv',  'user']


class MonHocSerializer(serializers.ModelSerializer):

    class Meta:
        model = MonHoc
        fields = ['ma_mon',  'ten_mon', 'giang_vien', 'cot_diem']


class BangThietKeMonHocSerializer(serializers.ModelSerializer):
    hoc_ky = serializers.SerializerMethodField()

    def get_hoc_ky(self, obj):
        hoc_ky = obj.ky_hoc
        return {
            'name': hoc_ky.name,
        }

    class Meta:
        model = MonHoc
        fields = ['ma_mon',  'ten_mon', 'giang_vien', 'cot_diem']



class DiemSoSerializer(serializers.ModelSerializer):
    bang_thiet_ke_mon_hoc = serializers.SerializerMethodField()

    def get_bang_thiet_ke_mon_hoc(self, obj):
        bang_thiet_ke_mon_hoc = obj.bang_thiet_ke_mon_hoc
        return {
            'id': bang_thiet_ke_mon_hoc.id
        }

    class Meta:
        model = DiemSo
        fields = ['diem',  'sinh_vien', 'bang_thiet_ke_mon_hoc']

