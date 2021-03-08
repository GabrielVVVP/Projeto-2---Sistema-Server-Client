import PySimpleGUI as sg
import os.path
import Server

# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("Carregar Imagem"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Text("Modo"),
        sg.Combo(['ARDUINO', 'INTERNO'], enable_events=True,size=(10, 4), key='combo1'),
    ],
    [
        sg.Text("Baud Rate"),
        sg.Combo([4800,9600,115200,230400,460800], enable_events=True,size=(10, 4), key='combo2'),
    ],
    [
        sg.Text("Porta Server TX"),
        sg.Combo(['COM1', 'COM2', 'COM3','COM4'], enable_events=True,size=(10, 4), key='combo3'),
    ],
    [
        sg.Text("Porta Server RX"),
        sg.Combo(['COM1', 'COM2', 'COM3','COM4'], enable_events=True,size=(10, 4), key='combo4'),
    ],
    [sg.Button('Atribuir Portas',size=(15, 2),enable_events=True, key="-BEGIN-")],
    [sg.Text(size=(40, 1), key="-BEGINTXT-")],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Imagem recebida do Cliente:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

Server_column = [
    [sg.Text("Comunicação Servidor:")],
    [sg.Text(size=(50, 1), key="-ROUT1-")],
    [sg.Text(size=(50, 1), key="-ROUT2-")],
    [sg.Text(size=(50, 1), key="-ROUT3-")],
    [sg.Text(size=(50, 1), key="-ROUT4-")],
    [sg.Text(size=(50, 1), key="-ROUT5-")],
    [sg.Text(size=(50, 1), key="-ROUT6-")],
    [sg.Text(size=(50, 1), key="-ROUT7-")],
    [sg.Text(size=(50, 1), key="-ROUT8-")],
    [sg.Text(size=(50, 1), key="-ROUT9-")],
    [sg.Text(size=(50, 1), key="-ROUT10-")],
    [sg.Text(size=(50, 1), key="-ROUT11-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(Server_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Projeto 2 - Servidor", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            filename = os.path.join(values["-FOLDER-"],"Copia_recebida.png")
        except:
            file_list = []
        
    elif event == "-BEGIN-":  
        try:
            modo = values['combo1']
            STX = values['combo3']
            SRX = values['combo4']
            if (((STX==SRX)and(filename!=None)and(modo=="ARDUINO"))or((STX!=SRX)and(filename!=None)and(modo=="INTERNO"))):
                
                baudrate = values['combo2']
                
                # Aviso para de início da GUI
                begintxt = "O protocolo foi inicializado."
                window["-BEGINTXT-"].update(begintxt)   
                
                # Iniciando a comunicação com Servidor
                server_info = Server.Server(filename,STX,SRX,baudrate)
                server_init_resp = server_info.init_comm()
                window["-ROUT1-"].update(server_init_resp[0])
                window["-ROUT2-"].update(server_init_resp[1])
                
                # Esperando o Header e retornando a resposta
                server_header_resp = server_info.header_receive_response()
                window["-ROUT3-"].update(server_header_resp[0])
                window["-ROUT4-"].update(server_header_resp[1])
                window["-ROUT5-"].update(server_header_resp[2])
                window["-ROUT6-"].update(server_header_resp[3])
                
                # Esperando os Dados e retornando a resposta
                server_data_resp = server_info.data_receive_response()
                window["-ROUT7-"].update(server_data_resp[0])
                window["-ROUT8-"].update(server_data_resp[1])
                window["-ROUT9-"].update(server_data_resp[2])    
                
                # Escrevendo dados na imagem e concluindo a conexão
                server_end_resp = server_info.end_connection()
                window["-ROUT10-"].update(server_end_resp[0])
                window["-ROUT11-"].update(server_end_resp[1])
                window["-TOUT-"].update("Copia_recebida.png")
                window["-IMAGE-"].update(filename=filename)
                
            else:
                begintxt = "O arranjo escolhido não pode ser inicializado."
                window["-BEGINTXT-"].update(begintxt)

        except:
            pass

window.close()