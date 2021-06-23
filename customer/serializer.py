from rest_framework import serializers

from utilities.python_utils import get_schema_from_url
from .models import *


class ClientSerializer(serializers.ModelSerializer):
    domains = serializers.SerializerMethodField('get_domains', read_only=True)

    def validate(self, initial_data):
        schema_name = get_schema_from_url(self.context)
        domain_exist = Client.objects.filter(schema_name=schema_name).exists()
        name_exist = Client.objects.filter(name=initial_data['name']).exists()
        if name_exist:
            raise serializers.ValidationError('A client with this name already exists')
        if domain_exist:
            raise serializers.ValidationError('A client with this domain already exists')
        initial_data['schema_name'] = schema_name
        initial_data['domain_url'] = self.context
        return initial_data

    def create(self, validated_data):
        client = Client.objects.create(name=validated_data['name'], schema_name=validated_data['schema_name'])
        domain = Domain()
        domain.domain = validated_data['domain_url']
        domain.tenant = client
        domain.is_primary = True
        domain.save()
        return client

    def get_domains(self, obj):
        domains = Domain.objects.filter(tenant=obj)
        serializer = DomainSerializer(domains, many=True)
        return serializer.data

    class Meta:
        model = Client
        fields = ('name', 'domains', 'schema_name')


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ('domain', 'is_primary')
