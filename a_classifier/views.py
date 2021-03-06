from PIL import Image
from rest_framework.views import APIView
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from a_api.permissions import ManagerPermission
from a_form.models import Equipment, Room

data_dir = './media/image/equipment'
batch_size = 32
img_height = 180
img_width = 180


class TrainingView(APIView):
    permission_classes = [ManagerPermission]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # print(data_dir)
        train_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="training",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size)
        val_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="validation",
            seed=123,
            image_size=(img_height, img_width),
            batch_size=batch_size)
        class_names = train_ds.class_names
        normalization_layer = tf.keras.layers.Rescaling(1. / 255)
        normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
        image_batch, labels_batch = next(iter(normalized_ds))
        first_image = image_batch[0]
        # Notice the pixel values are now in `[0,1]`.
        print(np.min(first_image), np.max(first_image))
        num_classes = len(class_names)

        model = tf.keras.Sequential([
            tf.keras.layers.RandomFlip("horizontal", input_shape=(img_height, img_width, 3)),
            tf.keras.layers.RandomRotation(0.1),
            tf.keras.layers.RandomZoom(0.1),
            tf.keras.layers.Rescaling(1. / 255),
            tf.keras.layers.Conv2D(16, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu'),
            tf.keras.layers.MaxPooling2D(),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dense(num_classes)
        ])
        model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])
        epochs = 15
        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs
        )
        model.save('./a_classifier/model')
        # acc = history.history['accuracy']
        # val_acc = history.history['val_accuracy']
        # loss = history.history['loss']
        # val_loss = history.history['val_loss']
        # epochs_range = range(epochs)
        # plt.figure(figsize=(8, 8))
        # plt.subplot(1, 2, 1)
        # plt.plot(epochs_range, acc, label='Training Accuracy')
        # plt.plot(epochs_range, val_acc, label='Validation Accuracy')
        # plt.legend(loc='lower right')
        # plt.title('Training and Validation Accuracy')
        #
        # plt.subplot(1, 2, 2)
        # plt.plot(epochs_range, loss, label='Training Loss')
        # plt.plot(epochs_range, val_loss, label='Validation Loss')
        # plt.legend(loc='upper right')
        # plt.title('Training and Validation Loss')
        # plt.show()
        return Response({"message": "Model Trained"})


class PredictView(APIView):
    permission_classes = [ManagerPermission]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if 'image' in request.data:
            pic = request.data['image']
            img = Image.open(pic).resize((img_height, img_width), Image.ANTIALIAS)
            img_array = tf.keras.utils.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)  # Create a batch
            model = tf.keras.models.load_model('./a_classifier/model')
            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0]).numpy()
            train_ds = tf.keras.utils.image_dataset_from_directory(
                data_dir)
            class_names = train_ds.class_names
            equipment1 = class_names[np.argsort(score, axis=0)[-1]]
            equipment1 = equipment1.split("@")
            equipment1 = Equipment.objects.filter(equipment_name=equipment1[1], room__room_name=equipment1[0])
            equipment2 = class_names[np.argsort(score, axis=0)[-2]]
            equipment2 = equipment2.split("@")
            equipment2 = Equipment.objects.filter(equipment_name=equipment2[1], room__room_name=equipment2[0])
            equipment3 = class_names[np.argsort(score, axis=0)[-2]]
            equipment3 = equipment3.split("@")
            equipment3 = Equipment.objects.filter(equipment_name=equipment3[1], room__room_name=equipment3[0])
            return Response(
                [
                    {
                        "equipment_id": equipment1[0].id,
                        "equipment_name": equipment1[0].equipment_name.replace("_", " "),
                        "confidence": 100 * score[np.argsort(score, axis=0)[-1]],
                        "equipment_code": equipment1[0].equipment_code,
                        "room_id": equipment1[0].room.id,
                        "room_name": equipment1[0].room.room_name.replace("_", " "),
                    },
                    {
                        "equipment_id": equipment2[0].id,
                        "equipment_name": equipment2[0].equipment_name.replace("_", " "),
                        "confidence": 100 * score[np.argsort(score, axis=0)[-2]],
                        "equipment_code": equipment2[0].equipment_code,
                        "room_id": equipment2[0].room.id,
                        "room_name": equipment2[0].room.room_name.replace("_", " "),
                    },
                    {
                        "equipment_id": equipment3[0].id,
                        "equipment_name": equipment3[0].equipment_name.replace("_", " "),
                        "confidence": 100 * score[np.argsort(score, axis=0)[-3]],
                        "equipment_code": equipment3[0].equipment_code,
                        "room_id": equipment3[0].room.id,
                        "room_name": equipment3[0].room.room_name.replace("_", " "),
                    }
                ]
            )
        return Response({"message": "image no found"})
