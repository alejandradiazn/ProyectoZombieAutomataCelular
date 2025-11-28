import random
import math
from celula_sanguinea import CelulaSanguinea
from estado_celular import EstadoCelular

class GrillaTorrenteSanguineo:
    
    #Constantes Fisiológicas.
    _TEMP_NORMAL = 37.0
    _TEMP_MAX_FIEBRE = 42.0
    _UMBRAL_ZOMBIFICACION = 60.0

    def __init__(self, ancho, alto):
        self.__ancho = ancho
        self.__alto = alto
        self.__generacion = 0

        # Grilla bidimensional - inicializada con Plasma por defecto.
        self.__grilla = [[CelulaSanguinea(EstadoCelular.Plasma) for _ in range(ancho)] for _ in range(alto)]

        #Métricas médicas.
        self.__temperaturaCorporal = self._TEMP_NORMAL
        self.__tasaInfeccion = 0.0
        self.__eficienciaInmune = 100.0
        self.__estaZombificado = False
        self.__etapaInfeccion = "Sano"

        #Contadores celulares.
        self.__globulosRojos = 0
        self.__globulosBlancos = 0
        self.__celulasInfectadas = 0
        self.__celulasZombie = 0
        self.__particulasVirus = 0
        self.__celulasInmunesActivas = 0
        
        self.inicializarTorrenteSanguineo()

    def inicializarTorrenteSanguineo(self):
        self.__generacion = 0
        self.__temperaturaCorporal = self._TEMP_NORMAL
        
        for fila in range(self.__alto):
            for col in range(self.__ancho):
                aleatorio = random.random()
                
                # Paredes de vasos sanguíneos (los bordes).
                if fila == 0 or fila == self.__alto - 1 or col == 0 or col == self.__ancho - 1:
                    if random.random() < 0.7:
                        self.__grilla[fila][col] = CelulaSanguinea(EstadoCelular.ParedVaso)
                        continue
                
                #Distribución normal de células sanguíneas.
                if aleatorio < 0.45:
                    # 45% Glóbulos rojos
                    self.__grilla[fila][col] = CelulaSanguinea(EstadoCelular.GlobuloRojo)
                elif aleatorio < 0.456:
                    # 0.6% Neutrófilos
                    self.__grilla[fila][col] = CelulaSanguinea(EstadoCelular.Neutrofilo)
                elif aleatorio < 0.459:
                    # 0.3% Linfocitos
                    self.__grilla[fila][col] = CelulaSanguinea(EstadoCelular.Linfocito)
                elif aleatorio < 0.460:
                    # 0.1% Macrófagos
                    self.__grilla[fila][col] = CelulaSanguinea(EstadoCelular.Macrofago)
                elif aleatorio < 0.470:
                    # 1% Plaquetas
                    self.__grilla[fila][col] = CelulaSanguinea(EstadoCelular.Plaqueta)
                else:
                    # 53% Plasma
                    self.__grilla[fila][col] = CelulaSanguinea(EstadoCelular.Plasma)
        
        self.actualizarEstadisticas()

    def introducirVirus(self, fila, col, radio):
        """
            fila: Fila central de la infección
            col: Columna central de la infección
            radio: Radio del área infectada
        """
        for df in range(-radio, radio + 1):
            for dc in range(-radio, radio + 1):
                f = fila + df
                c = col + dc
                
                if f >= 0 and f < self.__alto and c >= 0 and c < self.__ancho:
                    distancia = math.sqrt(df * df + dc * dc)
                    if distancia <= radio:
                        estado = self.__grilla[f][c].obtenerEstadoActual()
                        
                        #Instrucción de infección células en el área.
                        if estado == EstadoCelular.GlobuloRojo:
                            self.__grilla[f][c].establecerEstado(EstadoCelular.CelulaRojaInfectada)
                        elif estado.esCelulaInmune():
                            self.__grilla[f][c].establecerEstado(EstadoCelular.CelulaBlancaInfectada)
                        elif estado == EstadoCelular.Plasma:
                            self.__grilla[f][c].establecerEstado(EstadoCelular.ParticulaVirus)

    def paso(self):
        #LA ACTUALIZACIÓN DEL TORRENTE SANGUÍNEO ES UN PASO DEL AUTÓMATA.
        #Fase 1: Calcular próximo estado.
        for fila in range(self.__alto):
            for col in range(self.__ancho):
                vecinos = self.obtenerVecinos(fila, col)
                siguienteEstado = self.__grilla[fila][col].calcularSiguienteEstado(vecinos)
                self.__grilla[fila][col].establecerSiguienteEstado(siguienteEstado)
        
        #Fase 2: Aplicar cambios.
        for fila in range(self.__alto):
            for col in range(self.__ancho):
                self.__grilla[fila][col].aplicarSiguienteEstado()
        
        self.__generacion += 1
        self.actualizarEstadisticas()
        self.calcularTemperaturaCorporal()
        self.determinarEtapaInfeccion()

    def obtenerVecinos(self, fila, col):
        """
        Se obtienen los 8 vecinos (principio de vecindario de Moore).
        
        Args:
            fila: Fila de la célula
            col: Columna de la célula
            
        Returns:
            Lista de 8 vecinos (puede contener None para bordes)
        """
        vecinos = [None] * 8
        indice = 0
        
        for df in range(-1, 2):
            for dc in range(-1, 2):
                if df == 0 and dc == 0:
                    continue
                
                f = fila + df
                c = col + dc
                
                if f >= 0 and f < self.__alto and c >= 0 and c < self.__ancho:
                    vecinos[indice] = self.__grilla[f][c]
                else:
                    vecinos[indice] = None
                
                indice += 1
        
        return vecinos

    def actualizarEstadisticas(self):
        self.__globulosRojos = 0
        self.__globulosBlancos = 0
        self.__celulasInfectadas = 0
        self.__celulasZombie = 0
        self.__particulasVirus = 0
        self.__celulasInmunesActivas = 0
        
        totalCelulas = 0
        
        for fila in range(self.__alto):
            for col in range(self.__ancho):
                estado = self.__grilla[fila][col].obtenerEstadoActual()
                
                if estado != EstadoCelular.Plasma and estado != EstadoCelular.ParedVaso:
                    totalCelulas += 1
                
                if estado == EstadoCelular.GlobuloRojo:
                    self.__globulosRojos += 1
                elif estado.esCelulaInmune():
                    self.__globulosBlancos += 1
                    if (estado == EstadoCelular.NeutrofiloActivado or 
                        estado == EstadoCelular.LinfocitoActivado or 
                        estado == EstadoCelular.MacrofagoActivado):
                        self.__celulasInmunesActivas += 1
                elif estado.estaInfectada():
                    self.__celulasInfectadas += 1
                elif estado.esZombie():
                    self.__celulasZombie += 1
                elif estado.esVirus():
                    self.__particulasVirus += 1
        
        #Calcular tasas de infección.
        if totalCelulas > 0:
            self.__tasaInfeccion = ((self.__celulasInfectadas + self.__celulasZombie) / totalCelulas) * 100.0
            if self.__globulosBlancos > 0:
                self.__eficienciaInmune = (self.__celulasInmunesActivas / self.__globulosBlancos) * 100.0
            else:
                self.__eficienciaInmune = 0.0
        
        #Determinar zombificación.
        self.__estaZombificado = self.__tasaInfeccion >= self._UMBRAL_ZOMBIFICACION

    def calcularTemperaturaCorporal(self):

        #Temperatura base.
        temp = self._TEMP_NORMAL
        
        #Aumento por infección activa.
        temp += (self.__tasaInfeccion / 100.0) * 4.0
        
        #Aumento por respuesta inmune (fiebre).
        temp += (self.__celulasInmunesActivas / 100.0) * 1.5
        
        #Caída si zombificación completa (cuerpo "muerto").
        if self.__estaZombificado:
            temp = self._TEMP_NORMAL - 2.0 + (random.random() * 1.0)
        

        self.__temperaturaCorporal = max(35.0, min(self._TEMP_MAX_FIEBRE, temp))

    def determinarEtapaInfeccion(self):
        if self.__estaZombificado:
            self.__etapaInfeccion = "ZOMBIFICADO"
        elif self.__tasaInfeccion > 40:
            self.__etapaInfeccion = "CRÍTICO"
        elif self.__tasaInfeccion > 20:
            self.__etapaInfeccion = "SEVERO"
        elif self.__tasaInfeccion > 5:
            self.__etapaInfeccion = "MODERADO"
        elif self.__celulasInfectadas > 0 or self.__particulasVirus > 0:
            self.__etapaInfeccion = "TEMPRANO"
        else:
            self.__etapaInfeccion = "SALUDABLE"

    
    def obtenerEstadoCelula(self, fila, col):
        if fila >= 0 and fila < self.__alto and col >= 0 and col < self.__ancho:
            return self.__grilla[fila][col].obtenerEstadoActual()
        return EstadoCelular.Plasma

    def obtenerAncho(self):
        return self.__ancho

    def obtenerAlto(self):
        return self.__alto

    def obtenerGeneracion(self):
        return self.__generacion

    def obtenerTemperaturaCorporal(self):
        return self.__temperaturaCorporal

    def obtenerTasaInfeccion(self):
        return self.__tasaInfeccion

    def obtenerEficienciaInmune(self):
        return self.__eficienciaInmune

    def obtenerEstaZombificado(self):
        return self.__estaZombificado

    def obtenerEtapaInfeccion(self):
        return self.__etapaInfeccion

    def obtenerGlobulosRojos(self):
        return self.__globulosRojos

    def obtenerGlobulosBlancos(self):
        return self.__globulosBlancos

    def obtenerCelulasInfectadas(self):
        return self.__celulasInfectadas

    def obtenerCelulasZombie(self):
        return self.__celulasZombie

    def obtenerParticulasVirus(self):
        return self.__particulasVirus

    def obtenerCelulasInmunesActivas(self):
        return self.__celulasInmunesActivas