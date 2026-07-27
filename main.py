from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from io import BytesIO

from backend.services.pdf_service import gerar_pdf
from backend.services.r2_service import upload_file


app = FastAPI(
    title="Gestor Haras API",
    version="1.0.0"
)


# =====================================
# CORS - PERMITIR FLUTTER WEB
# =====================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "*"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],
)



# =====================================
# TESTE API
# =====================================

@app.get("/")
def home():

    return {
        "status": "ok",
        "api": "Gestor Haras"
    }




# =====================================
# GERAR CONTRATO PDF
# =====================================

@app.post("/gerar_contrato")
async def gerar_contrato(
    dados: dict
):

    try:


        proposta_id = dados.get(
            "proposta_id",
            "sem_id"
        )


        cliente = dados.get(
            "cliente",
            ""
        )


        valor = dados.get(
            "valor",
            0
        )


        parcelas = dados.get(
            "parcelas",
            1
        )


        cpf_cnpj = dados.get(
            "cpf_cnpj",
            ""
        )


        endereco = dados.get(
            "endereco",
            ""
        )


        cidade = dados.get(
            "cidade",
            ""
        )



        if not cliente:

            raise Exception(
                "Cliente não informado"
            )



        # =============================
        # GERAR PDF
        # =============================

        pdf_bytes = gerar_pdf(

            cliente,

            valor,

            parcelas,

            cpf_cnpj,

            endereco,

            cidade,

        )



        if not pdf_bytes:

            raise Exception(
                "PDF vazio"
            )



        arquivo = BytesIO(
            pdf_bytes
        )


        arquivo.seek(0)



        # =============================
        # SALVAR NO R2
        # =============================

        nome_arquivo = (

            "contratos/"
            "original/"
            f"contrato_{proposta_id}.pdf"

        )



        url = upload_file(

            arquivo=arquivo,

            nome=nome_arquivo,

            content_type="application/pdf"

        )



        # =============================
        # RETORNO PARA FLUTTER
        # =============================

        return {


            "sucesso": True,


            "contratoPdfUrl": url,


            "arquivo": nome_arquivo,


            "tipo": "contrato_original"


        }



    except Exception as e:


        print(
            "ERRO GERAR CONTRATO:",
            e
        )


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )