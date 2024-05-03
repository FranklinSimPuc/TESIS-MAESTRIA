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


C = 0.8 #Constante de To [0-1]
Nro_To = 1 #Número de soluciones aleatorias para calculo de To 

Tf=0.01 #Temperatura final
max_vecinos=25  #Número máximo de vecinos para cada temperatura
alpha1= 0.9  #Constante rápida geométrica

#Mallas del sistemas:
M1=[3,4,5,6,7,8,9,10,69,42,41,40,39,38,37,36,35]
M2=[43,44,45,71,14,13,12,11]
M3=[15,16,17,18,19,20,70]
M4=[46,47,48,49,72,58,57,56,55,54,53,52]
M5=[59,60,61,62,63,64,73,26,25,24,23,22,21]
Mallas=[M1,M2,M3,M4,M5]
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
    SolucionOpt,Perdida,iter,Vector_T,Vector_FOm,Vector_FOact=UTILRS.SA_joao(To,Tf,max_vecinos,alpha1,SolucionIni,PerdidaMin,Mallas,Sistema)

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
Nombre_xlsx='Resultados '+str(Sistema)+'B_C_joao_'+str(C)+'.xlsx'
UTILRS.Escribir_xls(Nombre_xlsx,Vec_Sim,Vec_To,Vec_SolucionIni,Vec_PerdidasIni,Vec_Tf,Vec_Solucion,Vec_Perdidas,Tiempo,
                    Vec_GlobalIter,Vec_GlobalT,Vec_GlobalFOm,Vec_GlobalFOact)

fig=plt.figure(figsize=(10,5))
plt.ax=UTILRS.plot(Vec_GlobalIter,Vec_GlobalT)
plt.ax.set(xlabel='Nro Iteración',ylabel='Temperatura',title='Decrecimiento de Temperatura')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_C_joao_'+str(C)+'T'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_C_joao_'+str(C)+'T'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')

fig=plt.figure(figsize=(10,5))
plt.ax1=UTILRS.plot(Vec_GlobalIter,Vec_GlobalFOm)
plt.ax1.set(xlabel='Nro Iteración',ylabel='FO - Pérdidas',title='Función Objetivo')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_C_joao_'+str(C)+'FOm'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_C_joao_'+str(C)+'FOm'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')

fig=plt.figure(figsize=(10,5))
plt.ax1=UTILRS.plot(Vec_GlobalIter,Vec_GlobalFOact)
plt.ax1.set(xlabel='Nro Iteración',ylabel='FO - Pérdidas',title='Función Objetivo - Actual')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_C_joao_'+str(C)+'FOact'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_C_joao_'+str(C)+'FOact'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')