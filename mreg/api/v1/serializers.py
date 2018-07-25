from django.contrib.sessions.backends.base import CreateError
from rest_framework import serializers
from mreg.models import *
from mreg.utils import *


def ttl_validate(value):
    """Ensures a ttl-value is within accepted range."""
    if value < 300:
        raise serializers.ValidationError("Ensure this value is greater than or equal to 300.")
    if value > 68400:
        raise serializers.ValidationError("Ensure this value is less than or equal to 68400.")


def key_validate(obj):
    """
    Filters out unknown keys and raises a ValidationError.
    :param obj: Serializer object whose keys should be checked.
    """
    unknown_keys = set(obj.initial_data.keys()) - set(obj.fields.keys())
    if unknown_keys:
        raise serializers.ValidationError('invalid keys passed into serializer: {0}'.format(unknown_keys))


class CnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cname
        fields = '__all__'

    def validate(self, data):
        key_validate(self)
        data = {key: nonify(value) for key, value in data.items()}
        return data

    def validate_ttl(self, value):
        """Ensures ttl is within range. -1 equals None/Null"""
        value = nonify(value)
        if value:
            ttl_validate(value)
        return value


class HinfoPresetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HinfoPresets
        fields = '__all__'

    def validate(self, data):
        key_validate(self)
        data = {key: nonify(value) for key, value in data.items()}
        return data


class IpaddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ipaddress
        fields = ('hostid', 'ipaddress', 'macaddress')

    def validate(self, data):
        invalid_keys = set(self.initial_data.keys()) - set(self.fields.keys())
        if invalid_keys:
            raise serializers.ValidationError('invalid keys passed into serializer: {0}'.format(invalid_keys))
        key_validate(self)
        data = {key: nonify(value) for key, value in data.items()}
        return data


class TxtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Txt
        fields = '__all__'

    def validate(self, data):
        key_validate(self)
        data = {key: nonify(value) for key, value in data.items()}
        return data


class PtrOverrideSerializer(serializers.ModelSerializer):
    class Meta:
        model = PtrOverride
        fields = '__all__'

    def validate(self, data):
        key_validate(self)
        data = {key: nonify(value) for key, value in data.items()}
        return data


class HostsSerializer(serializers.ModelSerializer):
    ipaddress = IpaddressSerializer(many=True, read_only=True)
    cname = CnameSerializer(many=True, read_only=True)
    txt = TxtSerializer(many=True, read_only=True)
    ptr_override = PtrOverrideSerializer(many=True, read_only=True)
    hinfo = HinfoPresetsSerializer(required=False)['hinfoid']

    class Meta:
        model = Hosts
        fields = ('hostid', 'name', 'contact', 'ttl', 'hinfo', 'loc',
                  'comment', 'cname', 'ipaddress', 'txt', 'ptr_override')

    def validate(self, data):
        key_validate(self)
        data = {key: nonify(value) for key, value in data.items()}
        return data

    def validate_ttl(self, value):
        """Ensures ttl is within range. -1 equals None/Null"""
        value = nonify(value)
        if value:
            ttl_validate(value)
        return value


class HostsSaveSerializer(serializers.ModelSerializer):
    ipaddress = IpaddressSerializer(many=True, read_only=True)
    cname = CnameSerializer(many=True, read_only=True)
    txt = TxtSerializer(many=True, read_only=True)
    ptr_override = PtrOverrideSerializer(many=True, read_only=True)
    hinfo = serializers.IntegerField(required=False)

    class Meta:
        model = Hosts
        fields = ('hostid', 'name', 'contact', 'ttl', 'hinfo', 'loc',
                  'comment', 'cname', 'ipaddress', 'txt', 'ptr_override')

    def validate(self, data):
        key_validate(self)
        data = {key: nonify(value) for key, value in data.items()}
        return data

    def validate_ttl(self, value):
        """Ensures ttl is within range. -1 equals None/Null"""
        value = nonify(value)
        if value:
            ttl_validate(value)
        return value

    def validate_hinfo(self, value):
        value = nonify(value)
        if value != None:
            value = HinfoPresets.objects.get(pk=value)
        return value


class HostsNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hosts
        fields = ('name',)

    def validate(self, data):
        key_validate(self)
        data = {key: nonify(value) for key, value in data.items()}
        return data


class NaptrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Naptr
        fields = '__all__'

    def validate(self, data):
        key_validate(self)
        data = {key: nonify(value) for key, value in data.items()}
        return data


class NsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ns
        fields = '__all__'

    def validate_ttl(self, value):
        """Ensures ttl is within range. -1 equals None/Null"""
        value = nonify(value)
        if value:
            ttl_validate(value)
        return value


class SrvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Srv
        fields = '__all__'

    def validate_ttl(self, value):
        """Ensures ttl is within range. -1 equals None/Null"""
        value = nonify(value)
        if value:
            ttl_validate(value)
        return value


class SubnetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subnets
        fields = '__all__'

    def validate(self, data):
        key_validate(self)
        data = {key: nonify(value) for key, value in data.items()}
        return data

    def create(self):
        return Subnets(**self.validated_data)


class ZonesSerializer(serializers.ModelSerializer):
    nameservers = NsSerializer(read_only=True, many=True)

    class Meta:
        model = Zones
        fields = '__all__'

    def validate(self, data):
        key_validate(self)
        data = {key: nonify(value) for key, value in data.items()}
        return data

    def create(self):
        return Zones(**self.validated_data)

    def validate_ttl(self, value):
        """Ensures ttl is within range. -1 equals None/Null"""
        value = nonify(value)
        if value:
            ttl_validate(value)
        return value


class ModelChangeLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelChangeLogs
        fields = '__all__'

    def validate(self, data):
        key_validate(self)
        data = {key: nonify(value) for key, value in data.items()}
        return data

    def create(self):
        return ModelChangeLogs(**self.validated_data)




