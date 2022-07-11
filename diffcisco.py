import os
import filecmp
from shutil import copyfile
from datetime import *

#definicion Variables

Fecha = date.today()
date = datetime.strptime(str(Fecha), "%Y-%m-%d")
dia=date.day
mes=date.month
Month=mes
if mes < 10:
        mes='0'+str(mes)
if dia < 10:
        dia='0'+str(dia)
anio=date.year

def escribe(Archivo,Texto1):
	if 'Time:' in Texto1:
		X=1
	elif '! NVRAM' in Texto1:
		X=1
	elif 'ntp clock-period ' in Texto1:
		X=1
	elif '! Last configuration change ' in Texto1:
		X=1
	elif 'Current configuration' in Texto1:
		X=1
	elif '!Running configuration last' in Texto1:
		X=1
	elif '!No configuration change since' in Texto1:
		X=1
	else:
		try:
			Texto1=Texto1.replace("\r","")
			Archivo.write(IP+" Linea distinta: "+Texto1+"\n")
		except IOError:
			print("No hay mas espacio en Disco")
			exit() 



def ComparaArchivo(File1,File2):
	Archivo1=open(File1,"r")
	Archivo2=open(File2,"r")
	for linea1 in Archivo1:
		try:
			#print(File1)
			B=1
			for A in Archivo2:
				#print(A)
				A=A.rstrip("\n")
				A=A.rstrip("\r")
				linea1=linea1.rstrip("\n")
				linea1=linea1.rstrip("\r")
				if linea1 == A:
					B=1
					Archivo2.seek(0)
					break
				else:
					B=0
			if B == 0:
				escribe(Salida,linea1)
				Archivo2.seek(0)
		except IndexError:
			print("ERROOOOOR")
	Archivo1.close()
	Archivo2.close()

	

#definicion funciones
def get_MesActual (mes):
	switcher = {
		1:"Jan",
		2:"Feb",
		3:"Mar",
		4:"Apr",
		5:"May",
		6:"Jun",
		7:"Jul",
		8:"Ago",
		9:"Sep",
		10:"Oct",
		11:"Nov",
		12:"Dec"
	}
	val = switcher.get(int(mes),"Mes Invalido")
	return val
	

DirectorioHoy='/Respaldos/RouterySwitch/'+str(anio)+'/'+str(mes)+'/'+str(dia)+''



if int(dia) - 1 < 1:
	auxmes=str(mes)
	if int(dia) == 1:
                auxday='0'+str(int(dia))
		auxmes='0'+str(int(mes)-1)
	elif int(mes) - 1 < 10:
                auxmes='0'+str(int(mes)-1)
        else:
                auxmes=str(int(mes)-1)
	DirectorioAyer='/Respaldos/RouterySwitch/'+str(anio)+'/'+auxmes+'/28'
else:
	if int(dia) == 1:
		auxday='0'+str(int(dia))
	elif int(dia) - 1 < 10:
	        auxday='0'+str(int(dia)-1)
	else:
		auxday=str(int(dia)-1)
	DirectorioAyer='/Respaldos/RouterySwitch/'+str(anio)+'/'+str(mes)+'/'+auxday+''

Salida=open("//Respaldos//SCRIPT//Cambios//salida"+str(anio)+""+str(mes)+""+str(dia)+".txt","w+")


DirHoy=os.listdir(DirectorioHoy)
DirAyer=os.listdir(DirectorioAyer)
print(DirectorioAyer,DirectorioHoy)
for file1 in DirHoy:
	Archivo1=DirectorioHoy+'/'+file1
	auxFile=file1
	auxFile=file1.split("-")
	IP=auxFile[0]
	auxFile2=auxFile[1]
	auxFile=auxFile2.split(".")
	auxFile2=auxFile[0]
	Auxdia=auxFile2[6:]
	auxayer=int(Auxdia)-1
	auxmes=auxFile2[:6]
	if int(auxayer) == 0:
		auxday=str(28)
		auxmes=auxmes[4:]
		auxmes=str(int(auxmes)-1)
		if int(auxmes) < 10:
			auxmes=str("0")+str(auxmes)
		auxmes=str(auxFile2[:4])+auxmes
	elif int(auxayer) == 10:
		auxday=str(auxayer)
	elif int(auxayer) - 1 < 10:
                auxday='0'+str(auxayer)
		#auxday=str(auxayer)
        else:
                auxday=str(auxayer)

	Archivo2=DirectorioAyer+'/'+IP+'-'+auxmes+str(auxday)+'.bkp'
	if os.path.exists(Archivo1):
		if os.path.exists(Archivo2):
			print("Comparando: "+Archivo1+" con:"+Archivo2)
			ComparaArchivo(Archivo1,Archivo2)
			ComparaArchivo(Archivo2,Archivo1)
		else:
			Salida.write('Configuracion no fue comparada:'+str(Archivo2)+"\n")
	else:
		Salida.write('Archivo1 no existe:'+str(Archivo1))
Salida.close()

