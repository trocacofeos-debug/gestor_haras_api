import os
import boto3

from dotenv import load_dotenv


load_dotenv()


ACCOUNT_ID = os.getenv(
    "R2_ACCOUNT_ID"
)

ACCESS_KEY = os.getenv(
    "R2_ACCESS_KEY"
)

SECRET_KEY = os.getenv(
    "R2_SECRET_KEY"
)

BUCKET = os.getenv(
    "R2_BUCKET"
)

PUBLIC_URL = os.getenv(
    "R2_PUBLIC_URL"
)


if not all([
    ACCOUNT_ID,
    ACCESS_KEY,
    SECRET_KEY,
    BUCKET,
]):
    raise Exception(
        "Variáveis do Cloudflare R2 não configuradas"
    )



client = boto3.client(
    "s3",

    endpoint_url=(
        f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"
    ),

    aws_access_key_id=ACCESS_KEY,

    aws_secret_access_key=SECRET_KEY,

    region_name="auto",
)



def upload_file(
    arquivo,
    nome,
    content_type="application/octet-stream"
):

    """
    Envia arquivo para Cloudflare R2

    arquivo:
        file object

    nome:
        nome do arquivo no bucket
    """


    client.upload_fileobj(

        arquivo,

        BUCKET,

        nome,

        ExtraArgs={

            "ContentType": content_type

        }

    )


    if PUBLIC_URL:

        return (
            f"{PUBLIC_URL}/{nome}"
        )


    return (
        f"https://{BUCKET}.{ACCOUNT_ID}.r2.cloudflarestorage.com/{nome}"
    )