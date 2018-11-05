# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from models import Workday
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


def index(request):
    return HttpResponse('<h1>punchtime!</h1>')


class WorkdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Workday
        fields = ('date', 'intime', 'outtime', 'total')

        read_only_fields = ('total',)


class WorkdayViewSet(viewsets.ModelViewSet):
    serializer_class = WorkdaySerializer

    def get_queryset(self):
        queryset = Workday.objects.all()

        start_date = self.request.query_params.get('start_date', None)
        if start_date is not None:
            queryset = queryset.filter(date__gte=start_date)

        end_date = self.request.query_params.get('end_date', None)
        if end_date is not None:
            queryset = queryset.filter(date__lte=end_date)

        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Workday.objects.all()
        wd = get_object_or_404(queryset, pk=pk)
        serializer = WorkdaySerializer(wd)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def total_sum(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        try:
            total_seconds = queryset.aggregate(total_sum=Sum('total'))['total_sum'].seconds
        except AttributeError:
            total_seconds = 0

        h, s = divmod(total_seconds, 3600)
        m, s = divmod(s, 60)
        total_time = "%02d:%02d:%02d" % (h, m, s)

        return Response(dict(
            total_sum=total_time
        ))


router = routers.DefaultRouter()
router.register(r'workdays', WorkdayViewSet, base_name='workday')
