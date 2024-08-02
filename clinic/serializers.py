from rest_framework.serializers import ModelSerializer, ImageField, SerializerMethodField

from .models import ClinicImage, Clinic

# minseo : 한의원 이미지 
class ClinicImageSerializer(ModelSerializer):
    image = ImageField(use_url=True)

    class Meta:
        model = ClinicImage
        fields = ['image']


class ClinicSerializer(ModelSerializer):
    image_list = SerializerMethodField()

    class Meta:
        model = Clinic
        fields = '__all__'

	# minseo : 게시글에 등록된 이미지들 가지고 오기
    def get_image_list(self, obj):
        image = obj.image.all() 
        return ClinicImageSerializer(instance=image, many=True, context=self.context).data

    def create(self, validated_data):
        instance = Clinic.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            ClinicImage.objects.create(clinic=instance, image=image_data)
        return instance