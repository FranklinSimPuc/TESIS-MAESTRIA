class DSS():
        def __init__(self, end_modelo_DSS):
            import win32com.client
            self.end_modelo_DSS = end_modelo_DSS
    
            # Criar a conexÃ£o entre Python e OpenDSS
            self.dssObj = win32com.client.Dispatch("OpenDSSEngine.DSS")
    
            # Iniciar o Objeto DSS
            if self.dssObj.Start(0) == False:
                print ("Problemas em iniciar o OpenDSS")
            else:
                # Criar variÃ¡veis paras as principais interfaces
                self.dssText = self.dssObj.Text
                self.dssCircuit = self.dssObj.ActiveCircuit
                self.dssSolution = self.dssCircuit.Solution
                self.dssCktElement = self.dssCircuit.ActiveCktElement
                self.dssBus = self.dssCircuit.ActiveBus
                self.dssLines = self.dssCircuit.Lines
                self.dssTransformers = self.dssCircuit.Transformers
                #self.dssEngine = self.dssObj.Engine
                #self.dssSwtControl = self.dssObj.SwtControls
                self.dssTopology = self.dssCircuit.Topology
                self.dssMeters = self.dssCircuit.Meters
                #self.dssBus = self.dssEngine
                self.dssLines = self.dssCircuit.Lines
                self.dssLoads = self.dssCircuit.Loads
                self.dssSwtControl = self.dssCircuit.SwtControls
        
        def n_loops_DSS(self):
            return self.dssTopology.NumLoops
    
        def versao_DSS(self):
    
            return self.dssObj.Version
    
        def compile_DSS(self):
    
            # Limpar informações da ultima simulação
            self.dssObj.ClearAll()
    
            self.dssText.Command = "compile " + self.end_modelo_DSS
    
        def solve_DSS_snapshot(self):
    
            # Configurações
            #self.dssText.Command = "Set Mode=Snap"
            #self.dssText.Command = "Set ControlMode=STATIC"
    
            # Resolve o Fluxo de Potência
            self.dssSolution.Solve()
    
        def get_resultados_potencia(self):
            self.dssText.Command = "Show powers kva elements"
    
        def get_nome_circuit(self):
            return self.dssCircuit.Name
        
        def switch_elemento(self,chave,estado):
            if (estado==1 or estado=='1'):
                self.dssText.Command = "SwtControl."+"S"+chave+".action=close"
            elif (estado==0 or estado=='0'):
                self.dssText.Command = "SwtControl."+"S"+chave+".action=open"
                
        def switch_elemento2(self, chave, estado):
            self.dssSwtControl.Name = chave
            if (estado==1) or (estado=='1'):
                self.dssSwtControl.Action = 0
            elif (estado==0) or (estado=='0'):
                self.dssSwtControl.Action = 1
                
        def matrixY(self):
            self.dssText.Command = "build Y"
            self.dssText.Command = "calcincmatrix"
            self.dssText.Command = "show Y"
        
        def get_line_losses (self):
            perdas,perdas2 = self.dssCircuit.LineLosses
            return perdas
        def get_nombre_Barras (self):
            Nombres = self.dssCircuit.AllBusNames
            return Nombres
        

        def get_nombre_Linea (self):
            Nombres = self.dssBus.LineList
            return Nombres


        def get_perdas_por_Lineas (self):
            Perdas = self.dssCircuit.AllElementLosses
            return Perdas
        def get_tensoes_DSS(self):
            return self.dssCircuit.AllBusVmag
            #return self.dssCircuit.AllBusMagPu
    
        def num_isolated_loads_DSS(self): #numero de cargas isoladas
            return self.dssTopology.NumIsolatedLoads
    
        def num_loops_DSS(self): #numero de malhas no circuito
            return self.dssTopology.NumLoops
        
        def ativa_elemento(self, nome_elemento):

            # Ativa elemento pelo seu nome completo Tipo.Nome
            self.dssCircuit.SetActiveElement(nome_elemento)
            
            # Retonar o nome do elemento ativado
            #return self.dssCktElement.Name
        
        def get_potencias_elemento(self):
            return self.dssCktElement.Powers
    
        def get_tensoes_elemento(self):
            return self.dssCktElement.VoltagesMagAng
        
        def get_barras_elemento(self):
    
            barras = self.dssCktElement.BusNames
    
            barra1 = barras[0]
            barra2 = barras[1]
    
            return barra1, barra2
        
        def get_names_lines(self):
            return self.dssLines.AllNames
        
        def get_buildYmatrix(self):
            import numpy as np
            NumNodes = self.dssCircuit.NumNodes
            #print (NumNodes)
            #print (self.dssCircuit.YNodeOrder)
            Y = np.asarray(self.dssCircuit.SystemY).view(dtype=np.complex).reshape((NumNodes, NumNodes))
            
            #ydata = self.dssCircuit.SystemY
            #Ymatrix = np.reshape(complex(float(','.join(str(elem) for elem in ydata[0:][::2])), float(','.join(str(elem) for elem in ydata[1:][::2]))), (NumNodes, NumNodes))
            #print (Ymatrix)
            #return Ymatrix
            return Y
            
            #return ydata
            #return self.dssCircuit.SystemY
    
        def get_dados_barras (self):

        
            AllBusNames = self.dssCircuit.AllBusNames
            #print (AllBusNames)
            carga_kW = []
            carga_kvar = []
            load_list = []
            tensoes_barras = []
            for i in range (len(AllBusNames)):
                self.dssCircuit.SetActiveBus (AllBusNames[i])
                load_list.append (self.dssBus.LoadList)
                tensoes_barras.append (self.dssBus.VMagAngle)
                if (load_list[i][0]):
                    self.dssCircuit.SetActiveElement(load_list[i][0])
                    carga_kW.append (self.dssCktElement.Powers[0])
                    carga_kW.append (self.dssCktElement.Powers[2])
                    carga_kW.append (self.dssCktElement.Powers[4])
                    carga_kvar.append (self.dssCktElement.Powers[1])
                    carga_kvar.append (self.dssCktElement.Powers[3])
                    carga_kvar.append (self.dssCktElement.Powers[5])
                else:
                    carga_kW.append (0)
                    carga_kW.append (0)
                    carga_kW.append (0)
                    carga_kvar.append (0)
                    carga_kvar.append (0)
                    carga_kvar.append (0)
                
            #print (AllBusNames)
            #print (load_list)
            #print (carga_kW)
            #print (carga_kvar)
            #print (tensoes_barras)
            
            
            return tensoes_barras, carga_kW, carga_kvar, load_list