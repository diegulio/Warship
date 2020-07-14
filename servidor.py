import random
import socket
import sys
def enviarMensaje(mensaje):
    connection.sendall(mensaje)
    return True
def verificarDistribucionBarcosCliente():
    data = connection.recv(50)
    print  'Mensaje recibido:'
    if data == 'listo':
        return True
    return data
def verificarTurno():
    data = connection.recv(50)
    print  'Mensaje recibido:' , data
    if str(data) == 'turno':
        mensaje=enviarMensaje('--')
        return True
    if data == 'Tu enemigo ha acertado a uno de tus barcos':
        enviarMensaje('turno')
        return False
    if data == '¡El otro jugador se ha Rendido!':
        raise ValueError
    if data=='HAS PERDIDO LA GUERRA':
        raise ValueError
    return False
def recibirBarcosEnemigos():
    data = connection.recv(50)
    return data

#EN PROCESO ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def verificarDestruccion(tableroBarcos,coordenada):
    tableroNuevo=tableroVirgen()
    contadorFilas=0
    for fila in tableroNuevo:
        contadorColumna=0
        for columna in fila:
            if coordenada==columna:
                if tableroBarcos[contadorFilas][contadorColumna] == ' T':
                    return 'T'
                    
                if tableroBarcos[contadorFilas][contadorColumna] == ' A':
                    return 'A'
                if tableroBarcos[contadorFilas][contadorColumna] == ' P':
                    return 'P'
                    
            contadorColumna+=1
        contadorFilas+=1
    return True
def juegoCompleto(jugador1F):
    contadorSurrender=0
    bandera=True
    contadorP=0
    contadorA=0
    contadorT=0
    contadorA2=0
    contadorP2=0
    contadorT2=0
    contadorGlobal1=0
    contadorGlobal2=0
    bandera1=True
    bandera2=True
    while bandera:
        while bandera1:
            print 'ES TURNO DE COLOCAR LOS BARCOS AL JUGADOR' , jugador1F
            distribuirBarcoJug1=distribuirBarcos(tableroBarcosJug1)
            bandera1=False
        barcosEnemigos=distribuirBarcosEnemigos(tableroBarcosJug2)
        enviarMensajes=enviarMensaje('listo')
        print 'esperando a que el otro jugador coloque sus barcos'
        banderaAtaque=verificarDistribucionBarcosCliente()
        while bandera2 and banderaAtaque:
            while verificarTurno() and bandera2:
                if contadorGlobal1==15:
                    print '¡HEMOS GANADO LA GUERRA COMANDANTE!',jugador1
                    enviarMensaje('HAS PERDIDO LA GUERRA')
                    raise ValueError
                    bandera2=False
                print'Es el turno de atacar del jugador' , jugador1F
                print 'ha acertado' ,contadorGlobal1,'veces'
                if contadorSurrender%7==0:
                    print 'Para rendirte debes escribir surrender al momento de atacar'
                atacar=solicitarAtaque(tableroAtaqueJug1,tableroBarcosJug2,tableroBarcosJug1)
                if atacar=='surrender':
                    print >>sys.stderr,'TE HAS RENDIDO'
                    enviarMensaje('¡El otro jugador se ha Rendido!')
                    raise ValueError
                aciertoJug1=verificarAciertos(tableroBarcosJug2,atacar)
                if aciertoJug1== True:
                    contadorGlobal1+=1
                    if verificarDestruccion(tableroBarcosJug2,atacar)=='T':
                        contadorT+=1
                        if contadorT==3:
                            print >>sys.stderr,'¡HAS DESTRUIDO A TOR!'
                            enviarMensaje('TE HAN DESTRUIDO A TOR')
                    if verificarDestruccion(tableroBarcosJug2,atacar)=='A':
                        contadorA+=1
                        if contadorA==5:
                            print >>sys.stderr,'¡HAS DESTRUIDO A ARMIN!'
                            enviarMensaje('TE HAN DESTRUIDO A ARMIN')
                    if verificarDestruccion(tableroBarcosJug2,atacar)=='P':
                        contadorP+=1
                        if contadorP==7:
                            print >>sys.stderr,'¡HAS DESTRUIDO A PIOTTOR!'
                            enviarMensaje('TE HAN DESTRUIDO A PIOTTOR')
                    enviarMensajeAcertado=enviarMensaje('Tu enemigo ha acertado a uno de tus barcos')
                else:
                    mensaje1='turno' 
                    cambioTurno=enviarMensaje(mensaje1)
                    contadorSurrender+=1
                print 'esperando el ataque del otro jugador'
        bandera=False
    return False
