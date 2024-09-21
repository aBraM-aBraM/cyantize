import pytest

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.exceptions import InvalidSignature
from cyantize.license import CyantizeLicense, SignedCyantizeLicense, CyantizeLicenseExpired
from datetime import datetime, timedelta


@pytest.fixture
def keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    return private_key, public_key


def test_cyantize_license_sanity(keys):
    private, public = keys

    cyantize_license = CyantizeLicense(licensee_company_name="example", expiration_date=datetime.now() + timedelta(hours=1))
    signed_cyantize_license = SignedCyantizeLicense.dumps(cyantize_license, private)

    verified_cyantize_license = SignedCyantizeLicense.loads(signed_cyantize_license, public)
    assert verified_cyantize_license == cyantize_license

    invalid_cyantize_license = signed_cyantize_license
    invalid_cyantize_license.cyantize_license.licensee_company_name = "other-company"

    with pytest.raises(InvalidSignature):
        SignedCyantizeLicense.loads(invalid_cyantize_license, public)


def test_cyantize_license_expiration(keys):
    private, public = keys

    cyantize_license = CyantizeLicense(licensee_company_name="example", expiration_date=datetime(year=1970, month=1, day=1))
    signed_cyantize_license = SignedCyantizeLicense.dumps(cyantize_license, private)

    with pytest.raises(CyantizeLicenseExpired):
        SignedCyantizeLicense.loads(signed_cyantize_license, public)
