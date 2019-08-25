# Recepção de control remoto

import time
import serial 
import os

VERSION = "0.1"
SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 9600

REPEATABLE = True
NOT_REPEATABLE = False
UNKNOW_COMMAND = '??'
NO_COMMAND = ''
NO_DESCRIPTION = ''
NO_IR_CODE = -1
#Lista de relacao entre codigo IR e comando linux. Formato [Codigo IR, Comando Linux, Descricao, Pode Repetir?]
command_list = [
	['E17AF807','amixer -q -D pulse sset Master toggle','mute',NOT_REPEATABLE],
	['BE3BB37','xdotool key XF86AudioRaiseVolume','aumenta volume',REPEATABLE],
	['D4D9F2A7','xdotool key XF86AudioLowerVolume','baixa volume',REPEATABLE],
	['21035431','xdotool mousemove_relative -- %MOUSE_MOVE 0','seta para direita',REPEATABLE],
	['983AB4C1','xdotool mousemove_relative -- -%MOUSE_MOVE 0','seta para esquerda',REPEATABLE],
	['C20370A1','xdotool mousemove_relative -- 0 -%MOUSE_MOVE','seta para cima',REPEATABLE],
	['81930A09','xdotool mousemove_relative -- 0 %MOUSE_MOVE','seta para baixo',REPEATABLE],
	['BB0ED9E1','xdotool click 1; sleep 0.2','ok',NOT_REPEATABLE],
	['AA7B2167','xdotool key XF86AudioPlay','play',NOT_REPEATABLE],
	['2E8C2A89','xdotool key XF86AudioNext','fwd',NOT_REPEATABLE],
	['1F6E01C9','xdotool key XF86AudioPrev','rew',NOT_REPEATABLE],
	['1D15F4D7','xdotool key XF86AudioStop','stop',NOT_REPEATABLE],
	['406A954D','systemctl poweroff -i','desliga',NOT_REPEATABLE],
	['E17A24DB','xset dpms force off; sleep 1','apaga tv',NOT_REPEATABLE],
	['E17A18E7','xdotool key C; sleep 1','apaga tv',NOT_REPEATABLE],
	['E17A7887','xdotool getwindowfocus getwindowname;sleep 1','pega nome janela em foco',NOT_REPEATABLE],
	['A26409C9','pkill --oldest chrome; google-chrome-stable deezer.com/br/ & sleep 1','Abre pagina deezer',NOT_REPEATABLE],
	['240C9161','pkill --oldest chrome; google-chrome-stable www.netflix.com & sleep 1','Abre pagina netflix',NOT_REPEATABLE],
	['68E839F1','pkill --oldest chrome; google-chrome-stable www.youtube.com & sleep 1','Abre pagina youtube',NOT_REPEATABLE],
	['ABBE1086','xdotool key Escape','esc',NOT_REPEATABLE], 
	['68E69B7F','xdotool click 4','scrool up',REPEATABLE],
	['223C02A7','xdotool click 5','scrool down',REPEATABLE]
]

#Codigo q corresponde a tecla repetida do IR. Tecla ainda esta apertada
button_down = 'FFFFFFFF'
#inicializa para evitar possivel chamada dessa variavel sem inicilizacao
linux_command = NO_COMMAND
last_command = NO_COMMAND
description = NO_DESCRIPTION
allow_repeat = NOT_REPEATABLE
repetition_count=0
last_ir_code = NO_IR_CODE
ir_code = NO_IR_CODE
#tempo max para interpretar que a tecla foi solta
IR_TIMEOUT = 0.3
#sinaliza q tecla esta pressionada desde ultima vez
pressed = False
#Maximo deslocamento do mouse
max_mouse = 35

# Hello message
print("Controle Remoto Arduino/Linux TabaJairo para controle Panasonic")
print("Versao: " + VERSION);


# Tenta conectar a serial
serial_connected = False
print("Procurando porta serial...")
while (not serial_connected):
	try:
		ser = serial.Serial(port=SERIAL_PORT,baudrate=BAUD_RATE, timeout=1)
		serial_connected = True
		print("yeah...achei")
	except:
		print("buuu...ainda não achei")
		time.sleep(1)
		

#Loop infinito - ctrl+c para terminar
while 1 :
	#Recebe ir code. Aguarda enquanto nao tem nada na serial
	last_ir_code = ir_code
	t = 0
	while ser.inWaiting() == 0:
		time.sleep(0.1)
		t = t + 0.1
		if t > IR_TIMEOUT:
			t=0
			#limpa ultimo codigo pois estourou timeout
			last_ir_code = NO_IR_CODE
	out = ser.readline().rstrip()
	ir_code = out.decode('utf-8')


	#Procura comando na lista
	#Coloca NO_COMMAND em linux_command para indicar q nao foi encontrado
	linux_command = NO_COMMAND
	for command in command_list:
		if ir_code == command[0]:
			linux_command = command[1]
			description = command[2]
			allow_repeat = command[3]

	# Se teve timeout na recepcao do codigo IR entao o ultimo comando eh vazio
	if last_ir_code == NO_IR_CODE:
		last_command = NO_COMMAND
		
	pressed = False
	#Verifica se eh comando repetido (tecla pressionada)
	if (linux_command == last_command) and (last_ir_code != NO_IR_CODE):
		pressed = True
		
	# Aqui tem um truque para melhor responsividade: se o comando atual nao eh reconhecido e 
	#  nao teve timeout na recepcap de IR supoe que houve problema na recepcao do codigo:
	#  o codigo eh diferente mas corresponde a ultima tecla pressionada
	if (linux_command == NO_COMMAND) and (last_ir_code != NO_IR_CODE) and (last_command != NO_COMMAND):
		pressed = True
		linux_command = last_command
		print("Codigo IR invalido! Provavelmente eh o ultimo comando, vamos repetir..."); 
	
	# Incrementa contador de botao pressionado
	if pressed:
		repetition_count+=1
	else:
		repetition_count=0

	# Atualiza last command. A posicao da linha eh importante para o codigo funcionar		
	last_command = linux_command
		
	#subsitui wildcard %MOUSE_MOVE do movimento do mouse para fazer aceleracao
	mouse_move = repetition_count*repetition_count+1;
	if mouse_move > max_mouse:
		mouse_move = max_mouse
	linux_command = linux_command.replace("%MOUSE_MOVE",str(mouse_move))	

	#executa comando se for conhecido. Verifica se ele pode ser repetido ou nao.
	# Nao queremos o play/pause repetindo, nem o mute por exemplo
	if linux_command != NO_COMMAND:
		if repetition_count == 0 or  (repetition_count > 0 and allow_repeat):
			print(ir_code + ' ' +  str(repetition_count) + ' --> ' + description + ' --> ' + linux_command); 
			os.system(linux_command)
		else:
			print(ir_code + ' ' +  str(repetition_count) + ' --> ' + description + ' --> nao pode repetir');
	else:
		print(ir_code + ' ' +  str(repetition_count) + ' --> buuu, nao conheco esse comando ');
