import socket
import threading
import time
import os
import cv2

# Importação dos módulos separados
from utils import protocolo
from utils.imagem import Imagem 

class Servidor():
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Prepara o classificador de faces (carregado apenas uma vez)
        xml_classificador = os.path.join(os.path.relpath(
            cv2.__file__).replace('__init__.py', ''), 'data\\haarcascade_frontalface_default.xml')
        self.face_cascade = cv2.CascadeClassifier(xml_classificador)

    def start(self):
        endpoint = (self._host, self._port)
        try:
            self.__tcp.bind(endpoint)
            self.__tcp.listen(5) 
            print(f"Servidor iniciado em {self._host}:{self._port}")
            
            while True:
                # O servidor aceita a ligação e passa-a imediatamente para uma nova thread[cite: 11]
                con, client = self.__tcp.accept()
                thread_cliente = threading.Thread(target=self._service, args=(con, client))
                thread_cliente.start()
                
        except Exception as e:
            print("Erro ao inicializar o servidor", e.args)

    def processar_imagem(self, matriz_imagem):
        """Função isolada para aplicar o Haar Cascade e desenhar retângulos verdes"""
        gray = cv2.cvtColor(matriz_imagem, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        # Retângulo verde: (0, 255, 0)[cite: 10]
        for (x, y, w, h) in faces:
            cv2.rectangle(matriz_imagem, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
        return matriz_imagem

    def _service(self, con, client):
        """Método executado pela thread para atender um cliente específico"""
        time.sleep(5) # Pausa exigida para conseguirem fazer o teste de 2 clientes simultâneos
        print("Iniciou atendimento ao cliente", client)
        
        try:
            # 1. Recebe os bytes usando o protocolo
            dados_recebidos = protocolo.receber_mensagem(con)
            
            if dados_recebidos:
                # 2. Transforma bytes em matriz OpenCV
                img_obj = Imagem()
                img_obj.decodificar(dados_recebidos)
                
                # 3. Processa
                img_obj.matriz = self.processar_imagem(img_obj.matriz)
                
                # 4. Transforma matriz OpenCV em bytes novamente
                dados_resposta = img_obj.codificar()
                
                # 5. Envia de volta
                protocolo.enviar_mensagem(con, dados_resposta)
                
            print("Terminou atendimento e enviou resposta ao cliente", client)
            
        except Exception as e:
            print("Erro no atendimento ao cliente ", client, ": ", e.args)
        finally:
            con.close()

if __name__ == "__main__":
    serv = Servidor("localhost", 9000)
    serv.start()