class boxDisp:
        def __init__(self, nBox, x, colOr, y, colVer, nEpsX, nEpsY):
            self.nBox=nBox
            self.disp=[x, colOr, y, colVer, nEpsX, nEpsY]

def riceviInput():
    x_p=int(input('Dimensione 1 del plt in mm:'))
    y_p=int(input('Dimensione 2 del plt in mm:'))
    x_c=int(input('Dimensione 1 del collo in mm:'))
    y_c=int(input('Dimensione 2 del collo in mm:'))
    # riorganizzazione delle coordinate in modo che x_c < y_c & x_p > y_p
    return (max(x_p, y_p), min(x_p, y_p)), (min(x_c, y_c), max(x_c, y_c))

def snailMethod(pltDims, boxDims):
    x_c=boxDims[0]
    y_c=boxDims[1]
    pltDims={'o':pltDims, 'v':pltDims[-1::-1]}
    #area box e plt
    surBox=x_c*y_c
    surPlt=pltDims['o'][0]*pltDims['o'][1]
    
    boxConfigs={'o':[], 'v':[]}

    nBoxTmp=-1

    for i in pltDims:
        thLim=False
        # Colli per colonna orizzontale, verticale nella disposizione del plt i-esima
        colOr=pltDims[i][1]//x_c
        colVer=pltDims[i][1]//y_c
        
        for x in range(1+pltDims[i][0]//y_c):
            y=(pltDims[i][0]-x*y_c)//x_c
            nEpsX=(pltDims[i][0]-x*y_c)//y_c
            nEpsY=(pltDims[i][1]-(pltDims[i][1]//y_c)*y_c)//x_c
            nEpsBox=(nEpsX)*(nEpsY)
            #Aggiorna e appendi la nuova disposizione al migliore solo se il numero di box è aumentato (*)
            if x*colOr+y*colVer+nEpsBox>nBoxTmp:
                nBoxTmp=x*colOr+y*colVer+nEpsBox 
                boxDispTmp=boxDisp(nBoxTmp, x, colOr, y, colVer, nEpsX, nEpsY)
                boxConfigs[i].append(boxDispTmp)            
            # Check sul limite teorico dato dall'area
            if nBoxTmp*surBox > surPlt-surBox: 
                thLim=True
                break
        if thLim: 
            break
    return boxConfigs

def optimizer(boxConfigs):

    emptyO=False if len(boxConfigs['o'])>0 else True
    emptyV=False if len(boxConfigs['v'])>0 else True

    #Oggetto (dizionario) che ha come informazione la disposizione del plt ottimale e le disposizioni dei colli all'interno
    bestDisp={
        'orientamento':None,
        'boxDisp':[]
    }

    if emptyV==True or (emptyO==False and boxConfigs['o'][-1].nBox > boxConfigs['v'][-1].nBox):
        #Caso best case orizzontale
        bestDisp['orientamento']='o'
        bestDisp['boxDisp']=boxConfigs['o'][-1].disp
    else:
        #Caso best case verticale
        bestDisp['orientamento']='v'
        bestDisp['boxDisp']=boxConfigs['v'][-1].disp
    return bestDisp

def constructor(bestDisp, pltDims, boxDims):
    x_c=boxDims[0]
    y_c=boxDims[1]
    retList=[]
    if bestDisp['orientamento']=='o':
        #Costruttore delle colonne orizzontali 
        coordTmp=[0, 0]
        for i in range(bestDisp['boxDisp'][1]): #iterazione sul numero di colonne orizzontali
            for j in range(bestDisp['boxDisp'][1]): #iterazione sulla cardinalità della colonna
                retList.append([coordTmp[0], coordTmp[1], y_c, x_c])
                coordTmp=[coordTmp[0], coordTmp[1]+x_c]
            coordTmp=[coordTmp[0]+y_c, 0]
        
        #Costruttore delle colonne verticali
        coordTmp=[pltDims['o'][0]-x_c, 0]
        for i in range(bestDisp['boxDisp'][2]): #iterazione sul numero di colonne verticali
            for j in range(bestDisp['boxDisp'][3]): #iterazione sulla cardinalità della colonna
                retList.append([coordTmp[0], coordTmp[1], x_c, y_c])
                coordTmp=[coordTmp[0], coordTmp[1]+y_c]
            coordTmp=[coordTmp[0]-x_c, 0]
        
        #Costruttore degli eps-colli
        coordTmp=[pltDims['o'][0]-y_c, pltDims['o'][1]-x_c]
        for i in range(bestDisp['boxDisp'][4]): #iterazione su eps-x
            for j in range(bestDisp['boxDisp'][5]): #iterazione su eps-y
                retList.append([coordTmp[0], coordTmp[1], y_c, x_c])
                coordTmp=[coordTmp[0], coordTmp[1]-x_c]
            coordTmp=[coordTmp[0]-y_c, coordTmp[1]-x_c]
        
    else:
        #Costruttore delle colonne orizzontali 
        coordTmp=[0, pltDims['v'][0]-y_c]
        for i in range(bestDisp['boxDisp'][0]): #iterazione sul numero di colonne orizzontali
            for j in range(bestDisp['boxDisp'][1]): #iterazione sulla cardinalità della colonna
                retList.append([coordTmp[0], coordTmp[1], x_c, y_c])
                coordTmp=[coordTmp[0]+x_c, coordTmp[1]]
            coordTmp=[0, coordTmp[1]-y_c]
        
        #Costruttore delle colonne verticali
        coordTmp=[0, 0]
        for i in range(bestDisp['boxDisp'][2]): #iterazione sul numero di colonne verticali
            for j in range(bestDisp['boxDisp'][3]): #iterazione sulla cardinalità della colonna
                retList.append([coordTmp[0], coordTmp[1], y_c, x_c])
                coordTmp=[coordTmp[0]+y_c, coordTmp[1]]
            coordTmp=[0, coordTmp[1]+x_c]
        
        #Costruttore degli eps-colli
        coordTmp=[pltDims['v'][1]-x_c, 0]
        for i in range(bestDisp['boxDisp'][4]):
            for j in range(bestDisp['boxDisp'][5]):
                retList.append([coordTmp[0], coordTmp[1], x_c, y_c])
                coordTmp=[coordTmp[0]-x_c, coordTmp[1]]
            coordTmp=[coordTmp[0], coordTmp[1]+y_c]

    return retList

info=riceviInput()

pltDims=info[0]
boxDims=info[1]

pltDict={'o':pltDims, 'v':pltDims[-1::-1]}

p=optimizer(snailMethod(pltDims, boxDims))

print(constructor(p, pltDict, boxDims))