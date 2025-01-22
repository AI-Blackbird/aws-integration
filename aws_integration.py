from cat.mad_hatter.decorators import tool, hook, plugin
from pydantic import BaseModel, Field, model_validator
from typing import Optional
from cat.log import log
import json

AWS_ACCES_KEY_LEN = 20
AWS_SECRET_ACCES_KEY_LEN = 40
DEFAULT_REGION = "us-east-1"





class AWSSettings(BaseModel):
    aws_access_key_id: str = Field(
        default="", description="AWS access key ID for authentication."
    )
    aws_secret_access_key: str = Field(
        default="", description="AWS secret access key for authentication."
    )
    region_name: str = Field(
        default=DEFAULT_REGION, description="Default AWS region for the client."
    )
    credentials_profile_name: str = Field(
        default="", description="Name of the AWS credentials profile to use."
    )
    endpoint_url: str = Field(
        default="",
        description="Custom endpoint URL, if using a non-standard AWS service endpoint.",
    )
    iam_role_assigned: bool = Field(
        default=False, description="Indicates if the required IAM role is assigned."
    )
    caller_identity: str = Field(
        default="",
        description="Amazon Resource Name (ARN) that uniquely identifies the caller based on the credentials provided.",
    )



#     @model_validator(mode="after")
#     def validate(cls, v):
#         session = boto3.Session()
#         available_regions = session.get_available_regions("ec2")
#         if v.region_name not in available_regions:
#             raise ValueError(f"{v.region_name} is not a valid AWS region")
#
#         if not v.iam_role_assigned:
#             if not v.credentials_profile_name:
#                 if not v.aws_access_key_id or not v.aws_secret_access_key:
#                     raise ValueError(
#                         "Enable the IAM role or provide a credentials profile name or both aws_access_key_id and aws_secret_access_key."
#                     )
#                 elif not (
#                     len(v.aws_access_key_id) == AWS_ACCES_KEY_LEN
#                     and len(v.aws_secret_access_key) == AWS_SECRET_ACCES_KEY_LEN
#                 ):
#                     raise ValueError("The access key or secret access key is invalid!")
#
#         values = cls.set_identity(v.dict())
#         v.caller_identity = values["caller_identity"]
#
#         return v
#
#     @model_validator(mode="before")
#     def set_identity(cls, values):
#         client = cls.get_aws_client(values, service_name="sts")
#         response = client.get_caller_identity()
#         log.debug("AWS Caller Identity Response: {}".format(json.dumps(response)))
#         values["caller_identity"] = response["Arn"]
#
#         return values

    class Config:
        extra = "forbid"
        anystr_strip_whitespace = True


@plugin
def settings_model():
    return AWSSettings
