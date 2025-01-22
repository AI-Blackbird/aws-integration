import boto3
from typing import Optional

class Boto3Builder:
    def __init__(
        self,
        region_name: str,
        service_name: Optional[str] = None,
        profile_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        endpoint_url: Optional[str] = None,
        iam_role_assigned: Optional[bool] = False,
    ):
        self.service_name = service_name
        self.profile_name = profile_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint_url = endpoint_url
        self.iam_role_assigned = iam_role_assigned
        self.region_name = region_name

    def set_profile_name(self, profile_name: str):
        self.profile_name = profile_name

    def set_credentials(self, aws_access_key_id: str, aws_secret_access_key: str):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def set_endpoint_url(self, endpoint_url: str):
        self.endpoint_url = endpoint_url

    def build_session(self):
        if self.iam_role_assigned:
            session = boto3.Session()
        elif self.profile_name:
            session = boto3.Session(profile_name=self.profile_name)
        else:
            session_kwargs = {}
            if self.aws_access_key_id and self.aws_secret_access_key:
                session_kwargs["aws_access_key_id"] = self.aws_access_key_id
                session_kwargs["aws_secret_access_key"] = self.aws_secret_access_key
            session = boto3.Session(**session_kwargs)
        return session

    def _get_kwargs(self):
        kwargs = {
            "region_name": self.region_name,
        }
        if self.endpoint_url:
            kwargs["endpoint_url"] = self.endpoint_url
        return kwargs

    def build_client(self, service_name):
        session = self.build_session()
        client_kwargs = self._get_kwargs()
        return session.client(self.service_name or service_name, **client_kwargs)

    def build_resource(self, service_name):
        session = self.build_session()
        resource_kwargs = self._get_kwargs()
        return session.resource(self.service_name or service_name, **resource_kwargs)
