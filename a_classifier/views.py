from django.shortcuts import render
from rest_framework.views import APIView
import tensorflow as tf
from PIL import Image
from rest_framework import status
from rest_framework.response import Response

# Create your views here.
from a_form.models import EquipmentImage


class PredictView(APIView):
    def post(self, request):
        pass


class TrainingView(APIView):
    def post(self, request):
        # convert image to png
        equipmentImage = EquipmentImage.objects.all()
        for equipment in equipmentImage:

            imageName = str(equipment.image).split('.')[0]
            img = Image.open(equipment.image)
            # img.save("{}.{}".format(imageName, "png"))
            # equipment.save()
        data_dir = './image/equipment'
        print(data_dir)
        # batch_size = 32
        # img_height = 180
        # img_width = 180
        # train_ds = tf.keras.utils.image_dataset_from_directory(
        #     data_dir,
        #     validation_split=0.2,
        #     subset="training",
        #     seed=123,
        #     image_size=(img_height, img_width),
        #     batch_size=batch_size)
        # val_ds = tf.keras.utils.image_dataset_from_directory(
        #     data_dir,
        #     validation_split=0.2,
        #     subset="validation",
        #     seed=123,
        #     image_size=(img_height, img_width),
        #     batch_size=batch_size)
        # class_names = train_ds.class_names
        return Response({"message": "Model Trained"}, status=status.HTTP_204_NO_CONTENT)
