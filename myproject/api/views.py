# api/views.py
from rest_framework import viewsets, status
from serializers.serializers import ItemSerializer
from services.services import get_all_items, create_item
from api.models import Item
from rest_framework.views import APIView
from rest_framework.response import Response
from services import services

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get_queryset(self):
        return get_all_items()

    def perform_create(self, serializer):
        data = serializer.validated_data
        create_item(data['name'], data['description'])
        
class ItemListGetAPIView(APIView):
    def get(self, request):
        items = services.get_all_items()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    
class ItemListPostAPIView(APIView):
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ItemUpdateAPIView(APIView):
    def put(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)  # get the item by ID
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()  # updates the item
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ItemDeleteAPIView(APIView):
    def delete(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response({"message": "Item deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class ItemPartialUpdateAPIView(APIView):
    def patch(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)