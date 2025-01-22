from cat.log import log
from cat.db.cruds import plugins as crud_plugins

from core.cat.plugins.aws_integration.aws_integration import AWSSettings

AWS_PLUGIN_PREFIX = "aws_integration"


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

    def __init__(self, settings, aws_model):
        super().__init__(settings)
        self._aws_model = aws_model

    def get_client(self, service_name, settings=None):
        return self._aws_model.get_aws_client(settings or self._settings, service_name)

    def get_resource(self, service_name, settings=None):
        return self._aws_model.get_aws_resource(
            settings or self._settings, service_name
        )


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

    aws_model = AWSSettings()
    plugin_settings = crud_plugins.get_setting('user', AWS_PLUGIN_PREFIX)

    if plugin_settings and aws_model:
        return AWSFactory(plugin_settings, aws_model)


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
