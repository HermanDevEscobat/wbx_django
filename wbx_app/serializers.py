from rest_framework import serializersfrom .models import User, Category, Lotclass UserSerializer(serializers.ModelSerializer):    class Meta:        model = User        fields = '__all__'  # Можно указать конкретные поля, например ['id_tlg', 'coordinates', 'locations']class CategorySerializer(serializers.ModelSerializer):    class Meta:        model = Category        fields = '__all__'class LotSerializer(serializers.ModelSerializer):    class Meta:        model = Lot        fields = '__all__'class EmptySerializer(serializers.Serializer):    lot_id = serializers.IntegerField()    tlg_id = serializers.IntegerField()