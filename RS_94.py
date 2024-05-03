from statistics import mean
from math import log,e
import time
import Clase_OpenDSS as OPEND
import Utilitarios_RS as UTILRS
import matplotlib.pyplot as plt

Sistema=94
timeo=time.time()
Objeto=OPEND.DSS(r"[C:\Users\Windows 10\Downloads\codigos\94Barras.dss]")
Objeto.compile_DSS()


C = 0.1 #Constante de To [0-1]
Nro_To=6 #Número de soluciones aleatorias para calculo de To 

Tf=0.01 #Temperatura final
max_vecinos=35  #Número máximo de vecinos para cada temperatura
max_RepFO = 30 #Número máximo de repeticiones de la FO
alpha1= 0.9  #Constante rápida geométrica
alpha2= 0.95   #Constate lenta geométrica
Klm=3   # Multiplicador de N° de veces las iteraciones para Lundy & Mees
Tlm=0.95  # Temperatura inicial para Lundy & Mees: Tlm es porcentaje de To

#Mallas del sistemas:

M1= [84,55,54,53,52,51,50,49,48,47] #10
M2= [1,2,3,4,5,6,7,85,60,59,58,57,56] #13
M3= [11,86,43] #3
M4= [65,66,67,68,69,70,71,72,87] #9
M5= [73,74,75,76,88,13] #6
M6= [12,14,89,18,17] #5
M7= [25,26,90,16,15] #5
M8= [77,78,79,80,81,82,83,91,20,19] #10
M9= [30,31,32,92,28,27] #6
M10= [35,36,37,38,39,93,29] #7
M11= [44,45,46,94,34,33] #6
M12= [40,95,42,41] #4
M13= [96,64,63,62,61] #5

Mallas=[M1,M2,M3,M4,M5,M6,M7,M8,M9,M10,M11,M12,M13]


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