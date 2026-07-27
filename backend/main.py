from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
    Query,
)

from backend.services.pdf_assinatura_service import gerar_contrato_assinado

from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse

from io import BytesIO

import uuid



from backend.services.pdf_service import gerar_pdf

from backend.services.r2_service import upload_file



# =====================================================
# APP
# =====================================================

app = FastAPI(

    title="Gestor Haras API",

    version="1.0.0"

)





# =====================================================
# CORS
# =====================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "*"
    ],

    allow_credentials=False,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ],

)





# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():

    return {

        "status":
            "ok",

        "api":
            "Gestor Haras",

        "storage":
            "cloudflare_r2"

    }





# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health():

    return {

        "online":
            True,

        "servico":
            "Gestor Haras API"

    }





# =====================================================
# STATUS UPLOAD
# =====================================================

@app.get("/api/upload")
def upload_status():

    return {

        "status":
            "online",

        "servico":
            "upload",

        "storage":
            "cloudflare_r2"

    }





# =====================================================
# UPLOAD GENERICO R2
# DOCUMENTOS / IMAGENS
# =====================================================

@app.post("/api/upload")
async def upload(

    file:
        UploadFile = File(...),


    pasta:
        str = Form("documentos"),

):


    try:


        print(
            "UPLOAD RECEBIDO:",
            file.filename
        )



        if not file.filename:


            raise HTTPException(

                status_code=400,

                detail="Arquivo não informado"

            )





        extensao = ""


        if "." in file.filename:


            extensao = (

                "."

                +

                file.filename

                .split(".")

                [-1]

                .lower()

            )





        nome = (

            f"{pasta}/"

            f"{uuid.uuid4()}"

            f"{extensao}"

        )





        conteudo = await file.read()




        if not conteudo:


            raise HTTPException(

                status_code=400,

                detail="Arquivo vazio"

            )





        arquivo = BytesIO(

            conteudo

        )


        arquivo.seek(0)





        url = upload_file(

            arquivo=arquivo,

            nome=nome,

            content_type=(

                file.content_type

                or

                "application/octet-stream"

            )

        )





        print(

            "SALVO R2:",

            url

        )





        return {


            "sucesso":

                True,


            "arquivo":

                nome,


            "url":

                url


        }





    except HTTPException:


        raise





    except Exception as e:


        print(

            "ERRO UPLOAD:",

            e

        )


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )








# =====================================================
# GERAR CONTRATO ORIGINAL PDF
# =====================================================

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





        pdf_bytes = gerar_pdf(


            cliente,

            valor,

            parcelas,

            cpf_cnpj,

            endereco,

            cidade


        )





        if not pdf_bytes:


            raise Exception(

                "PDF vazio"

            )





        arquivo = BytesIO(

            pdf_bytes

        )


        arquivo.seek(0)





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





        print(

            "CONTRATO ORIGINAL SALVO:",

            url

        )





        return {


            "sucesso":

                True,


            "contratoPdfUrl":

                url,


            "arquivo":

                nome_arquivo,


            "tipo":

                "contrato_original"


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

    # =====================================================
# GERAR CONTRATO ASSINADO
# CONTRATO ORIGINAL + ASSINATURA
# =====================================================

@app.post("/upload_contrato_assinado")

async def upload_contrato_assinado(


    proposta_id:

        str = Form(...),



    contrato_url:

        str = Form(...),



    file:

        UploadFile = File(...),


):


    try:


        print(

            "ASSINATURA RECEBIDA:",

            file.filename

        )





        if not file.filename:


            raise HTTPException(

                status_code=400,

                detail="Assinatura não informada"

            )







        assinatura_bytes = await file.read()





        if not assinatura_bytes:


            raise HTTPException(

                status_code=400,

                detail="Arquivo assinatura vazio"

            )







        # =====================================
        # GERAR PDF ASSINADO
        # =====================================


        pdf_final = gerar_contrato_assinado(

            contrato_url,

            assinatura_bytes,

            proposta_id

        )







        if not pdf_final:


            raise Exception(

                "PDF assinado vazio"

            )







        arquivo = BytesIO(

            pdf_final

        )


        arquivo.seek(0)







        nome_arquivo = (

            "contratos/"

            "assinados/"

            f"contrato_{proposta_id}_assinado.pdf"

        )







        url = upload_file(


            arquivo=arquivo,


            nome=nome_arquivo,


            content_type="application/pdf"


        )







        print(

            "CONTRATO ASSINADO SALVO:",

            url

        )







        return {


            "sucesso":

                True,


            "contratoAssinadoUrl":

                url,


            "arquivo":

                nome_arquivo,


            "tipo":

                "contrato_assinado"


        }







    except HTTPException:


        raise





    except Exception as e:


        print(

            "ERRO CONTRATO ASSINADO:",

            e

        )


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )








# =====================================================
# CONSULTAR ARQUIVO
# =====================================================

@app.get("/arquivo")

async def consultar_arquivo(


    url:

        str = Query(...)


):


    return {


        "sucesso":

            True,


        "arquivo":

            url


    }








# =====================================================
# EXCLUIR ARQUIVO R2
# FUTURO
# =====================================================

@app.delete("/api/upload")

async def excluir_upload(


    url:

        str = Query(...)


):


    try:


        print(

            "SOLICITAÇÃO DELETE:",

            url

        )




        return {


            "sucesso":

                False,


            "mensagem":

                "Exclusão ainda não implementada",


            "url":

                url


        }




    except Exception as e:


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )








# =====================================================
# TRATAMENTO GLOBAL DE ERRO
# =====================================================

@app.exception_handler(Exception)

async def erro_global(


    request,


    exc


):


    print(

        "ERRO GLOBAL:",

        exc

    )



    return JSONResponse(


        status_code=500,


        content={


            "sucesso":

                False,


            "erro":

                str(exc)


        }


    )

    