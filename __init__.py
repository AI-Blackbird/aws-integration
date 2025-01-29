from cat.log import log
from cat.db.cruds import plugins as crud_plugins

import boto3
from typing import Optional
from cat.plugins.aws_integration.aws_integration import AWSSettings
from cat.plugins.aws_integration.boto3_builder import Boto3Builder

AWS_PLUGIN_PREFIX = "aws_integration"

AWS_ACCES_KEY_LEN = 20
AWS_SECRET_ACCES_KEY_LEN = 40
DEFAULT_REGION = "us-east-1"

class BaseFactory:
    """Base class for all factories to ensure consistent interfaces."""

    def __init__(self, settings=None):
        self._settings = settings

    def get_client(self, service_name, settings=None):
        raise NotImplementedError("Subclasses must implement this method.")

    def get_resource(self, service_name, settings=None):
        raise NotImplementedError("Subclasses must implement this method.")




class AWSFactory(BaseFactory):
    """Specific factory capable of creating AWS clients and resources based on aws_model."""

    def __init__(self, settings):
        super().__init__(settings)

    def get_client(self, service_name, settings=None):
        return self.get_aws_client(settings or self._settings, service_name)

    def get_resource(self, service_name, settings=None):
        return self.get_aws_resource(
            settings or self._settings, service_name
        )

    def get_aws(cls, settings, service_name=None) -> Optional[Boto3Builder]:
        return Boto3Builder(
            service_name=service_name,
            profile_name=settings.get("credentials_profile_name"),
            aws_access_key_id=settings.get("aws_access_key_id"),
            aws_secret_access_key=settings.get("aws_secret_access_key"),
            endpoint_url=settings.get("endpoint_url"),
            iam_role_assigned=settings.get("iam_role_assigned"),
            region_name=settings.get("region_name", DEFAULT_REGION),
        )

    def get_aws_client(cls, settings, service_name) -> Optional[Boto3Builder]:
        client_builder = cls.get_aws(settings)
        return client_builder.build_client(service_name)

    def get_aws_resource(cls, settings, service_name) -> Optional[Boto3Builder]:
        resource_builder = cls.get_aws(settings)
        return resource_builder.build_resource(service_name)

class EmptyFactory(BaseFactory):
    """Fallback factory that does nothing but log calls to show missing configurations."""

    def get_client(self, service_name, settings=None):
        log.info("No operation available. Ensure plugin is configured correctly.")
        return None

    def get_resource(self, service_name, settings=None):
        log.info("No operation available. Ensure plugin is configured correctly.")
        return None


def factory():
    """Create an AWS client factory from the aws_integration plugin settings."""

    plugin_settings = crud_plugins.get_setting('system', AWS_PLUGIN_PREFIX)

    if plugin_settings:
        return AWSFactory(plugin_settings)


    log.info("No AWS integration plugin found or failed to initialize.")
    return EmptyFactory()


class Boto3:
    """Wrapper class that uses a factory to get AWS clients and resources based on plugin configuration."""

    def __init__(self, settings=None):
        self.factory_instance = factory()
        self.settings = settings

    def get_client(self, service_name, settings=None):
        return self.factory_instance.get_client(service_name, settings or self.settings)

    def get_resource(self, service_name, settings=None):
        return self.factory_instance.get_resource(
            service_name, settings or self.settings
        )


__all__ = ["Boto3"]
