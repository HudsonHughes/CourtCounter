from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from django.shortcuts import render

from court_counter.serializers import *


# Create your views here.

def view_home(request):

	return render(request, 'home.html', {})


def view_file(request, filename=None):
	pass


def view_open_menu(request):
	pass


def view_delete_menu(request):
	pass


class FileViewSet(viewsets.ModelViewSet):
	queryset = File.objects.all()
	serializer_class = FileSerializer

	def list(self, request):
		queryset = self.filter_queryset(self.get_queryset().filter())
		queryset.filter(name__icontains=request.query_params.get('query', ''))
		if request.query_params.get('sort', '') == 'last_modified':
			queryset.order_by(('-' if request.query_params.get('reverse', 'true') == 'true' else '') + 'last_modified')
		elif request.query_params.get('sort', '') == 'created':
			queryset.order_by(('-' if request.query_params.get('reverse', 'true') == 'true' else '') + 'created')
		elif request.query_params.get('sort', '') == 'name':
			queryset.order_by(('-' if request.query_params.get('reverse', 'true') == 'true' else '') + 'query')
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	def create(self, request, pk=None):
		return Response({}, status=status.HTTP_404_NOT_FOUND)

	def update(self, request, pk=None):
		return Response({}, status=status.HTTP_404_NOT_FOUND)

	def partial_update(self, request, pk=None):
		return Response({}, status=status.HTTP_404_NOT_FOUND)


class ShotViewSet(viewsets.ModelViewSet):
	queryset = Shot.objects.all()
	serializer_class = ShotSerializer

	def list(self, request, filename=None):
		queryset = self.filter_queryset(self.get_queryset()).filter(filename=filename)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	def create(self, request, filename=None):
		request.data["filename"] = filename
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		return Response({"new_count": Shot.objects.filter(filename=filename).count(), "new_object": serializer.data},
		                status=status.HTTP_201_CREATED, headers=headers)

	@detail_route(methods=['post'])
	def set_password(self, request, filename=None):
		return Response({})

	@list_route()
	def recent_users(self, request, filename=None):
		return Response({})
