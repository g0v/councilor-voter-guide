import json
from rest_framework import serializers


class Field(serializers.Field):
    def to_native(self, obj):
        return obj
