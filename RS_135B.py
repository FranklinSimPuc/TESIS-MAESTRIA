from statistics import mean
from math import log,e
import time
import Clase_OpenDSS as OPEND
import Utilitarios_RS as UTILRS
import matplotlib.pyplot as plt

Sistema=135
timeo=time.time()
Objeto=OPEND.DSS(r"[D:\codigos\135Barras.dss]")
Objeto.compile_DSS()

C = 0.1 #Constante de To [0-1]
Nro_To=8 #Número de soluciones aleatorias para calculo de To 

Tf=0.01 #Temperatura final
max_vecinos=50  #Número máximo de vecinos para cada temperatura
max_RepFO = 40 #Número máximo de repeticiones de la FO
alpha1= 0.9  #Constante rápida geométrica
alpha2= 0.95   #Constate lenta geométrica
Klm=3   #Multiplicador de N° de veces las iteraciones para Lundy & Mees
Tlm=0.95  #Temperatura inicial para Lundy & Mees: Tlm es porcentaje de To

#Mallas del sistemas:
M1 = [1,2,3,4,5,6,8,9,137,24,22,20,19,18,17]
M2 = [99,100,101,103,149,90,89,88,86,85]
M3 = [121,122,123,125,127,129,148]
M4 = [75,76,154,126]
M5 = [77,155,128]
M6 = [78,79,145,131,130]
M7 = [63,64,65,66,144]
M8 = [91,147,104]
M9 = [92,150]
M10 = [132,151]
M11 = [133,134,135,156,98,97,93]
M12 = [80,81,83,84,146]
M13 = [25,140,51,48,47,46,45,43,42,40,39]
M14 = [7,136,73,70,68,67]
M15 = [10,13,15,138]
M16 = [26,27,28,31,35,38,139]
M17 = [52,53,54,55,142]
M18 = [118,119,120,143,62]
M19 = [94,95,96,152]
M20 = [49,50,141]
M21 = [153,110,107,106,105]

Mallas=[M1,M2,M3,M4,M5,M6,M7,M8,M9,M10,M11,M12,M13,M14,M15,M16,M17,M18,M19,M20,M21]
#print(Mallas)

i=0
Numero_sim=100 #Número de simulaciones
Vec_Perdidas=[0]*Numero_sim
Vec_PerdidasIni=[0]*Numero_sim
Vec_Solucion=[]
Vec_SolucionIni=[]
Vec_Sim=[0]*Numero_sim
Vec_To=[0]*Numero_sim
Vec_Tf=[0]*Numero_sim
bestPerdida=999999999999999999
maxIter=999999999999999999
Vec_GlobalT=[]
Vec_GlobalIter=[]
Vec_GlobalFOm=[]
Vec_GlobalFOact=[]

while i<Numero_sim:
    Objeto.compile_DSS()
    print(i)
    SolIni=UTILRS.SolAle(Nro_To,Mallas).copy()
    #print(SolIni)
    PerdidasIni,PerdidaMin,SolucionMin=Objeto.FitnessIni(SolIni,'0')
    #print(PerdidasIni,PerdidaMin,SolucionIni)
    #print("Solución inicial = ",SolucionMin)
    #print("Perdida inicial =" ,PerdidaMin)
    PerdidaIni=PerdidaMin
    SolucionIni=SolucionMin.copy()

    PerdidasProm=mean(PerdidasIni)
    To=-PerdidasProm/log(C) #LogC = LnC en python
    Vec_To[i]=To
    #print('Temperatura inicial=',To)
    SolucionOpt,Perdida,iter,Vector_T,Vector_FOm,Vector_FOact=UTILRS.SA_Mejorado(To,Tf,max_vecinos,max_RepFO,alpha1,alpha2,Klm,Tlm,SolucionIni,PerdidaMin,Mallas,Sistema)

    #print("Solución Final =" , SolucionOpt)
    #print("Pérdida final =",Perdida)
    Vec_Tf[i]=min(Vector_T)
    Vec_Perdidas[i]=Perdida
    Vec_Sim[i]=i+1
    Vec_Solucion.insert(i,str(SolucionOpt))
    Vec_SolucionIni.insert(i,str(SolucionIni))
    Vec_PerdidasIni[i]=PerdidaMin

    #index=Vector_FOm.index(Perdida)
    index=len(iter)
    if ((Perdida<bestPerdida) or (Perdida==bestPerdida and index<maxIter)):
        maxiter=index
        bestPerdida=Perdida
        Vec_GlobalT=Vector_T.copy()
        Vec_GlobalIter=iter.copy()
        Vec_GlobalFOm=Vector_FOm.copy()
        Vec_GlobalFOact=Vector_FOact.copy()

    i+=1

timef=time.time()
Tiempo=timef-timeo
print('tiempo= ',Tiempo,' seg')
Nombre_xlsx='Resultados '+str(Sistema)+'B_C_'+str(C)+'_SolIni_'+str(Nro_To)+'.xlsx'
UTILRS.Escribir_xls(Nombre_xlsx,Vec_Sim,Vec_To,Vec_SolucionIni,Vec_PerdidasIni,Vec_Tf,Vec_Solucion,Vec_Perdidas,Tiempo,
                    Vec_GlobalIter,Vec_GlobalT,Vec_GlobalFOm,Vec_GlobalFOact)

fig=plt.figure(figsize=(10,5))
plt.ax=UTILRS.plot(Vec_GlobalIter,Vec_GlobalT)
plt.ax.set(xlabel='Nro Iteración',ylabel='Temperatura',title='Decrecimiento de Temperatura')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_C'+str(C)+'_SolIni_'+str(Nro_To)+'_T'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_C'+str(C)+'_SolIni_'+str(Nro_To)+'_T'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')

fig=plt.figure(figsize=(10,5))
plt.ax1=UTILRS.plot(Vec_GlobalIter,Vec_GlobalFOm)
plt.ax1.set(xlabel='Nro Iteración',ylabel='FO - Pérdidas',title='Función Objetivo')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_C'+str(C)+'_SolIni_'+str(Nro_To)+'_FOm'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_C'+str(C)+'_SolIni_'+str(Nro_To)+'_FOm'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')

fig=plt.figure(figsize=(10,5))
plt.ax1=UTILRS.plot(Vec_GlobalIter,Vec_GlobalFOact)
plt.ax1.set(xlabel='Nro Iteración',ylabel='FO - Pérdidas',title='Función Objetivo - Actual')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_C'+str(C)+'_SolIni_'+str(Nro_To)+'_FOact'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_C'+str(C)+'_SolIni_'+str(Nro_To)+'_FOact'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')