def distribuirBarcosEnemigos(tablero):
    barcosEnemigos=recibirBarcosEnemigos()
    posiciones=barcosEnemigos.split(',')
    for elemento in posiciones:
        coordenada=str(elemento[0])+str(elemento[1])
        orientacion=str(elemento[2])
        barco=str(elemento[3])
        contadorFila=0
        for fila in tablero:
            contadorColumna=0
            for columna in fila:
                if coordenada == columna:
                    if orientacion == 'H':
                        contador1=0
                        if barco== 'T':
                            while contador1<3:
                                fila[contadorColumna-1+contador1]= ' '+str(barco)
                                contador1+=1
                        if barco== 'A':
                            while contador1<5:
                                fila[contadorColumna-2+contador1]= ' '+str(barco)
                                contador1+=1
                        if barco== 'P':
                            while contador1<7:
                                fila[contadorColumna-3+contador1]= ' '+str(barco)
                                contador1+=1
                    if orientacion == 'V':
                        contador1=0
                        if barco== 'T':
                            while contador1<3:
                                x=contadorFila-1+contador1
                                tablero[x][contadorColumna]= ' '+str(barco)
                                contador1+=1
                        if barco== 'A':
                            while contador1<5:
                                x=contadorFila-2+contador1
                                tablero[x][contadorColumna]= ' '+str(barco)
                                contador1+=1
                        if barco== 'P':
                            while contador1<7:
                                x=contadorFila-3+contador1
                                tablero[x][contadorColumna]= ' '+str(barco)
                                contador1+=1
                contadorColumna+=1                    
            contadorFila+=1
    return tablero
                    
            
                
                
def verificarAciertos(tableroBarcos,coordenada):
    tableroNuevo=tableroVirgen()
    contadorFila=0
    acierto=False
    for fila in tableroNuevo:
        contadorColumna=0
        for columna in fila:
            if coordenada==columna:
                if tableroBarcos[contadorFila][contadorColumna] == ' T':
                    print 'oh! has acertado el ataque!.Repites turno! :D' 
                    return True
                if tableroBarcos[contadorFila][contadorColumna] == ' A':
                    print 'oh! has acertado el ataque!.Repites turno! :D' 
                    return True
                if tableroBarcos[contadorFila][contadorColumna] == ' P':
                    print 'oh! has acertado el ataque!.Repites turno! :D' 
                    return True
            contadorColumna+=1
        contadorFila+=1
    print 'oh ... has fallado el ataque :( . Suerte para la Proxima!'
    return acierto
def mostrarTablero(tablero):
    for fila in tablero:
        print fila
    return tablero 
