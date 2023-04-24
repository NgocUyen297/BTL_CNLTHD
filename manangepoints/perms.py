from rest_framework import permissions


class IsSuperUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return bool(request.user.is_superuser)
#         Nay chua xong chua tim cac them cac quyen cho admin


class LopHocOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, lop_hoc):
        return request.user and request.user == lop_hoc.giang_vien


class SinhVienorGiangVien(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, sinh_vien):
        return sinh_vien.user == request.user or sinh_vien.lop_hoc.giang_vien == request.user


class IsStaff(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_staff.__eq__(True)


class IsGiangVienOrAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, giang_vien):
        return bool(giang_vien == request.user.giangvien)


class IsSinhVienOrGVMonHoc(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, mon_hoc):
        return bool(request.user.is_sinhvien)
