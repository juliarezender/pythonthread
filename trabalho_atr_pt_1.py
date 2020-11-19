import threading
import time
import math
import logging
from simple_pid import PID
import socket
import os

def calculo_altura_integral_tanque_1():
    """
    Função que integra o valor retornado pela função calculo diferencial tanque 1, para obter o valor
    de altura no instante futuro, e assim controlar esse valor posteriormente na função controlador.
    Para integrar tal valor, utiliza-se o metodo de integração Runge-Kutta.
    """
    global altura_integral_1
    global tempo_1
    variacao_tempo = 0.2

    while True:
        mutex.acquire()
        # Calcular passos parciais
        k1 = calculo_diferencial_tanque_1(tempo_1, altura_integral_1)
        k2 = calculo_diferencial_tanque_1(
            tempo_1 + variacao_tempo / 2, altura_integral_1 + variacao_tempo * k1 / 2
        )
        k3 = calculo_diferencial_tanque_1(
            tempo_1 + variacao_tempo / 2, altura_integral_1 + variacao_tempo * k2 / 2
        )
        k4 = calculo_diferencial_tanque_1(
            tempo_1 + variacao_tempo, altura_integral_1 + variacao_tempo * k3
        )
        # Calcular media ponderada dos passos parciais
        altura_integral_1 = variacao_tempo / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        tempo_1 += variacao_tempo
        mutex.release()

        # Thread se repete a cada 200 ms
        time.sleep(0.2)


def calculo_altura_integral_tanque_2():
    """
    Função que integra o valor retornado pela função calculo diferencial tanque 1, para obter o valor
    de altura no instante futuro, e assim controlar esse valor posteriormente na função controlador.
    Para integrar tal valor, utiliza-se o metodo de integração Runge-Kutta.
    """
    global altura_integral_2
    global tempo_2
    variacao_tempo = 0.2

    while True:
        mutex.acquire()
        # Calcular passos parciais
        k1 = calculo_diferencial_tanque_2(tempo_2, altura_integral_2)
        k2 = calculo_diferencial_tanque_2(
            tempo_2 + variacao_tempo / 2, altura_integral_2 + variacao_tempo * k1 / 2
        )
        k3 = calculo_diferencial_tanque_2(
            tempo_2 + variacao_tempo / 2, altura_integral_2 + variacao_tempo * k2 / 2
        )
        k4 = calculo_diferencial_tanque_2(
            tempo_2 + variacao_tempo, altura_integral_2 + variacao_tempo * k3
        )
        # Calcular media ponderada dos passos parciais
        altura_integral_2 = variacao_tempo / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        tempo_2 += variacao_tempo
        mutex.release()

        # Thread se repete a cada 200 ms
        time.sleep(0.2)


def calculo_diferencial_tanque_1(tempo, altura_integral_1):
    """
    Função que calcula a altura diferencial do tanque 1, de acordo com a formula disponibilizada
    na descrição do trabalho
    """
    global altura_controlada_1
    global q_output_tanque_1
    global q_input_tanque_2
    global altura_derivada_1
    global q_input_tanque_1

    R = 4
    r = 2
    H = 4
    coeficiente = 2

    altura_controlada_1 = abs(math.sin(tempo))  # função senoidal
    q_output_tanque_1 = coeficiente * math.sqrt(altura_controlada_1)

    altura_derivada_1 = (
        q_input_tanque_1
        - q_output_tanque_1
        - q_input_tanque_2 / (math.pi * (r + ((R - r) / H) * altura_controlada_1) ** 2)
    )

    return altura_derivada_1


def calculo_diferencial_tanque_2(tempo, altura_integral_2):
    """
    Função que calcula a altura diferencial do tanque 2, de acordo com a formula disponibilizada
    na descrição do trabalho
    """
    global altura_controlada_2
    global q_output_tanque_2
    global q_input_tanque_2

    R = 3
    r = 1
    H = 3
    coeficiente = 2

    altura_controlada_2 = abs(math.sin(tempo))  # função senoidal
    q_output_tanque_2 = coeficiente * math.sqrt(altura_controlada_2)

    altura_derivada_2 = q_input_tanque_2 - q_output_tanque_2 / (
        math.pi * (r + ((R - r) / H) * altura_controlada_2) ** 2
    )

    return altura_derivada_2


