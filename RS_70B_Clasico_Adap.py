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


C = 0.8 #Constante de To [0-1]

Tf=0.0009 #Temperatura final
max_vecinos=35  #Número máximo de vecinos para cada temperatura
alpha1= 0.85  #Constante rápida geométrica

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
    SolIni=UTILRS.SolAle(1,Mallas).copy()
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
    SolucionOpt,Perdida,iter,Vector_T,Vector_FOm,Vector_FOact=UTILRS.SA_Clasico(To,Tf,max_vecinos,alpha1,SolucionIni,PerdidaMin,Mallas,Sistema)

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
Nombre_xlsx='Resultados '+str(Sistema)+'B_clasico_Adap_'+str(C)+'.xlsx'
UTILRS.Escribir_xls(Nombre_xlsx,Vec_Sim,Vec_To,Vec_SolucionIni,Vec_PerdidasIni,Vec_Tf,Vec_Solucion,Vec_Perdidas,Tiempo,
                    Vec_GlobalIter,Vec_GlobalT,Vec_GlobalFOm,Vec_GlobalFOact)

fig=plt.figure(figsize=(10,5))
plt.ax=UTILRS.plot(Vec_GlobalIter,Vec_GlobalT)
plt.ax.set(xlabel='Nro Iteración',ylabel='Temperatura',title='Decrecimiento de Temperatura')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_clasico_Adap_'+str(C)+'T'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_clasico_Adap_'+str(C)+'T'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')

fig=plt.figure(figsize=(10,5))
plt.ax1=UTILRS.plot(Vec_GlobalIter,Vec_GlobalFOm)
plt.ax1.set(xlabel='Nro Iteración',ylabel='FO - Pérdidas',title='Función Objetivo')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_clasico_Adap_'+str(C)+'FOm'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_clasico_Adap_'+str(C)+'FOm'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')

fig=plt.figure(figsize=(10,5))
plt.ax1=UTILRS.plot(Vec_GlobalIter,Vec_GlobalFOact)
plt.ax1.set(xlabel='Nro Iteración',ylabel='FO - Pérdidas',title='Función Objetivo - Actual')
plt.grid()
#plt.show()
nombre=str(Sistema)+'B_clasico_Adap_'+str(C)+'FOact'+'.pdf'
plt.savefig(nombre, dpi=300, bbox_inches='tight')
nombre=str(Sistema)+'B_clasico_Adap_'+str(C)+'FOact'+'.png'
plt.savefig(nombre, dpi=300, bbox_inches='tight')