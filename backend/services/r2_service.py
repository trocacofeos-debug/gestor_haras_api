import os
import boto3

from dotenv import load_dotenv

load_dotenv()

ACCOUNT_ID = os.getenv("7eeaf013daeb98306d3ec8a7a6810983")
ACCESS_KEY = os.getenv("ce59cafbd16bf84385b4f56332e53f7c")
SECRET_KEY = os.getenv("ab390ba95abecb33e75f5d3b8c323fff80fbf401aef0d280ef2637551700beec")
BUCKET = os.getenv("gestor-haras-documentos")
PUBLIC_URL = os.getenv("https://pub-0183482dc8464927b3051ac235ffad6f.r2.dev")


def _criar_cliente():
    if not all([
        ACCOUNT_ID,
        ACCESS_KEY,
        SECRET_KEY,
        BUCKET,
    ]):
        raise Exception(
            "Variáveis do Cloudflare R2 não configuradas"
        )

    return boto3.client(
        "s3",
        endpoint_url=(
            f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"
        ),
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name="auto",
    )


client = _criar_cliente()


def upload_file(
    arquivo,
    nome,
    content_type="application/octet-stream",
):
    """
    Envia arquivo para Cloudflare R2

    arquivo:
        objeto BytesIO ou arquivo aberto

    nome:
        caminho dentro do bucket

    content_type:
        MIME Type do arquivo
    """

    arquivo.seek(0)

    client.upload_fileobj(
        arquivo,
        BUCKET,
        nome,
        ExtraArgs={
            "ContentType": content_type
        },
    )

    if PUBLIC_URL:
        return f"{PUBLIC_URL}/{nome}"

    return (
        f"https://{BUCKET}.{ACCOUNT_ID}.r2.cloudflarestorage.com/{nome}"
    )