def controlador():
    """
    Função que implementa o controlador PID e calcula a entrada do tanque 1 e a entrada do
    tanque 2 com base na altura obtida atravez da integralização.
    """
    global altura_integral_2
    global q_input_tanque_2
    global altura_integral_1
    global q_input_tanque_1
    global altura_desejada_tanque_1
    global altura_desejada_tanque_2

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65434        # The port used by the server

    while True:

        mutex.acquire()

        pid_1 = PID(Kp=1, Ki=0.1, Kd=0.05, setpoint=altura_desejada_tanque_1)
        pid_2 = PID(Kp=1, Ki=0.1, Kd=0.05, setpoint=altura_desejada_tanque_2)

        q_input_tanque_2 = pid_2(altura_integral_2)
        q_input_tanque_1 = pid_1(altura_integral_1)

        message = [
            "Altura do tanque 1: {} Vazao do tanque 1: {}, Valor setado pelo user: {}".format(
                altura_integral_1, q_input_tanque_1, altura_desejada_tanque_1
            ),
            "                       ",
            "Altura do tanque 2: {} Vazao do tanque 2: {}, Valor setado pelo user: {}".format(
                altura_integral_2, q_input_tanque_2, altura_desejada_tanque_2
            ),
        ]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))

            for item in message:
                s.sendall(item.encode())

        mutex.release()

        # Thread se repete a cada 100 ms, ou seja, com o dobro da frenquencia das outras threads
        time.sleep(0.1)


def log_informacao():
    while True:
        logging.basicConfig(
            filename="log.txt",
            level="DEBUG",
            format="%(levelname)s:%(asctime)s:%(message)s",
        )
        mutex.acquire()

        logger = logging.getLogger()
        logger.debug(
            "Altura tanque 1: {}, entrada tanque 1: {}".format(altura_integral_1, q_input_tanque_1)
        )
        logger.debug(
            "Altura tanque 2: {}, entrada tanque 2: {}".format(altura_integral_2, q_input_tanque_2)
        )

        mutex.release()

        time.sleep(0.1)


def selecionar_altura_tanque():

    global altura_desejada_tanque_1
    global altura_desejada_tanque_2

    while True:
        alturas_a_serem_modificadas = input("Voce deseja modificar quantos valores de referencia? Escolha 0, 1 ou 2 ")

        mutex.acquire()

        if alturas_a_serem_modificadas == "1":
            unica_altura_a_mudar = input("Qual altura vc deseja mudar? 1 ou 2")
            if unica_altura_a_mudar == "1":
                altura_desejada_tanque_1 = float(int(input("Selecione valor de 0 a 4 para a altura do tanque 1:")))
            elif unica_altura_a_mudar == "2":
                altura_desejada_tanque_2 = float(int(input("Selecione valor de 0 a 3 para a altura do tanque 2:")))
            else:
                print("Selecione um valor valido: 1 ou 2")

        elif alturas_a_serem_modificadas == "2":
            altura_desejada_tanque_1 = float(int(input("Selecione valor de 0 a 4 para a altura do tanque 1:")))
            altura_desejada_tanque_2 = float(int(input("Selecione valor de 0 a 3 para a altura do tanque 2:")))
        elif alturas_a_serem_modificadas == "0":
            pass
        else:
            print("Selecione um valor valido: 0, 1 ou 2")

        mutex.release()

        time.sleep(2)

def servidor():

    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 65434        # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        print ('Socket binded to port', PORT)
        s.listen(3)
        print ('socket is listening')
        text_file = open("historiador.txt", "w")
        while True:
            conn, addr = s.accept()
            # print('Connected by', addr)
            data = conn.recv(1024)
            # print(data)
            text_file.write(str(data))
            text_file.write("\n")
def parentchild():
    n = os.fork()
    if n == 0:
        # Criando as threads
        process_thread_1 = threading.Thread(target=calculo_altura_integral_tanque_1)
        process_thread_2 = threading.Thread(target=calculo_altura_integral_tanque_2)
        softPLC = threading.Thread(target=controlador)
        logger_thread = threading.Thread(target=log_informacao)
        interface_thread = threading.Thread(target=selecionar_altura_tanque)


        # Começando novas Threads
        process_thread_1.start()
        process_thread_2.start()
        softPLC.start()
        logger_thread.start()
        interface_thread.start()

        threads = []
        threads.append(process_thread_1)
        threads.append(process_thread_2)
        threads.append(softPLC)
        threads.append(logger_thread)
        threads.append(interface_thread)

        for t in threads:
            t.join()

        print("Fim....")
    else:
        servidor()

mutex = threading.Lock()

altura_integral_1 = 0
altura_integral_2 = 0
q_input_tanque_1 = 2
q_input_tanque_2 = 2
tempo_2 = 0
tempo_1 = 0
altura_desejada_tanque_1 = 2
altura_desejada_tanque_2 = 1

parentchild()