def verificarLimites(coordenadaEntrante,barco,orientacion):
    bandera= True
    while bandera:
        try:
            comprobacion1= False
            comprobacion2= False 
            letras=['A','B','C','D','E','F','G','H','I','J']
            numeros=['0','1','2','3','4','5','6','7','8','9']
            if barco == 0 and orientacion=='V':
                letras.remove('A')
                letras.remove('J')
            if barco == 0 and orientacion=='H':
                numeros.remove('0')
                numeros.remove('9')
            if barco == 1 and orientacion=='V':
                letras.remove('A')
                letras.remove('B')
                letras.remove('J')
                letras.remove('I')
            if barco == 1 and orientacion=='H':
                numeros.remove('0')
                numeros.remove('1')
                numeros.remove('8')
                numeros.remove('9')
            if barco == 2 and orientacion=='V':
                letras.remove('A')
                letras.remove('B')
                letras.remove('C')
                letras.remove('H')
                letras.remove('I')
                letras.remove('J')
            if barco == 2 and orientacion=='H':
                numeros.remove('0')
                numeros.remove('1')
                numeros.remove('2')
                numeros.remove('7')
                numeros.remove('8')
                numeros.remove('9')
            i=0
            while i<len(letras):
                j=0
                if letras[i]==coordenadaEntrante[0]:
                    comprobacion1=True
                while comprobacion1==True:
                    if numeros[j]==coordenadaEntrante[1]:
                        comprobacion2=True
                        if comprobacion1== True and comprobacion2== True and len(coordenadaEntrante)==2: 
                            return True
                        
                    j+=1
                if i==11:
                    print "por favor ingrese coordenadas correctas."
                    return False
                i+=1
                
        except IndexError:
            print "coordenada Erronea. por favor ingresar nuevamente."
            return False 
        except AttributeError:
            print "coordenada Erronea. por favor ingresar nuevamente."
            return False
        except TypeError:
            print "coordenada erronea. por favor ingresar nuevamente."
        print "coordenada Erronea. por favor ingresar nuevamente."
        return False 
        bandera = False
def verificarDisponibilidadBarco(coordenada,tableroBarcos,tableroVirgen):
    contadorFilas=0
    for fila in tableroVirgen:
        contadorColumnas=0
        for columna in fila:
            if coordenada==columna:
                if tableroBarcos[contadorFilas][contadorColumnas] == ' T':
                    return False
                if tableroBarcos[contadorFilas][contadorColumnas] == ' A':
                    return False
                if tableroBarcos[contadorFilas][contadorColumnas] == ' P':
                    return False
            contadorColumnas+=1
        contadorFilas+=1
    return True 
def verificarVerticalHorizontal():
    bandera = True 
    while bandera:
        direccionNueva=raw_input('Ingrese direccion del desplazamiento del barco. V para que sea vertical y H para que sera horizontal:V o H?')
        direccion=direccionNueva.upper()
        try :
            if direccion == 'V':
                return direccion
            if direccion == 'H':
                return direccion 
            else:
                print 'Ingresar V o H. Por favor.'
        except IndexError:
            print 'Ingresar V o H. Por favor.(INDEX)'
        except AttributeError:
            print 'Ingresar V o H. Por favor.(Attribute)' 
def verificarEspacio(tablero,coordenada,orientacion,barco):
    contador=0
    while contador<len(barco):
        contadorFilas=0
        for fila in tablero:
            contadorColumnas=0
            for columna in fila:
                if coordenada == columna:
                    if orientacion == 'H':
                        if barco == 'Tor':
                            contador1=0
                            while contador1<len(barco):
                                if fila[contadorColumnas-1+contador1]== ' T' or fila[contadorColumnas-1+contador1]== ' A' or fila[contadorColumnas-1+contador1]== ' P':
                                    return False     
                                contador1+=1
                        if barco== 'Armin':
                            contador1=0
                            while contador1<len(barco):
                                if fila[contadorColumnas-2+contador1]== ' T' or fila[contadorColumnas-2+contador1]== ' A' or fila[contadorColumnas-2+contador1]== ' P':
                                    return False
                                contador1+=1
                        if barco== 'Piottor':
                            contador1=0
                            while contador1<len(barco):
                                if fila[contadorColumnas-3+contador1]== ' T' or fila[contadorColumnas-3+contador1]== ' A' or fila[contadorColumnas-3+contador1]== ' P':
                                    return False 
                                contador1+=1
                    if orientacion == 'V':
                        if barco== 'Tor':
                            contador1=0
                            while contador1<len(barco):
                                x=contadorFilas-1+contador1
                                if tablero[x][contadorColumnas]== ' T' or tablero[x][contadorColumnas]== ' A' or tablero[x][contadorColumnas]== ' P':
                                    return False
                                contador1+=1
                        if barco== 'Armin':
                            contador1=0
                            while contador1<len(barco):
                                x=contadorFilas-2+contador1
                                if tablero[x][contadorColumnas]== ' T' or tablero[x][contadorColumnas]== ' A' or tablero[x][contadorColumnas]== ' P':
                                    return False
                                contador1+=1
                        if barco== 'Piottor':
                            contador1=0
                            while contador1<len(barco):
                                x=contadorFilas-3+contador1
                                if tablero[x][contadorColumnas]== ' T' or tablero[x][contadorColumnas]== ' A' or tablero[x][contadorColumnas]== ' P':
                                    return False 
                                contador1+=1
                contadorColumnas+=1                    
            contadorFilas+=1
            contador+=1
    return True 
        
