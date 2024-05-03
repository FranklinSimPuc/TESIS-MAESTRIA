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

    index=Vector_FOm.index(Perdida)
    if index<maxIter:
        maxiter=index
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