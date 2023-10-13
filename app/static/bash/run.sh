#!/bin/bash
#Autor: Faguiro

vermelho="\e[31m"
verde="\e[32m"
amarelo="\e[33m"
reset="\e[0m" 


mensagem="---------- AmazonClip Flask-CLI ----------   
  ____           _____                     _             
 | __ )  _   _  |  ___|__ _   __ _  _   _ (_) _ __  ___  
 |  _ \ | | | | | |_  / _` | / _` || | | || || '__|/ _ \ 
 | |_) || |_| | |  _|| (_| || (_| || |_| || || |  | (_) |
 |____/  \__, | |_|   \__,_| \__, | \__,_||_||_|   \___/ 
         |___/               |___/ faguiro2005@gmail.com"

mensagem_colorida="${verde}${mensagem}${reset}"
echo -e "${mensagem_colorida}"
sleep 3 

mensagem="ativando o ambiente virtual..." 
mensagem_colorida="${amarelo}${mensagem}${reset}"
echo -e "${mensagem_colorida}"
sleep 1

source venv/Scripts/activate
activate=$?

if [ $activate -eq 0 ]; then
    mensagem="ambiente virtual ativado com sucesso!"
    mensagem_colorida="${verde}${mensagem}${reset}"
    echo -e "${mensagem_colorida}"
else
    mensagem="Erro: ativar o ambiente virtual, código de retorno $activate"
    mensagem_colorida="${vermelho}${mensagem}${reset}"
    echo -e "${mensagem_colorida}"
    sleep 1

    mensagem="instalando os requisitos..."
    mensagem_colorida="${amarelo}${mensagem}${reset}"
    echo -e "${mensagem_colorida}"
    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt
    source venv/Scripts/activate
    sleep 1
    sucesso=$?
    if [ $sucesso -eq 0 ]; then
        mensagem="ambiente virtual ativado com sucesso após instalar os requisitos!"
        mensagem_colorida="${verde}${mensagem}${reset}"
        echo -e "${mensagem_colorida}"
        sleep 1
    else
        mensagem="Erro: ativar o ambiente virtual, código de retorno $sucesso"
        mensagem_colorida="${vermelho}${mensagem}${reset}"
        echo -e "${mensagem_colorida}"
        sleep 1
        exit 1
    fi
fi


mensagem="Exportando variáveis de ambiente..."
mensagem_colorida="${amarelo}${mensagem}${reset}"
echo -e "${mensagem_colorida}"
sleep 1

export FLASK_ENV=development
export FLASK_APP=microblog.py
export FLASK_DEBUG=1
export FLASK_RUN_PORT=6200
export FLASK_RUN_HOST=0.0.0.0

mensagem="OK!"
mensagem_colorida="${verde}${mensagem}${reset}"
echo -e "${mensagem_colorida}"
sleep 1

mensagem="executando flask run..."
mensagem_colorida="${amarelo}${mensagem}${reset}"
echo -e "${mensagem_colorida}"

flask run 