def distribuirBarcos(tablero):
    mostrartablero=mostrarTablero(tablero)
    listaBarcos=['Tor','Armin','Piottor']
    contador=0
    posiciones=''
    while contador<len(listaBarcos):
        barco=listaBarcos[contador]
        variable=''
        l=len(barco)
        print 'Es momento de posicionar a', barco , '!!!. Barco de largo ', l 
        verticalHorizontal=verificarVerticalHorizontal()
        coordenada=raw_input('ingrese coordenada para distribuir(coordenada de pivote):')
        coordenadaVerificada=verificarFormato(coordenada)
        coordenadaLimitada=verificarLimites(coordenadaVerificada,contador,verticalHorizontal)
        if coordenadaLimitada == True:
            coordenadaDisponible=verificarDisponibilidadBarco(coordenadaVerificada,tablero,tableroVirgen())
            if coordenadaDisponible == True:
                espacioVerificado=verificarEspacio(tablero,coordenadaVerificada,verticalHorizontal,listaBarcos[contador])
                if espacioVerificado==True:
                    contadorFila=0
                    for fila in tablero:
                        contadorColumna=0
                        for columna in fila:
                            if coordenadaVerificada == columna:
                                    if contador>0:
                                        posiciones=posiciones + ',' 
                                    if verticalHorizontal == 'H':
                                        contador1=0
                                        if barco== 'Tor':
                                            while contador1<len(barco):
                                                fila[contadorColumna-1+contador1]= ' '+str(barco[0])
                                                contador1+=1
                                        if barco== 'Armin':
                                            while contador1<len(barco):
                                                fila[contadorColumna-2+contador1]= ' '+str(barco[0])
                                                contador1+=1
                                        if barco== 'Piottor':
                                            while contador1<len(barco):
                                                fila[contadorColumna-3+contador1]= ' '+str(barco[0])
                                                contador1+=1
                                    if verticalHorizontal == 'V':
                                        
                                        contador1=0
                                        if barco== 'Tor':
                                            while contador1<len(barco):
                                                x=contadorFila-1+contador1
                                                tablero[x][contadorColumna]= ' '+str(barco[0])
                                                contador1+=1
                                        if barco== 'Armin':
                                            while contador1<len(barco):
                                                x=contadorFila-2+contador1
                                                tablero[x][contadorColumna]= ' '+str(barco[0])
                                                contador1+=1
                                        if barco== 'Piottor':
                                            while contador1<len(barco):
                                                x=contadorFila-3+contador1
                                                tablero[x][contadorColumna]= ' '+str(barco[0])
                                                contador1+=1   
                            contadorColumna+=1                    
                        contadorFila+=1
                    mostrartablero=mostrarTablero(tablero)
                    posiciones=posiciones + str(coordenadaVerificada) + str(verticalHorizontal) + str(barco[0])
                    contador+=1
                else:
                    print 'los barcos topan!! intenta con una coordenada u orientación distinta'
            else:
                print "ingresar coordenada no utilizada"
        else:
            print "El barco excederá los limites del tablero, por favor ingresar dentro de los parametros"
    print posiciones
    enviarMensaje(posiciones)
    return tablero

