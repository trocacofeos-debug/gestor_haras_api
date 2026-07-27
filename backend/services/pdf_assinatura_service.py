import io
import requests

from PIL import Image

from pypdf import PdfReader, PdfWriter

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4



def baixar_pdf(url: str) -> bytes:
    """
    Baixa o contrato original do Cloudflare R2
    """

    response = requests.get(
        url,
        timeout=60,
    )

    response.raise_for_status()

    return response.content





def criar_pagina_assinatura(
    assinatura_bytes: bytes,
    proposta_id: str,
) -> bytes:
    """
    Cria uma página PDF contendo a assinatura
    """

    buffer = io.BytesIO()


    pdf = canvas.Canvas(
        buffer,
        pagesize=A4,
    )


    largura, altura = A4



    pdf.setFont(
        "Helvetica-Bold",
        16,
    )


    pdf.drawString(
        50,
        altura - 80,
        "Assinatura Digital do Contrato",
    )



    pdf.setFont(
        "Helvetica",
        12,
    )


    pdf.drawString(
        50,
        altura - 120,
        f"Proposta: {proposta_id}",
    )



    imagem = Image.open(
        io.BytesIO(
            assinatura_bytes
        )
    )


    imagem.save(
        "/tmp/assinatura.png"
    )



    pdf.drawImage(
        "/tmp/assinatura.png",
        80,
        altura - 300,
        width=250,
        height=120,
        preserveAspectRatio=True,
        mask="auto",
    )



    pdf.drawString(
        50,
        altura - 360,
        "Documento assinado eletronicamente.",
    )


    pdf.save()


    buffer.seek(0)


    return buffer.read()







def juntar_pdf_assinatura(
    contrato_original: bytes,
    pagina_assinatura: bytes,
) -> bytes:
    """
    Junta o contrato original com a página da assinatura
    """

    saida = io.BytesIO()


    writer = PdfWriter()



    contrato = PdfReader(
        io.BytesIO(
            contrato_original
        )
    )


    assinatura = PdfReader(
        io.BytesIO(
            pagina_assinatura
        )
    )



    for pagina in contrato.pages:

        writer.add_page(
            pagina
        )



    for pagina in assinatura.pages:

        writer.add_page(
            pagina
        )



    writer.write(
        saida
    )


    saida.seek(0)


    return saida.read()







def gerar_contrato_assinado(
    contrato_url: str,
    assinatura_bytes: bytes,
    proposta_id: str,
) -> bytes:
    """
    Fluxo completo:

    1 - baixa contrato original
    2 - cria página assinatura
    3 - junta PDFs
    4 - retorna PDF final
    """



    contrato_original = baixar_pdf(
        contrato_url
    )



    pagina_assinatura = criar_pagina_assinatura(

        assinatura_bytes,

        proposta_id,

    )



    contrato_final = juntar_pdf_assinatura(

        contrato_original,

        pagina_assinatura,

    )



    return contrato_final