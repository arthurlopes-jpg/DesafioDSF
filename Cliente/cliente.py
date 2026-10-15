import socket
import cv2

# Importação dos módulos separados
from utils import protocolo
from utils.imagem import Imagem

class Cliente():
    def __init__(self, server_ip, port):
        self.__server_ip = server_ip
        self.__port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        endpoint = (self.__server_ip, self.__port)
        try:
            self.__tcp.connect(endpoint)
            print("Ligação realizada com sucesso!")
            self.__method()
        except:
            print("Servidor não disponível")

    def __method(self):
        try:
            # 1. Carrega e codifica a imagem (Atenção ao caminho da imagem!)
            img_obj = Imagem()
            # Certifique-se de que a pasta 'faces' e a imagem existem no seu diretório
            img_obj.ler('faces/image_0001.jpg') 
            dados_enviar = img_obj.codificar()

            if not dados_enviar:
                print("Erro: Não foi possível carregar a imagem. Verifique o caminho.")
                return

            # 2. Envia para o servidor
            print("A enviar imagem para o servidor...")
            protocolo.enviar_mensagem(self.__tcp, dados_enviar)

            # 3. Aguarda a resposta
            print("A aguardar resposta do servidor (o servidor tem uma pausa de 5s)...")
            dados_recebidos = protocolo.receber_mensagem(self.__tcp)

            # 4. Decodifica e mostra a janela[cite: 10]
            if dados_recebidos:
                img_resposta = Imagem()
                img_resposta.decodificar(dados_recebidos)
                
                print("Imagem recebida! A abrir a janela...")
                cv2.imshow('Imagem Processada', img_resposta.matriz)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("Falha ao receber a imagem processada.")

        except Exception as e:
            print("Erro ao realizar comunicação com o servidor", e.args)
        finally:
            self.__tcp.close()

if __name__ == "__main__":
    c = Cliente("127.0.0.1", 9000)
    c.start()