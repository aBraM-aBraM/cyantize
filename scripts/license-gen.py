import sys
from pathlib import Path
import click
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from cyantize.license import CyantizeLicense, SignedCyantizeLicense
from cyantize.consts import PRIVATE_KEY_FILENAME, PUBLIC_KEY_FILENAME, LICENSE_FILENAME


def generate_keys(private_key_path: Path, public_key_path: Path):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    with open(private_key_path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    public_key = private_key.public_key()

    with open(public_key_path, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


@click.group()
def cli():
    pass


@cli.command()
@click.argument("licensee-company-name", type=str)
@click.argument("expiration-date", type=click.DateTime(formats=["%d-%m-%Y"]))
def generate_license(
    licensee_company_name: str,
    expiration_date: str,
):
    print(f"Creating license for {licensee_company_name}", file=sys.stderr)

    private_key_path = Path.cwd() / PRIVATE_KEY_FILENAME
    public_key_path = Path.cwd() / PUBLIC_KEY_FILENAME

    output = Path.cwd() / LICENSE_FILENAME

    if not (private_key_path.exists() and public_key_path.exists()):
        if click.confirm(
            f"Both key files don't exist. Would you like both to be generated at {private_key_path}, {public_key_path}?",
            err=True,
        ):
            generate_keys(private_key_path, public_key_path)
        else:
            print("Exited because keys don't exist", file=sys.stderr)
            return

    cyantize_license = CyantizeLicense(expiration_date=expiration_date, licensee_company_name=licensee_company_name)
    SignedCyantizeLicense.to_file(cyantize_license=cyantize_license, license_path=output, private_key_path=private_key_path)


@cli.command()
@click.argument("license-path", type=click.types.Path(exists=True, dir_okay=False))
@click.argument("private_key_path", type=click.types.Path(exists=True, dir_okay=False))
def show_license(license_path: Path, private_key_path):
    try:
        cyantize_license = SignedCyantizeLicense.from_file(license_path, private_key_path)

        print(f'License for "{cyantize_license.licensee_company_name}"', file=sys.stderr)
        print(f"Expires in {cyantize_license.expiration_date.strftime('%d-%m-%Y')}", file=sys.stderr)
        print("", file=sys.stderr)

        print(cyantize_license.model_dump())

    except InvalidSignature:
        print("License signature is invalid", file=sys.stderr)
        return


if __name__ == "__main__":
    cli()