def AsigJugador1():
    jugador1=raw_input('ingrese nombre para jugador : ')
    return jugador1


def tableroVirgen():
    listaA=['A0','A1','A2','A3','A4','A5','A6','A7','A8','A9']
    listaB=['B0','B1','B2','B3','B4','B5','B6','B7','B8','B9']
    listaC=['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9']
    listaD=['D0','D1','D2','D3','D4','D5','D6','D7','D8','D9']
    listaE=['E0','E1','E2','E3','E4','E5','E6','E7','E8','E9']
    listaF=['F0','F1','F2','F3','F4','F5','F6','F7','F8','F9']
    listaG=['G0','G1','G2','G3','G4','G5','G6','G7','G8','G9']
    listaH=['H0','H1','H2','H3','H4','H5','H6','H7','H8','H9']
    listaI=['I0','I1','I2','I3','I4','I5','I6','I7','I8','I9']
    listaJ=['J0','J1','J2','J3','J4','J5','J6','J7','J8','J9']
    table=[listaA,listaB,listaC,listaD,listaE,listaF,listaG,listaH,listaI,listaJ]
    return table
def verificarDisponibilidad(coordenada,tablero,tableroVirgen):
    contadorFila=0
    for fila in tableroVirgen():
        contadorColumna=0
        for columna in fila:
            if coordenada==columna:
                if tablero[contadorFila][contadorColumna] == ' X' or tablero[contadorFila][contadorColumna] == ' *':
                    return False
            contadorColumna+=1
        contadorFila+=1
    return True 
def verificarFormato(coordenadaEntrante):
    bandera= True
    while bandera:
        coordenada=coordenadaEntrante.upper()
        try:
            comprobacion1= False
            comprobacion2= False 
            contador=0
            letras="ABCDEFGHIJ"
            numeros="0123456789"
            while contador<len(letras):
                contador1=0
                if letras[contador]==coordenada[0]:
                    comprobacion1=True
                while comprobacion1==True:
                    if numeros[contador1]==coordenada[1]:
                        comprobacion2=True
                        if comprobacion1== True and comprobacion2== True and len(coordenada)==2: 
                            return coordenada
                        
                    contador1+=1
                if contador==11:
                    print "por favor ingrese coordenadas correctas"
                    return False 
                contador+=1
                
        except IndexError:
            print "coordenada Erronea. por favor ingresar nuevamente"
            return False 
        except AttributeError:
            print "coordenada Erronea. por favor ingresar nuevamente"
            return False 
        print "coordenada Erronea. por favor ingresar nuevamente"
        return False 
        bandera = False
        
        
def solicitarAtaque(tablero,tableroBarcos,tableroPersonal):
    bandera=True
    while bandera:
        posicion=raw_input("General! Solicitamos coordenadas de Ataque!(ingresa coordenadas de ataque):")
        if posicion=='surrender':
            return posicion
        posicionElevada=posicion.upper()
        posicionVerificada=verificarFormato(posicionElevada)
        if posicionVerificada != False:
            posicionDisponible=verificarDisponibilidad(posicionVerificada,tablero,tableroVirgen)
            if posicionDisponible == True:
                acierto=verificarAciertos(tableroBarcos,posicionVerificada)
                if acierto == True:
                    for fila in tablero:
                        contador = 0
                        for columna in fila:
                            if posicionVerificada== columna:
                                fila[contador]=' *'
                                
                            contador+=1
                else:
                    for fila in tablero:
                        contador = 0
                        for columna in fila:
                            if posicionVerificada== columna:
                                fila[contador]=' X'
                            contador+=1
                mostrarTable=mostrarTablero(tableroPersonal)
                print '--------------------------------------------------------------------'
                mostrarTabler=mostrarTablero(tablero)
                bandera = False 
            else:
                print "ingresar coordenada no utilizada"
        else:
            print '  '
    return posicionVerificada 


