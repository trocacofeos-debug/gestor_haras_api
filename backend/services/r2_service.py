import os
import boto3

from dotenv import load_dotenv

# ==========================================
# CARREGA VARIÁVEIS DE AMBIENTE
# ==========================================

load_dotenv()

ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
SECRET_KEY = os.getenv("R2_SECRET_KEY")
BUCKET = os.getenv("R2_BUCKET")
PUBLIC_URL = os.getenv("R2_PUBLIC_URL")


# ==========================================
# VALIDA CONFIGURAÇÕES
# ==========================================

def _validar_configuracao():
    faltando = []

    if not ACCOUNT_ID:
        faltando.append("R2_ACCOUNT_ID")

    if not ACCESS_KEY:
        faltando.append("R2_ACCESS_KEY")

    if not SECRET_KEY:
        faltando.append("R2_SECRET_KEY")

    if not BUCKET:
        faltando.append("R2_BUCKET")

    if faltando:
        raise Exception(
            f"Variáveis do Cloudflare R2 não configuradas: {', '.join(faltando)}"
        )


# ==========================================
# CRIA CLIENTE R2
# ==========================================

def _criar_cliente():
    _validar_configuracao()

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


# ==========================================
# UPLOAD DE ARQUIVO
# ==========================================

def upload_file(
    arquivo,
    nome,
    content_type="application/octet-stream",
):
    """
    Envia arquivo para Cloudflare R2.

    Parâmetros:
        arquivo:
            BytesIO ou arquivo aberto

        nome:
            caminho dentro do bucket

        content_type:
            MIME Type
    """

    try:
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

    except Exception as e:
        raise Exception(
            f"Erro ao enviar arquivo para Cloudflare R2: {str(e)}"
        )


# ==========================================
# TESTE LOCAL
# ==========================================

if __name__ == "__main__":
    print("R2_ACCOUNT_ID:", ACCOUNT_ID)
    print("R2_BUCKET:", BUCKET)
    print("R2_PUBLIC_URL:", PUBLIC_URL)
    print("Cloudflare R2 configurado com sucesso.")