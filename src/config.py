
import toml
from pathlib import Path

config_path = Path(__file__).resolve(strict=True).parent.parent / "config.toml"

try:
    print(config_path)
    config_file = open(config_path)
except IOError:
    raise IOError("Config file doesn't exist, create config.toml")


CONFIG = toml.load(config_file)
# Certs
certs_path = Path(__file__).resolve(strict=True).parent.parent / "certs"
CONFIG["AWS"]["certs"] = {
    "certificate": str(certs_path / "certificate.pem.crt"),
    "private": str(certs_path / "private.pem.key"),
    # "public": str(certs_path / "public.pem.key"),
}
print(CONFIG)
