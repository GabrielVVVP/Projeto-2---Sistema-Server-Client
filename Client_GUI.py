import PySimpleGUI as sg
import os.path
import Client


# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("Carregar Imagem"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 7), key="-FILE LIST-"
        )
    ],
    [
        sg.Text("Modo"),
        sg.Combo(['ARDUINO', 'INTERNO'], enable_events=True,size=(10, 4), key='combo1'),
    ],
    [
        sg.Text("Baud Rate"),
        sg.Combo([9600,115200,230400], enable_events=True,size=(10, 4), key='combo2'),
    ],
    [
        sg.Text("Porta Client TX"),
        sg.Combo(['COM1', 'COM2', 'COM3','COM4'], enable_events=True,size=(10, 4), key='combo3'),
    ],
    [
        sg.Text("Porta Client RX"),
        sg.Combo(['COM1', 'COM2', 'COM3','COM4'], enable_events=True,size=(10, 4), key='combo4'),
    ],
    [sg.Button('Atribuir Portas',size=(15, 2),enable_events=True, key="-BEGIN-")],
    [sg.Text(size=(40, 1), key="-BEGINTXT-")],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Imagem para ser enviada para o Server:")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

Client_column = [
    [sg.Text("Comunicação Cliente:")],
    [sg.Text(size=(45, 1), key="-ROUT1-")],
    [sg.Text(size=(45, 1), key="-ROUT2-")],
    [sg.Text(size=(45, 1), key="-ROUT3-")],
    [sg.Text(size=(45, 1), key="-ROUT4-")],
    [sg.Text(size=(45, 1), key="-ROUT5-")],
    [sg.Text(size=(45, 1), key="-ROUT6-")],
    [sg.Text(size=(45, 1), key="-ROUT7-")],
    [sg.Text(size=(45, 1), key="-ROUT8-")],
    [sg.Text(size=(45, 1), key="-ROUT9-")],
    [sg.Text(size=(45, 1), key="-ROUT10-")],
    [sg.Text(size=(45, 1), key="-ROUT11-")],
    [sg.Text(size=(45, 1), key="-ROUT12-")],
    [sg.Text(size=(45, 1), key="-ROUT13-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(Client_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Projeto 2 - Cliente", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
            window["-TOUT-"].update(values["-FILE LIST-"][0])
            window["-IMAGE-"].update(filename=filename)

        except:
            pass
    elif event == "-BEGIN-":  
        try:
            modo = values['combo1']
            CTX = values['combo3']
            CRX = values['combo4']
            filename = os.path.join(values["-FOLDER-"], values["-FILE LIST-"][0])
            
            if (((CTX==CRX)and(filename!=None)and(modo=="ARDUINO"))or((CTX!=CRX)and(filename!=None)and(modo=="INTERNO"))):
                
                baudrate = values['combo2']
                
                # Aviso para de início da GUI
                begintxt = "O protocolo foi inicializado."
                window["-BEGINTXT-"].update(begintxt)   
                
                # Iniciando a comunicação com Client
                client_info = Client.Client(filename,CTX,CRX,baudrate)
                client_init_resp = client_info.init_comm()
                window["-ROUT1-"].update(client_init_resp[0])
                window["-ROUT2-"].update(client_init_resp[1])
                window["-ROUT3-"].update(client_init_resp[2])
                
                # Enviando e recebendo o Header
                client_header_resp = client_info.header_send_response()
                window["-ROUT4-"].update(client_header_resp[0])
                window["-ROUT5-"].update(client_header_resp[1])
                window["-ROUT6-"].update(client_header_resp[2])
                window["-ROUT7-"].update(client_header_resp[3])
                
                # Esperando os Dados e retornando a resposta
                client_data_resp = client_info.data_send_response()
                window["-ROUT8-"].update(client_data_resp[0])
                window["-ROUT9-"].update(client_data_resp[1])
                window["-ROUT10-"].update(client_data_resp[2])  
                
                # Escrevendo dados na imagem e concluindo a conexão
                client_end_resp = client_info.end_connection()
                window["-ROUT11-"].update(client_end_resp[0])
                window["-ROUT12-"].update(client_end_resp[1])
                window["-ROUT13-"].update(client_end_resp[2])
                
            else:
                begintxt = "O arranjo escolhido não pode ser inicializado."
                window["-BEGINTXT-"].update(begintxt)

        except:
            pass

window.close()