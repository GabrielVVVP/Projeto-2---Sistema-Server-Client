from enlace import *
import time
import numpy as np

class Client:
    
    def __init__(self, img_location, TX, RX, baudrate):
        self.location_r  = img_location
        self.comTX       = TX
        self.comRX       = RX
        self.txBuffer_H = 0
        self.txBuffer = 0
        self.txBuffer_len = 0
        self.rxBuffer_H = 0
        self.rxBuffer_D = 0
        self.start_time = 0
        self.execution_time = 0
        self.Baud_Rate = baudrate
        
    def init_comm(self):
            try:
                print("-------------------------")
                print("Client Started")
                print("-------------------------")
                
                # Declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
                # para declarar esse objeto é o nome da porta.
                self.CTX = enlace(self.comTX, self.Baud_Rate)
                self.CRX = enlace(self.comRX, self.Baud_Rate)
                
                # Ativa comunicacao. Inicia os threads e a comunicação serial 
                self.CTX.enable()
                self.CRX.enable()
                
                # Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
                client_init_msg1 = "Client TX iniciado na porta: {}.".format(self.comTX)
                client_init_msg2 = "Client RX iniciado na porta: {}.".format(self.comRX)
                
                print(client_init_msg1)
                print(client_init_msg2)  
                print("-------------------------")
                
                # Começar o cronometro do tempo de execução do envio
                client_init_msg3 = "Iniciando o timer de execução."
                print(client_init_msg3)
                print("-------------------------")
                self.start_time = time.time()
                
                return([client_init_msg1,client_init_msg2,client_init_msg3])
            
            except Exception as erro:
                print("ops! :-\\")
                print(erro)
                self.CTX.disable()
                self.CRX.disable()   
                
    def header_send_response(self):
            try:
                # Carregando imagem a ser executada
                image_name = self.location_r.split("\\")
                self.txBuffer = open(self.location_r, "rb").read()
                self.txBuffer_len = len(self.txBuffer)
                client_comm_msg1 = "Imagem para transmissão: {} ({} bytes).".format(image_name[1], self.txBuffer_len)
                print(client_comm_msg1)
                print("-------------------------")
                
                # Enviando para o Server o Header
                client_comm_msg2 = "Enviando o para o Server o Head."
                print(client_comm_msg2)
                print("-------------------------")
                self.txBuffer_H = (self.txBuffer_len).to_bytes(2, byteorder="big")
                
                self.CTX.sendData(np.asarray(self.txBuffer_H)) 
                
                # Recebendo uma resposta do Server sobre o Header
                client_comm_msg3 = "Esperando a resposta do Server sobre o Head."
                print(client_comm_msg3)
                self.rxBuffer_H, nRx = self.CRX.getData(2)
                print("-------------------------")
                client_comm_msg4 = "Recebido do Server a resposta do Head."
                print(client_comm_msg4)
                print("-------------------------")
                
                return([client_comm_msg1,client_comm_msg2,client_comm_msg3,client_comm_msg4])
            
            except Exception as erro:
                print("ops! :-\\")
                print(erro)
                self.CTX.disable()
                self.CRX.disable()
                
    def data_send_response(self):
            try: 
                
                # Transmitir dados para Server
                client_data_msg1 = "Enviando os dados para o Server."
                print(client_data_msg1)
                print("-------------------------")
                self.CTX.sendData(np.asarray(self.txBuffer)) 
              
                # Acesso aos bytes recebidos
                client_data_msg2 = "Esperando a resposta de conclusão da conexão."
                print(client_data_msg2)
                print("-------------------------")
                self.rxBuffer_D, nRx = self.CRX.getData(self.txBuffer_len)
                
                client_data_msg3 = "Concluindo a conexão com o Server."
                print(client_data_msg3)
                print("-------------------------")
                
                return([client_data_msg1,client_data_msg2,client_data_msg3])
            
            except Exception as erro:
                print("ops! :-\\")
                print(erro)
                self.CTX.disable()
                self.CRX.disable() 
                
    def end_connection(self):
            try:
                # Encerra tempo de cronometro
                print("Procedimento finalizado")
                self.execution_time = time.time() - self.start_time
                client_end_msg1 = "Tempo de execução: {:.2f} segundos.".format(self.execution_time)
                print(client_end_msg1)
                client_end_msg2 = "Velocidade de transmissão: {:.2f} Bytes/segundos.".format(self.txBuffer_len/self.execution_time)
                print(client_end_msg2)
                
                # Encerra comunicação
                print("-------------------------")
                client_end_msg3 = "Comunicação encerrada com as portas {} e {}.".format(self.comTX,self.comRX)
                print(client_end_msg3)
                print("-------------------------")
                self.CTX.disable()
                self.CRX.disable() 
                
                return([client_end_msg1,client_end_msg2,client_end_msg3])
            
            except Exception as erro:
                print("ops! :-\\")
                print(erro)
                self.CTX.disable()
                self.CRX.disable()             