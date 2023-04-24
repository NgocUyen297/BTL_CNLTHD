from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class UserBaseModel(models.Model):
    avatar = models.ImageField(upload_to='users/%Y/%m', null=True)

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email không thể bỏ trống')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, UserBaseModel):
    objects = CustomUserManager()
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.email

    class Meta:
        unique_together = ('email', 'username')


class SinhVien(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ma_sv = models.CharField(max_length=10, unique=True)
    lop_hoc = models.ForeignKey('LopHoc', on_delete=models.CASCADE, related_name='sinh_vien', null=True)

    def __str__(self):
        return self.user.email


class GiangVien(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ma_gv = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.user.email


class LopHoc(models.Model):
    ma_lop = models.CharField(max_length=10, unique=True)
    ten_lop = models.CharField(max_length=120, unique=True)
    giang_vien = models.ForeignKey(GiangVien, on_delete=models.SET_NULL, related_name='lop_hoc_giang_day', null=True)

    def __str__(self):
        return self.ma_lop


class MonHoc(models.Model):
    ma_mon = models.CharField(max_length=10, unique=True)
    ten_mon = models.CharField(max_length=50)
    giang_vien = models.ForeignKey(GiangVien, on_delete=models.SET_NULL, null=True)
    cot_diem = models.ManyToManyField('CotDiem', through='BangThietKeMonHoc', related_name='mon_hoc')

    def __str__(self):
        return self.ten_mon


class HocKy(models.Model):
    name = models.CharField(max_length=255, null=True)
    start_at = models.DateTimeField(auto_now=True)
    end_at = models.DateTimeField()


class CotDiem(models.Model):
    name = models.CharField(max_length=255)
    ghi_chu = models.TextField()

    def __str__(self):
        return self.name


class BangThietKeMonHoc(models.Model):
    ky_hoc = models.ForeignKey(HocKy, on_delete=models.CASCADE)
    cot_diem = models.ForeignKey(CotDiem, on_delete=models.CASCADE, null=True)
    mon_hoc = models.ForeignKey(MonHoc, on_delete=models.CASCADE, related_name='bang_thiet_ke_diem_so')
    giang_vien = models.ForeignKey(GiangVien, on_delete=models.CASCADE, related_name='giang_vien', null=True)

    def __str__(self):
        return f"Diem so {self.mon_hoc} - Ky hoc {self.ky_hoc}"


class DiemSo(models.Model):
    diem = models.FloatField(null=True, default=None, blank=True)
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)
    bang_thiet_ke_mon_hoc = models.ForeignKey(BangThietKeMonHoc, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.diem}'


class FileCSV(models.Model):
    file = models.FileField(upload_to='csv/')
    lop_hoc = models.ForeignKey(LopHoc, on_delete=models.CASCADE)
    sinh_vien = models.ForeignKey(SinhVien, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name
