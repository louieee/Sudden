from django.contrib.auth.models import User
from django_tenants.utils import schema_context, tenant_context
from rest_framework import serializers

from customer.models import Client


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password",)
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        with tenant_context(Client.objects.get(schema_name=self.context['schema'])):
            if self.context['title'] == 'superuser':
                user = User.objects.create_superuser(email=validated_data["email"], username=validated_data["username"],
                                                     password=validated_data["password"])
            else:
                user = User.objects.create(email=validated_data["email"], username=validated_data["username"],
                                           password=validated_data["password"])
                if self.context['title'] == 'staff':
                    user.is_staff = True
                user.save()
            return user