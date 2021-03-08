from enlace import *
import time
import numpy as np

class Server:
    
    def __init__(self, img_location, TX, RX, baudrate):
        self.location_w  = img_location
        self.comTX       = TX
        self.comRX       = RX
        self.rxBuffer_H = 0
        self.rxBuffer = 0
        self.rxBuffer_resp = 0
        self.Baud_Rate = baudrate
        
    def init_comm(self):
            try:
                print("-------------------------")
                print("Server Started")
                print("-------------------------")
                
                # Declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
                # para declarar esse objeto é o nome da porta.
                self.STX = enlace(self.comTX, self.Baud_Rate)
                self.SRX = enlace(self.comRX, self.Baud_Rate)
                
                # Ativa comunicacao. Inicia os threads e a comunicação serial 
                self.STX.enable()
                self.SRX.enable()
                
                # Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
                server_init_msg1 = "Server TX iniciado na porta: {}.".format(self.comTX)
                server_init_msg2 = "Server RX iniciado na porta: {}.".format(self.comRX)
                
                print(server_init_msg1)
                print(server_init_msg2) 
                print("-------------------------")
                
                return([server_init_msg1,server_init_msg2])
            
            except Exception as erro:
                print("ops! :-\\")
                print(erro)
                self.STX.disable()
                self.SRX.disable()  
                
    def header_receive_response(self):
            try:
                # Local da imagem a ser salva
                server_comm_msg1 = "Local onde a imagem recebida será salva: {}.".format(self.location_w)
                print(server_comm_msg1)
                print("-------------------------")
                
                # Espera os dados do Header - Client
                server_comm_msg2 = "Esperando o Header do Client."
                print(server_comm_msg2)
                
                self.rxBuffer_H, nRx_H = self.SRX.getData(2)
                self.rxBuffer_resp = int.from_bytes(self.rxBuffer_H, "big")
                print("-------------------------")
                server_comm_msg3 = "O Header do Client foi recebido."
                print(server_comm_msg3)
                print("-------------------------")
                time.sleep(1)
                
                # Retornando uma resposta do Header para o Client
                server_comm_msg4 = "Enviando uma resposta do Header para o Client."
                print(server_comm_msg4)
                self.STX.sendData(np.asarray(self.rxBuffer_H)) 
                print("-------------------------")
                
                return([server_comm_msg1,server_comm_msg2,server_comm_msg3,server_comm_msg4])
            
            except Exception as erro:
                print("ops! :-\\")
                print(erro)
                self.STX.disable()
                self.SRX.disable()  
                
    def data_receive_response(self):
            try:
                # Espera os dados do Client
                server_data_msg1 = "Esperando os dados do Client."
                print(server_data_msg1)
                print("-------------------------")
                self.rxBuffer, nRx = self.SRX.getData(self.rxBuffer_resp)
                server_data_msg2 = "Dados recebidos do Client."
                print(server_data_msg2)
                print("-------------------------")
                
                # Passando os dados para o Client
                server_data_msg3 = "Concluindo a conexão com o Client."
                print(server_data_msg3)
                self.STX.sendData(np.asarray(self.rxBuffer)) 
                time.sleep(1)
                
                return([server_data_msg1,server_data_msg2,server_data_msg3])
            
            except Exception as erro:
                print("ops! :-\\")
                print(erro)
                self.STX.disable()
                self.SRX.disable()   
                
    def end_connection(self):
            try:
                # Salva imagem
                print("-------------------------")
                image_name = self.location_w.split("\\")
                server_end_msg1 = "Salvando dados no arquivo: {}.".format(image_name[1])
                print(server_end_msg1)
                f = open(self.location_w, "wb")
                f.write(self.rxBuffer)
            
                # Encerra comunicação
                print("-------------------------")
                server_end_msg2 = "Comunicação encerrada com as portas {} e {}.".format(self.comTX,self.comRX)
                print(server_end_msg2)
                print("-------------------------")
                self.STX.disable()
                self.SRX.disable() 
                
                return([server_end_msg1,server_end_msg2])
            
            except Exception as erro:
                print("ops! :-\\")
                print(erro)
                self.STX.disable()
                self.SRX.disable()                   