#PROCESAMIENTO

listaA=['A0','A1','A2','A3','A4','A5','A6','A7','A8','A9']
listaB=['B0','B1','B2','B3','B4','B5','B6','B7','B8','B9']
listaC=['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9']
listaD=['D0','D1','D2','D3','D4','D5','D6','D7','D8','D9']
listaE=['E0','E1','E2','E3','E4','E5','E6','E7','E8','E9']
listaF=['F0','F1','F2','F3','F4','F5','F6','F7','F8','F9']
listaG=['G0','G1','G2','G3','G4','G5','G6','G7','G8','G9']
listaH=['H0','H1','H2','H3','H4','H5','H6','H7','H8','H9']
listaI=['I0','I1','I2','I3','I4','I5','I6','I7','I8','I9']
listaJ=['J0','J1','J2','J3','J4','J5','J6','J7','J8','J9']
tableroAtaqueJug1=[listaA,listaB,listaC,listaD,listaE,listaF,listaG,listaH,listaI,listaJ]
lista0=['A0','A1','A2','A3','A4','A5','A6','A7','A8','A9']
lista1=['B0','B1','B2','B3','B4','B5','B6','B7','B8','B9']
lista2=['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9']
lista3=['D0','D1','D2','D3','D4','D5','D6','D7','D8','D9']
lista4=['E0','E1','E2','E3','E4','E5','E6','E7','E8','E9']
lista5=['F0','F1','F2','F3','F4','F5','F6','F7','F8','F9']
lista6=['G0','G1','G2','G3','G4','G5','G6','G7','G8','G9']
lista7=['H0','H1','H2','H3','H4','H5','H6','H7','H8','H9']
lista8=['I0','I1','I2','I3','I4','I5','I6','I7','I8','I9']
lista9=['J0','J1','J2','J3','J4','J5','J6','J7','J8','J9']
tableroBarcosJug1=[lista0,lista1,lista2,lista3,lista4,lista5,lista6,lista7,lista8,lista9]
lista00=['A0','A1','A2','A3','A4','A5','A6','A7','A8','A9']
lista10=['B0','B1','B2','B3','B4','B5','B6','B7','B8','B9']
lista20=['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9']
lista30=['D0','D1','D2','D3','D4','D5','D6','D7','D8','D9']
lista40=['E0','E1','E2','E3','E4','E5','E6','E7','E8','E9']
lista50=['F0','F1','F2','F3','F4','F5','F6','F7','F8','F9']
lista60=['G0','G1','G2','G3','G4','G5','G6','G7','G8','G9']
lista70=['H0','H1','H2','H3','H4','H5','H6','H7','H8','H9']
lista80=['I0','I1','I2','I3','I4','I5','I6','I7','I8','I9']
lista90=['J0','J1','J2','J3','J4','J5','J6','J7','J8','J9']
tableroBarcosJug2=[lista00,lista10,lista20,lista30,lista40,lista50,lista60,lista70,lista80,lista90]
#JUGADORES(entradas) 
jugador1=AsigJugador1()
#procesamiento
jugador1F=jugador1
print 'BIENVENIDO A LA GUERRA COMANDANTE',jugador1
#proceso con socket
# Creando el socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Enlace de socket y puerto
server_address = ('localhost',10102)
print >>sys.stderr, 'empezando a levantar %s puerto %s' % server_address
sock.bind(server_address)
# Escuchando conexiones entrantes
sock.listen(1)
banderaJ=True 
while banderaJ:
    # Esperando conexion
    print >>sys.stderr, 'Esperando para conectarse'
    connection, client_address = sock.accept()
    try:
        juego=juegoCompleto(jugador1)
            
    except ValueError:
        print'gracias por preferirnos'
        banderaJ=False
        connection.close()
        
       

