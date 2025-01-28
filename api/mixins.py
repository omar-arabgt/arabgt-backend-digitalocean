from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework.serializers import ValidationError

from .choices import *


class FileMixin:

    @transaction.atomic
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        files = validated_data.pop("file")
        instance = super().create(validated_data)
        self._process_file(instance, files)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        files = validated_data.pop("file")
        self._process_file(instance, files, update=True)
        return super().update(instance, validated_data)

    def _process_file(self, instance, files, update=False):
        from .serializers import FileSerializer

        if update:
            image_count = instance.files.filter(file_type=FileType.IMAGE).count()
            video_count = instance.files.filter(file_type=FileType.VIDEO).count()
        else:
            image_count = 0
            video_count = 0

        file_serializers = []

        for file in files:
            file_data = {
                "file": file,
                "content_type": ContentType.objects.get_for_model(self.Meta.model).id,
                "object_id": instance.id
            }
            file_serializer = FileSerializer(data=file_data)
            file_serializer.is_valid(raise_exception=True)

            file_type = file_serializer.validated_data.get("file_type")
            if file_type == FileType.IMAGE:
                image_count += 1
            elif file_type == FileType.VIDEO:
                video_count += 1

            file_serializers.append(file_serializer)

        if image_count > UPLOAD_MAX_IMAGE_NUMBER or video_count > UPLOAD_MAX_VIDEO_NUMBER:
            raise ValidationError({"error": "Maximum file limit exceeded!"})

        for i in file_serializers:
            i.save()
