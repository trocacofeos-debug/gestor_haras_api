from http.server import BaseHTTPRequestHandler
import json

from io import BytesIO

from backend.services.pdf_service import gerar_pdf
from backend.services.r2_service import upload_file



class handler(BaseHTTPRequestHandler):


    def responder(
        self,
        status,
        dados
    ):

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.end_headers()


        self.wfile.write(

            json.dumps(
                dados,
                ensure_ascii=False
            ).encode("utf-8")

        )



    def do_POST(self):

        try:


            tamanho = int(

                self.headers.get(
                    "Content-Length",
                    0
                )

            )


            corpo = self.rfile.read(
                tamanho
            )



            dados = json.loads(

                corpo.decode(
                    "utf-8"
                )

            )



            # =====================================
            # DADOS DA PROPOSTA
            # =====================================


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





            # =====================================
            # GERAR PDF
            # =====================================


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





            # =====================================
            # CAMINHO NO CLOUDFLARE R2
            # =====================================


            nome_arquivo = (

                "contratos/"
                "original/"
                f"contrato_{proposta_id}.pdf"

            )





            # =====================================
            # ENVIO R2
            # =====================================


            url = upload_file(

                arquivo=arquivo,

                nome=nome_arquivo,

                content_type="application/pdf"

            )





            # =====================================
            # RESPOSTA
            # =====================================


            self.responder(

                200,

                {


                    "sucesso":

                        True,


                    "contratoPdfUrl":

                        url,


                    "arquivo":

                        nome_arquivo,


                    "tipo":

                        "contrato_original"


                }

            )





        except Exception as e:



            print(

                "ERRO GERAR CONTRATO:",

                e

            )



            self.responder(

                500,

                {


                    "sucesso":

                        False,


                    "erro":

                        str(e)

                }

            )