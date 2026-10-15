import cv2
import numpy as np

class Imagem:
    """
    Classe para guardar os pixels, ler, codificar em JPEG e decodificar bytes.
    """
    def __init__(self):
        self.matriz = None

    def ler(self, caminho):
        """Lê a imagem de um arquivo local"""
        self.matriz = cv2.imread(caminho)

    def codificar(self):
        """Converte a matriz da imagem do OpenCV para bytes no formato JPEG"""
        if self.matriz is not None:
            sucesso, buffer = cv2.imencode('.jpg', self.matriz)
            if sucesso:
                return buffer.tobytes()
        return b''

    def decodificar(self, dados):
        """Converte os bytes recebidos da rede de volta para matriz do OpenCV"""
        if dados:
            nparr = np.frombuffer(dados, np.uint8)
            self.matriz = cv2.imdecode(nparr, cv2.IMREAD_COLOR)