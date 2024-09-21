import toml
from pathlib import Path

from pydantic import BaseModel
from datetime import datetime
import base64

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.types import PublicKeyTypes, PrivateKeyTypes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class CyantizeLicense(BaseModel):
    licensee_company_name: str
    expiration_date: datetime


class CyantizeLicenseExpired(Exception):
    pass


class SignedCyantizeLicense(BaseModel):
    """
    Utility class to write and read CyantizeLicense with
    an attached signature validating only signed licenses work
    """

    cyantize_license: CyantizeLicense
    signature: str

    @staticmethod
    def loads(signed_cyantize_license: "SignedCyantizeLicense", public_key: PublicKeyTypes):
        signature_data_bytes = toml.dumps(signed_cyantize_license.cyantize_license.model_dump()).encode("utf-8")
        signature_bytes = base64.b64decode(signed_cyantize_license.signature)

        public_key.verify(
            signature_bytes,
            signature_data_bytes,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )

        expiration_date = signed_cyantize_license.cyantize_license.expiration_date
        if expiration_date < datetime.now():
            raise CyantizeLicenseExpired(f"License expired in {expiration_date.strftime('%d-%m-%Y')}")

        return signed_cyantize_license.cyantize_license

    @classmethod
    def from_file(cls, signed_cyantize_license_path: Path, public_key_path: Path) -> CyantizeLicense:
        with open(signed_cyantize_license_path) as f:
            signed_cyantize_license_toml = toml.load(f)
            signed_cyantize_license = SignedCyantizeLicense.model_validate(signed_cyantize_license_toml)

        with open(public_key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

        return cls.loads(signed_cyantize_license, public_key)

    @staticmethod
    def dumps(cyantize_license: CyantizeLicense, private_key: PrivateKeyTypes):
        signature_data_bytes = toml.dumps(cyantize_license.model_dump()).encode("utf-8")
        signature_bytes = private_key.sign(
            signature_data_bytes, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256()
        )

        signature_textual = base64.b64encode(signature_bytes).decode("utf-8")

        return SignedCyantizeLicense(cyantize_license=cyantize_license, signature=signature_textual)

    @classmethod
    def to_file(cls, cyantize_license: CyantizeLicense, license_path: Path, private_key_path: Path):
        with open(private_key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

        signed_cyantize_license = cls.dumps(cyantize_license, private_key)

        with open(license_path, "w") as out_file:
            toml.dump(signed_cyantize_license.model_dump(), out_file)
