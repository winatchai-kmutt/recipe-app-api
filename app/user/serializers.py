"""
Serializers for the user API View.
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers


# Serializer : Python object <-> JSON + Validation
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user objects."""

    class Meta:
        # Ref model
        model = get_user_model()
        # list field for Serializer
        fields = ['email', 'password', 'name']
        # password -> can't read -> No response
        # validate with min_length 5
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

        def create(self, validated_data):
            """Create and return a user with encrypted password."""
            return get_user_model().objects.create_user(**validated_data)
