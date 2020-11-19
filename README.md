# pythonthread
README
-------------------------------------------

Programa que implementa 3 threads para o controle do nível de 2 tanques:

Para executá-lo basta rodar o comando no terminal linux dentro da pasta onde se encontra o arquivo:

python trabalho_atr_pt_1.py

O projeto conta com uma biblioteca para a execução do controlador PID, para instalá-la é necassário rodar 
o seguinte comando no terminal:

pip install simple-pid


Ou se preferir, a biblioteca conta com o pyproject, para não ter que instalar nenhuma dependencia no seu computador, basta ter o poetry instalado e pelo terminal, dentro do diretorio, rodar o comando poetry install.

No caso de utilização do poetry executar o arquivo com o seguinte comando:

poetry run python trabalho_atr_pt_1.py
--------------------------------------------


É importante ressaltar que será exibido no terminal um print que mostra os valores da altura atual dos tanques 1 e 2
e o valor da vazão de entrada dos tanques 1 e 2.

EXEMPLO DE DADO EXIBIDO NO TERMINAL:

Dados tanque 1:
Altura tanque 1:  1.5036402176959751 Entrada tanque 1:  1.7822013822745706
Dados tanque 2:
Altura tanque 2:  0.9621921020908177 Entrada tanque 2:  0.24313975131324408

-------------------------------------------

É importante ressaltar que o arquivo log.txt será armazenado no mesmo diretório do programa.

--------------------------------------------

Além disso, o arquivo historiador.txt que registra as informações de altura, vazão e altura de referência,
enviados pelo cliente da comunicação socket também será armazenado no mesmo diretório do programa.

As linhas que printam as informações armazenadas no arquivo historiador.txt no terminal foram comentadas à fim 
de permitir que o usuário continue fornecendo valores de altura de referência para os tanques 1 e 2.

Para ver as informações printadas na tela é necessário descomentar as linhas 237 e 239 do programa, mas ao fazer 
isso não será possível entrar com valores de altura de referência mais.
