import socket
import threading

class Servidor():
    """
    Classe Servidor - API Socket (Multithread)
    """

    def __init__(self, host, port):
        """
        Construtor da classe servidor
        """
        self._host = host
        self._port = port
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        """
        Método que inicializa a execução do servidor
        """
        endpoint = (self._host, self._port)
        try:
            self.__tcp.bind(endpoint)
            # Aumentei o listen para 5 (boa prática para servidores multithread)
            self.__tcp.listen(5) 
            print("Servidor iniciado em ", self._host, ": ", self._port)
            
            while True:
                con, client = self.__tcp.accept()
                thread_cliente = threading.Thread(target=self._service, args=(con, client))
                thread_cliente.start()
                #Aqui entrou o serviço multithreading
                
        except Exception as e:
            print("Erro ao inicializar o servidor", e.args)

    def _service(self, con, client):
        """
        Método que implementa o serviço de calculadora
        :param con: objeto socket utilizado para enviar e receber dados
        :param client: é o endereço do cliente
        """
        print("Atendendo cliente ", client)
        try:
            while True:
                msg = con.recv(1024)
                if not msg: # Sai do loop se o cliente fechar a conexão
                    break
                    
                msg_s = str(msg.decode('ascii'))
                resp = eval(msg_s)
                con.send(bytes(str(resp), 'ascii'))
                print(client, " -> requisição atendida")
                
        except OSError as e:
            print("Erro de conexão ", client, ": ", e.args)
        except Exception as e:
            print("Erro nos dados recebidos pelo cliente ", client, ": ", e.args)
            try:
                con.send(bytes("Erro", 'ascii'))
            except:
                pass
        finally:
            print("Encerrando conexão com", client)
            con.close()

if __name__ == "__main__":
    serv = Servidor("localhost", 9000)
    serv.start()