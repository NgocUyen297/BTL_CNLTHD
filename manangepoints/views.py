from rest_framework import viewsets, generics, parsers, permissions
from rest_framework.decorators import action
from rest_framework.views import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from .perms import *


class SinhVienViewSet(viewsets.ViewSet, generics.RetrieveAPIView,
                      generics.DestroyAPIView):
    queryset = SinhVien.objects.all()
    serializer_class = SinhVienSerializer

    def get_permissions(self):
        if self.action in ['create_sinh_vien']:
            return [permissions.IsAdminUser()]

        if self.action in ['update_sinh_vien', 'find_mon_hoc']:
            return [SinhVienorGiangVien()]

        return [permissions.AllowAny()]

    @action(methods=['post'], detail=False, url_path='create-sinh-vien')
    def create_sinh_vien(self, request):
        user = request.data.pop('user')
        if user is not None:
            user_email = user.get('email')
            if user_email is not None:
                user_email = user_email.lower()
                if not user_email.endswith('ou.edu.vn'):
                    return Response({'error': 'Email must end with ou.edu.vn'}, status=status.HTTP_400_BAD_REQUEST)

        avatar = user.get('avatar')
        if not avatar:
            return Response("Avatar khong ton tai", status=status.HTTP_400_BAD_REQUEST)

        lop_hoc = LopHoc.objects.get(pk=request.data.get('lop_hoc'))

        if lop_hoc is None:
            return Response("The class is not exit", status=status.HTTP_400_BAD_REQUEST)

        u = CustomUser(**user)
        u.set_password(u.password)
        u.is_active = False
        u.save()

        student = SinhVien.objects.create(user=u, ma_sv=u.id, lop_hoc=lop_hoc)
        student.save()

        return Response(SinhVienSerializer(student, context={'request': request}).data)

    @action(methods=['put'], detail=True, url_path='update_sinh_vien')
    def update_sinh_vien(self, request, *args, **kwargs):
        sinhvien = self.get_object()
        sinh_vien_user = sinhvien.user
        request_user = request.data.pop('user')

        if request_user is not None:
            user_email = request_user.get('email')
            if user_email is not None:
                user_email = user_email.lower()
                if not user_email.endswith('ou.edu.vn'):
                    return Response({'error': 'Email must end with ou.edu.vn'}, status=status.HTTP_400_BAD_REQUEST)

        if request.method.__eq__('PUT'):
            for k, v in request_user.items():
                if k.__eq__('password'):
                    sinh_vien_user.set_password(k)
                else:
                    setattr(sinh_vien_user, k, v)

            sinh_vien_user.is_active = True
            sinh_vien_user.save()

            for k, v in request.data.items():
                if k.__eq__('lop_hoc'):
                    lop_hoc = LopHoc.objects.get(pk=request.data.get('lop_hoc'))
                    sinhvien.lop_hoc = lop_hoc
                else:
                    setattr(sinhvien, k, v)
            sinhvien.save()

        return Response(SinhVienSerializer(sinhvien, context={'request': request}).data)

    @action(methods=['get'], detail=True, url_path='find_mon_hoc')
    def find_mon_hoc(self, request, *args, **kwargs):
        sinhvien = self.get_object()
        diemSo = sinhvien.diemso_set.all()
        cac_mon_hoc = set([])
        for diem in diemSo:
            cac_mon_hoc.add(diem.bang_thiet_ke_mon_hoc.mon_hoc)

        return Response(MonHocSerializer(cac_mon_hoc, many=True, context={'request': request}).data)


class LopHocViewSet(viewsets.ModelViewSet):
    queryset = LopHoc.objects.all()
    serializer_class = LopHocSerializer

    def get_permissions(self):
        if self.action in ['sinhvien']:
            return [LopHocOwner()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=True, url_path='get_sinhvien')
    def get_sinhvien(self, request, pk):
        lop_hoc = self.get_object()
        sinhvien = lop_hoc.sinh_vien.all()
        return Response(SinhVienSerializer(sinhvien, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


class GiangVienViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = GiangVien.objects.all()
    serializer_class = GiangVienSerializer

    def get_permissions(self):
        if self.action in ['find_sinhvien']:
            return [IsStaff()]

        if self.action in ['find_lop_hoc']:
            return [IsGiangVienOrAdmin()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='find_sinhvien')
    def find_sinhvien(self, request, pk):
        first_name = request.query_params.get('firstname', '')
        last_name = request.query_params.get('lastname', '')
        ma_sv = request.query_params.get('ma_sv', '')
        sinhvien = SinhVien.objects.all()
        if first_name != '':
            sinhvien = sinhvien.filter(user__first_name__icontains=first_name)

        if last_name != '':
            sinhvien = sinhvien.filter(user__last_name__icontains=last_name)

        if ma_sv != '':
            sinhvien = sinhvien.filter(ma_sv=ma_sv)

        return Response(SinhVienSerializer(sinhvien, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='find_lop_hoc')
    def find_lop_hoc(self, request, pk):
        giang_vien = self.get_object()
        cac_lop_hoc = giang_vien.lop_hoc_giang_day.all()

        return Response(LopHocSerializer(cac_lop_hoc, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class MonHocViewSet(viewsets.ModelViewSet):
    queryset = MonHoc.objects.all()
    serializer_class = MonHocSerializer

    def get_permissions(self):
        if self.action in ['find_diem_so']:
            return [IsSinhVienOrGVMonHoc()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=True, url_path='find_diem_so')
    def find_diem_so(self, request, pk):
        ma_sv = request.query_params.get('ma_sv', '')
        mon_hoc = self.get_object()
        if ma_sv != '':
            sinh_vien = SinhVien.objects.get(ma_sv=ma_sv)
            if sinh_vien is not None:
                diem_so = DiemSo.objects.filter(sinh_vien=sinh_vien, bang_thiet_ke_mon_hoc__mon_hoc=mon_hoc)
            else:
                return Response({'error': 'Sinh Vien khong ton tai'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            diem_so = DiemSo.objects.filter(sinh_vien=request.user.sinhvien, bang_thiet_ke_mon_hoc__mon_hoc=mon_hoc)

        return Response(DiemSoSerializer(diem_so, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['current_user']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get', 'put'], detail=False, url_path='current-user')
    def current_user(self, request):
        u = request.user
        if request.method.__eq__('PUT'):
            for k, v in request.data.items():
                if k.__eq__('password'):
                    u.set_password(k)
                else:
                    setattr(u, k, v)
            u.save()

        return Response(UserSerializer(u, context={'request': request}).data)
