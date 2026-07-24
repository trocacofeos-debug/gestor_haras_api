from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors


def gerar_pdf(
    cliente,
    valor,
    parcelas,
    cpf_cnpj=None,
    endereco=None,
    cidade=None,
):
    """
    Gera contrato PDF em memória.

    Retorna:
        bytes do arquivo PDF
    """

    buffer = BytesIO()


    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )


    estilos = getSampleStyleSheet()


    conteudo = []


    # ==========================
    # TÍTULO
    # ==========================

    conteudo.append(
        Paragraph(
            "CONTRATO DIGITAL",
            estilos["Title"],
        )
    )


    conteudo.append(
        Spacer(
            1,
            25,
        )
    )


    # ==========================
    # CLIENTE
    # ==========================

    dados_cliente = [
        [
            "Cliente",
            cliente or "-"
        ],
        [
            "CPF/CNPJ",
            cpf_cnpj or "-"
        ],
        [
            "Endereço",
            endereco or "-"
        ],
        [
            "Cidade",
            cidade or "-"
        ],
    ]


    tabela = Table(
        dados_cliente,
        colWidths=[
            100,
            300,
        ],
    )


    tabela.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    0.5,
                    colors.grey,
                ),

                (
                    "VALIGN",
                    (0,0),
                    (-1,-1),
                    "TOP",
                ),
            ]
        )
    )


    conteudo.append(
        tabela
    )


    conteudo.append(
        Spacer(
            1,
            25,
        )
    )


    # ==========================
    # TEXTO CONTRATO
    # ==========================

    texto = f"""
    Pelo presente instrumento particular,
    as partes formalizam o presente contrato digital.

    Cliente:
    {cliente}

    Valor total:
    R$ {valor}

    Quantidade de parcelas:
    {parcelas}

    O contratante declara que as informações
    fornecidas são verdadeiras e autoriza a
    assinatura eletrônica deste documento.

    Este contrato foi gerado eletronicamente
    pelo sistema Gestor Haras.
    """


    conteudo.append(
        Paragraph(
            texto.replace(
                "\n",
                "<br/>"
            ),
            estilos["BodyText"],
        )
    )


    conteudo.append(
        Spacer(
            1,
            80,
        )
    )


    # ==========================
    # ASSINATURA
    # ==========================

    assinatura = [
        [
            "____________________________",
        ],
        [
            "Assinatura do Cliente",
        ],
    ]


    tabela_assinatura = Table(
        assinatura
    )


    conteudo.append(
        tabela_assinatura
    )


    documento.build(
        conteudo
    )


    buffer.seek(0)


    return buffer.read()