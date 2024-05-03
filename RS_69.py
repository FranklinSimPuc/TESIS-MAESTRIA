from statistics import mean
from math import log,e
import time
import Clase_OpenDSS as OPEND
import Utilitarios_RS as UTILRS
import matplotlib.pyplot as plt

Sistema=69
timeo=time.time()
Objeto=OPEND.DSS(r"[C:\Users\Windows 10\Downloads\codigos\69_barras.dss]")
Objeto.compile_DSS()



C = 0.1 #Constante de To [0-1]
Nro_To=4 #Número de soluciones aleatorias para calculo de To 

Tf=0.01 #Temperatura final
max_vecinos=25  #Número máximo de vecinos para cada temperatura
max_RepFO = 20 #Número máximo de repeticiones de la FO
alpha1= 0.9  #Constante rápida geométrica
alpha2= 0.95   #Constate lenta geométrica
Klm=3   # Multiplicador de N° de veces las iteraciones para Lundy & Mees
Tlm=0.95  # Temperatura inicial para Lundy & Mees: Tlm es porcentaje de To

#Mallas del sistemas:
M1=[3,4,5,6,7,8,9,10,69,42,41,40,39,38,37,36,35]
M2=[43,44,45,71,14,13,12,11]
M3=[15,16,17,18,19,20,70]
M4=[46,47,48,49,72,58,57,56,55,54,53,52]
M5=[59,60,61,62,63,64,73,26,25,24,23,22,21]
Mallas=[M1,M2,M3,M4,M5]


SolIni=UTILRS.SolAle(Nro_To,Mallas).copy()
#print(SolIni)
PerdidasIni,PerdidaMin,SolucionMin=Objeto.FitnessIni(SolIni,'0')
#print(PerdidasIni,PerdidaMin,SolucionMin)
#print("Solución inicial = ",SolucionMin)
#print("Perdida inicial =" ,PerdidaMin)
PerdidaIni=PerdidaMin
SolucionIni=SolucionMin.copy()

PerdidasProm=mean(PerdidasIni)
#print(PerdidasProm)
To=-PerdidasProm/log(C) #LogC = LnC en python
#print('Temperatura inicial=',To)
SolucionOpt,Perdida,iter,Vector_T,Vector_FOm,Vector_FOact=UTILRS.SA_Mejorado(To,Tf,max_vecinos,max_RepFO,alpha1,alpha2,Klm,Tlm,SolucionIni,PerdidaMin,Mallas,Sistema)
print("Solución Final =" , SolucionOpt)
print("Pérdida final =",Perdida)

timef=time.time()
Tiempo=timef-timeo
print('tiempo= ',Tiempo,' seg')

Nombre_xlsx='Resultados '+str(Sistema)+'B_1Corrida_ISA-HC'+'.xlsx'
UTILRS.Escribir_xls_1corrida(Nombre_xlsx,iter,Vector_T,Vector_FOm,Vector_FOact)

fig=plt.figure(figsize=(10,5))
plt.ax=UTILRS.plot(iter,Vector_T)
plt.ax.set(xlabel='Nro Iteración',ylabel='Temperatura',title='Decrecimiento de Temperatura')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_1Corrida_ISA-HC_'+'T'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_1Corrida_ISA-HC_'+'T'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')

fig=plt.figure(figsize=(10,5))
plt.ax1=UTILRS.plot(iter,Vector_FOm)
plt.ax1.set(xlabel='Nro Iteración',ylabel='FO - Pérdidas',title='Función Objetivo')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_1Corrida_ISA-HC_'+'FOm'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_1Corrida_ISA-HC_'+'FOm'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')

fig=plt.figure(figsize=(10,5))
plt.ax1=UTILRS.plot(iter,Vector_FOact)
plt.ax1.set(xlabel='Nro Iteración',ylabel='FO - Pérdidas',title='Función Objetivo - Actual')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_1Corrida_ISA-HC_'+'FOact'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_1Corrida_ISA-HC_'+'FOact'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')