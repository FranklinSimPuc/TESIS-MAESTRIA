from statistics import mean
from math import log,e
import time
import Clase_OpenDSS as OPEND
import Utilitarios_RS as UTILRS
import matplotlib.pyplot as plt

Sistema=70
timeo=time.time()
Objeto=OPEND.DSS(r"[D:\codigos\70_barras.dss]")
Objeto.compile_DSS()

C = 0.1 #Constante de To [0-1]
Nro_To=4 #Número de soluciones aleatorias para calculo de To 

Tf=0.01 #Temperatura final
max_vecinos=25  #Número máximo de vecinos para cada temperatura
max_RepFO = 50  #Número máximo de repeticiones de la FO
alpha1= 0.85  #Constante rápida geométrica
alpha2= 0.95   #Constate lenta geométrica
Klm=3  # Multiplicador de N° de veces las iteraciones para Lundy & Mees
Tlm=0.95  # Temperatura inicial para Lundy & Mees: Tlm es porcentaje de To

#Mallas del sistemas:
M1=[1,2,3,4,5,6,7,8,69,51,50,49,48,36,35,34,33,32,31]
M2=[70,39,38,37]
M3=[75,44,43,42,41,40]
M4=[78,71,47]
M5=[9,10,11,12,13,14]
M6=[79,72,23,22,21,20,19,18,17]
M7=[76,60,59,58,53,52]
M8=[45,46,74,61]
M9=[54,55,56,62,63,66,67,68]
M10=[24,25,26,27,28,77]
M11=[29,30,73,65,64]
Mallas=[M1,M2,M3,M4,M5,M6,M7,M8,M9,M10,M11]
#[51, 70, 75, 78, 13, 79, 76, 45, 66, 77, 30]

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

Nombre_xlsx='Resultados '+str(Sistema)+'B_1Corrida_ISA-HC_'+str(C)+'.xlsx'
UTILRS.Escribir_xls_1corrida(Nombre_xlsx,iter,Vector_T,Vector_FOm,Vector_FOact)

fig=plt.figure(figsize=(10,5))
plt.ax=UTILRS.plot(iter,Vector_T)
plt.ax.set(xlabel='Nro Iteración',ylabel='Temperatura',title='Decrecimiento de Temperatura')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_1Corrida_ISA-HC_'+str(C)+'T'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_1Corrida_ISA-HC_'+str(C)+'T'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')

fig=plt.figure(figsize=(10,5))
plt.ax1=UTILRS.plot(iter,Vector_FOm)
plt.ax1.set(xlabel='Nro Iteración',ylabel='FO - Pérdidas',title='Función Objetivo')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_1Corrida_ISA-HC_'+str(C)+'FOm'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_1Corrida_ISA-HC_'+str(C)+'FOm'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')

fig=plt.figure(figsize=(10,5))
plt.ax1=UTILRS.plot(iter,Vector_FOact)
plt.ax1.set(xlabel='Nro Iteración',ylabel='FO - Pérdidas',title='Función Objetivo - Actual')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_1Corrida_ISA-HC_'+str(C)+'FOact'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_1Corrida_ISA-HC_'+str(C)+'FOact'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')