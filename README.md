# RemoteControlLinuxIR

Projeto composto por 2 componentes: programa para Arduino e programa Python. O Arduino é o receptor do controle remoto e envia os códigos respectivos a cada tecla pressionada no controle remoto pela serial para o computador. O programa em python fica aguardando os comandos pela serial, interpreta e executa o mesmo na plataforma.

### Arduino

Utiliza o sensor xxxx ligados aos pinos X,X,X do arduino UNO. Utiliza a bibliteca de IR disponibilizada no diretorio Arduino. Esse programa converte o sinal infravermelho de diferentes controles para um código que é enviado pela serial.

### Host - Python

Programa que interpreta o código recebido pela serial e executa determinado comando. O programa pode executar comandos especifidados pelo usuário. No meu caso estou utilizando a ferramenta xdotool para simular entradas de teclado e mouse. 
O programa tem uma lógica para processar as teclas enviadas pelo controle remoto para tornar o sistema mais responsível e corrigir erros na recepção.

### Requerimentos

DRemoteControlLinuxIR requer os seguintes componetes para funcionar:

-  pyserial - biblioteca python para acesso a porta serial
- python 2 ou 3 - o programa que roda no host é em python
- xdotool - pacote para simular entrada teclas e mouse virtual

### Instalação

Para utilizar o programa no host é necessário ter python instalado. 

Instalar a biblioteca python pyserial:
```pip install pyserial```

Instalar a ferramente xdotool
```sudo apt install xdotool```

Instalar a extensão streamkeys no Chrome para ele aceitar as teclas multimedia.

Chamar no startup do linux (esse é um exemplo, pode variar dependendo da distribuicao):
```gnome-terminal -- /usr/bin/python /home/tv/controleRemoto.py```


### Problemas conhecidos

- O uso do xdotool pode apresentar problemas dependendo da distribuição linux utilizada. Foi encontrado um problema com Ubuntu 19, com shell Gnome. Sempre que o controle remoto era utilizado e uma tecla virtual era gerada a tela trava por alguns segundos. Isso é aparentemente um bug do Gnome Shell. O software funcionou corretamente no Lubuntu 19.
- Deve-se permitir acesso a porta serial, caso contrário o programa não consegue detectar o arduino. Para liberar a porta serial utilize:
sudo usermod -a -G dialout $USER
Após isso reinicie o sistema que ele deve funcionar.

### Todos

- Fazer documentação
- Reorganizar código
- Alterar tabela de configuracao dos comando para algo mais python e menos C 





