from statistics import mean
from math import log,e
import time
import Clase_OpenDSS as OPEND
import Utilitarios_RS as UTILRS
import matplotlib.pyplot as plt

Sistema=5
timeo=time.time()
Objeto=OPEND.DSS(r"[C:\Users\Windows 10\Downloads\codigos\5Barras.dss]")
Objeto.compile_DSS()


C = 0.1 #Constante de To [0-1]
Nro_To=2 #Número de soluciones aleatorias para calculo de To 

Tf=0.01 #Temperatura final
max_vecinos=5  #Número máximo de vecinos para cada temperatura
max_RepFO = 20 #Número máximo de repeticiones de la FO
alpha1= 0.9   #Constante rápida geométrica
alpha2= 0.95   #Constate lenta geométrica
Klm=3   # Multiplicador de N° de veces las iteraciones para Lundy & Mees
Tlm=0.95  # Temperatura inicial para Lundy & Mees: Tlm es porcentaje de To

#Mallas del sistemas:
M1=[1,2,3]
M2=[4,5]
M3=[6,7]
Mallas=[M1,M2,M3]
#print(Mallas)


SolIni=UTILRS.SolAle(Nro_To,Mallas)
#print(SolIni)
PerdidasIni,PerdidaMin,SolucionMin=Objeto.FitnessIni(SolIni,'0')
#print(PerdidasIni,PerdidaMin,SolucionIni)
#print("Solución inicial = ",SolucionMin)
#print("Perdida inicial =" ,PerdidaMin)
PerdidaIni=PerdidaMin
SolucionIni=SolucionMin.copy()


PerdidasProm=mean(PerdidasIni)
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