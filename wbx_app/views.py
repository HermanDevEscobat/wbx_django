from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Lot, User
from .serializers import UserSerializer, CategorySerializer, LotSerializer, EmptySerializer

COUNT_ELEM = 100


@api_view(["PUT"])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def update_user(request, id_tlg):
    user = User.objects.get(id_tlg=id_tlg)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
def user_lots(request, id_tlg):
    try:
        lots = Lot.objects.filter(id_tlg=id_tlg)
    except User.DoesNotExist:
        return Response({"error": "Lots not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = LotSerializer(lots, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
def lot_detail(request, id_lot):
    try:
        lot = Lot.objects.get(pk=id_lot)
    except Lot.DoesNotExist:
        return Response({"error": "Lot not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LotSerializer(lot)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        lot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_lot(request):
    serializer = EmptySerializer(data=request.data)
    if serializer.is_valid():
        lot_id = serializer.validated_data.get('lot_id')
        tlg_id = serializer.validated_data.get('tlg_id')

        try:
            lot = Lot.objects.get(pk=lot_id)
            if lot.id_tlg == tlg_id and lot.id_tlg == request.user.id_tlg:
                lot.delete()
                return Response({'message': 'Lot deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'You do not have permission to delete this lot'}, status=status.HTTP_403_FORBIDDEN)
        except Lot.DoesNotExist:
            return Response({'error': 'Lot not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_user_tg_id(request, id_tlg):
    try:
        user = User.objects.get(id_tlg=id_tlg)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_category(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


def main(request):
    lots = Lot.objects.all().order_by("-dt_create")
    paginator = Paginator(lots, COUNT_ELEM)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "wbx_app/content.html", {"page_obj": page_obj})


def search(request):
    query = request.GET.get("q")
    lots = Lot.objects.filter(name__icontains=query)
    paginator = Paginator(lots, COUNT_ELEM)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "wbx_app/content.html", {"page_obj": page_obj})


@api_view(["PUT"])
def create_lot(request):
    id_tlg = request.data.get("id_tlg")
    if id_tlg:
        user = User.objects.get(id_tlg=id_tlg)
        lot_data = {
            "id_tlg": user.id_tlg,
            "name": request.data.get("name"),
            "categories": request.data.get("categories"),
            "url_photos": request.data.get("url_photos"),
            "url_chat": request.data.get("url_chat"),
            "description": request.data.get("description"),
            "price": request.data.get("price"),
            "region": user.region,
            "address": user.address,
            "working_time_start": user.working_time_start,
            "working_time_end": user.working_time_end,
        }
        serializer = LotSerializer(data=lot_data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(serializer.errors, status=400)
    return Response({"error": "id_tlg is required"}, status=400)


def lot_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    lots = category.lots.all()
    paginator = Paginator(lots, COUNT_ELEM)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "wbx_app/content.html", {"page_obj": page_obj})
