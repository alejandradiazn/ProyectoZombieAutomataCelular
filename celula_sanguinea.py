import random
from dataclasses import dataclass
from estado_celular import EstadoCelular

class CelulaSanguinea:
    def __init__(self, estadoInicial:EstadoCelular):
        self.estadoActual = estadoInicial
        self.estadoSiguiente = estadoInicial
        self.edadEstado = 0 #MÁXIMO DE 100 PARA TODOS LOS SIGUIENTES 
        self.cargaViral = 0
        self.nivelAnticuerpos = 20
        self.memoriaInmune = 0
        self.nivelEnergia = 100 #Energía para procesos de la célula (tipo ATP)
    
    def calcularSiguienteEstado(self, vecinos: list) -> EstadoCelular:
        analisis = self.analizarVecindario(vecinos)
        self.actualizarParametrosLocales(analisis)

        #Posibles Estados - Variaciones 
        if self.estadoActual == EstadoCelular.Plasma:
            return self.aplicarReglasPlasma(analisis)
        elif self.estadoActual == EstadoCelular.GlobuloRojo:
            return self.aplicarReglasGlobuloRojo(analisis)
        elif self.estadoActual in (EstadoCelular.Neutrofilo, EstadoCelular.NeutrofiloActivado):
            return self.aplicarReglasNeutrofilo(analisis)
        elif self.estadoActual in (EstadoCelular.Linfocito, EstadoCelular.LinfocitoActivado):
            return self.aplicarReglasLinfocito(analisis)
        elif self.estadoActual in (EstadoCelular.Macrofago, EstadoCelular.MacrofagoActivado):
            return self.aplicarReglasMacrofago(analisis)
        elif self.estadoActual == EstadoCelular.Plaqueta:
            return self.aplicarReglasPlaqueta(analisis)
        elif self.estadoActual == EstadoCelular.ParticulaVirus:
            return self.aplicarReglasParticulaVirus(analisis)
        elif self.estadoActual in (EstadoCelular.CelulaRojaInfectada, EstadoCelular.CelulaBlancaInfectada):
            return self.aplicarReglasCelulaInfectada(analisis)
        elif self.estadoActual == EstadoCelular.ExplosionViral:
            return self.aplicarReglasExplosionViral(analisis)
        elif self.estadoActual in (EstadoCelular.GlobuloRojoZombie, EstadoCelular.GlobuloBlancoZombie):
            return self.aplicarReglasZombie(analisis)
        elif self.estadoActual == EstadoCelular.TejidoNecrotico:
            return self.aplicarReglasNecrotico(analisis)
        elif self.estadoActual == EstadoCelular.CoaguloSangre:
            return self.aplicarReglasCoagulo(analisis)
        elif self.estadoActual == EstadoCelular.ParedVaso:
            return EstadoCelular.ParedVaso
        else:
            return self.estadoActual
    
    def analizarVecindario(self, vecinos:list):
        analisis = self.analisisVecindario()

        for vecino in vecinos:
            if vecino is None:
                continue

            estado = vecino.obtenerEstadoActual()
            
            if estado.esVirus():
                analisis.cantidadVirus += 1
            if estado.estaInfectada():
                analisis.cantidadInfectadas += 1
            if estado.esZombie():
                analisis.cantidadZombies += 1
            if estado.esCelulaInmune():
                analisis.cantidadInmunes += 1
                analisis.totalAnticuerpos += vecino.nivelAnticuerpos
            if estado == EstadoCelular.GlobuloRojo:
                analisis.cantidadGlobulosRojos += 1
            if estado == EstadoCelular.Plaqueta:
                analisis.cantidadPlaquetas += 1
            if estado == EstadoCelular.CoaguloSangre:
                analisis.cantidadCoagulos += 1
            if estado == EstadoCelular.Plasma:
                analisis.cantidadPlasma += 1
            
            # Acumular carga viral del vecindario
            analisis.cargaViralVecindario += vecino.cargaViral
        
        return analisis
    
    def actualizarParametrosLocales(self, analisis: 'analisisVecindario'):
        
        #Incremento y actualización de la carga viral
        self.cargaViral += (analisis.cantidadVirus * 12 + analisis.cantidadInfectadas * 6 + analisis.cantidadZombies *10)
        self.cargaViral -= ((analisis.cantidadInmunes *  18 + analisis.totalAnticuerpos) // 10 )
        self.cargaViral = max(0, min(100, self.cargaViral))
        
        #Actualizacion del nivel de anticuerpos 
        if analisis.cantidadInmunes > 0:
            self.nivelAnticuerpos = self.nivelAnticuerpos + (analisis.totalAnticuerpos / 20)
            self.nivelAnticuerpos = min(100, self.nivelAnticuerpos)
        
        #Energía que se gasta con la edad y la infección
        self.nivelEnergia -= (self.cargaViral / 50)
        self.nivelEnergia = max(0, self.nivelEnergia)

    def aplicarReglasPlasma(self, a : 'analisisVecindario') -> EstadoCelular:

        #Regla: El plasma puede contaminarse con el virus.
        if a.cantidadVirus >= 2 or self.cargaViral > 30:
            return EstadoCelular.ParticulaVirus
        
        #Regla: Coagulación defensiva ante infección masiva.
        if a.cantidadPlaquetas >= 4 and (a.cantidadInfectadas + a.cantidadZombies) > 2:
            return EstadoCelular.CoaguloSangre
        
        return EstadoCelular.Plasma
    
    def aplicarReglasGlobuloRojo(self, a: 'analisisVecindario') -> EstadoCelular:

        #Parámetro : Umbral de infección basado en la exposición a la carga viral.
        riesgoInfeccion =  (a.cantidadVirus * 0.25) + (a.cantidadInfectadas * 0.15) + (self.cargaViral / 200.0)

        #Regla: Si se genera un número random menor al riesgo de infección, el globulo rojo se cambia de estado a infectada.
        if random.random() < riesgoInfeccion:
            return EstadoCelular.CelulaRojaInfectada
        
        #Regla: Zombificación directa su se encuentra rodeada completamente de células Zombies
        if a.cantidadZombies >= 6:
            return EstadoCelular.GlobuloRojoZombie

        #Regla: Protección por anticuerpos del vecindario.
        if self.nivelAnticuerpos > 60 and a.cantidadInmunes >= 3:
            self.cargaViral = max(0, self.cargaViral - 20)

        return EstadoCelular.GlobuloRojo 
    
    def aplicarReglasNeutrofilo(self, a:'analisisVecindario') -> EstadoCelular:
        estaActivado = ( self.estadoActual == EstadoCelular.NeutrofiloActivado)

        #Regla: Actúan como respuesta rápida ante la amenaza del virus y células infectadas.
        if not estaActivado and (a.cantidadVirus + a.cantidadInfectadas >= 2):
            self.nivelEnergia = 100
            return EstadoCelular.NeutrofiloActivado
        
        if estaActivado:
            #Regla:  Defensa mediante proceso de fagocitosis - Destruye virus con probabilidad.
            if a.cantidadVirus > 0 and self.nivelEnergia > 30:
                probabilidadFagocitosis = 0.65 - (self.cargaViral/200.0)
                if random.random() < probabilidadFagocitosis:
                    self.cargaViral = 0
                    self.nivelEnergia -= 40
                    #Muerte de la celula después de la fagocitosis
                    if self.nivelEnergia < 20 or random.random() < 0.3:
                        return EstadoCelular.Plasma
            
            #Regla: Resistencia moderada a la infección.
            if a.cantidadZombies >= 4 or self.cargaViral > 75:
                probabilidadInfeccion = 0.35 + (self.cargaViral/150.0)
                if random.random() < probabilidadInfeccion:
                    return EstadoCelular.CelulaBlancaInfectada
            
            #Regla: Se desactiva como sistema de defensa si ya no hay amenaza.
            if a.cantidadVirus == 0 and a.cantidadInfectadas == 0 and self.edadEstado > 5:
                return EstadoCelular.Neutrofilo
        
        if not estaActivado and a.cantidadVirus >= 3 and self.cargaViral > 50:
            if random.random() < 0.25:
                return EstadoCelular.CelulaBlancaInfectada
        
        return self.estadoActual

    def aplicarReglasLinfocito(self, a: 'analisisVecindario') -> EstadoCelular:
        estaActivado = (self.estadoActual == EstadoCelular.LinfocitoActivado)

        # Regla: Activación más rápida con memoria alta (inmunidad entrenada)
        umbralActivacion = 2
        if self.memoriaInmune > 60:
            umbralActivacion = 1  # Se activa más rápido si "recuerda" el patógeno.
    
        # Regla: Respuesta más lenta del sistema pero duradera - Activación.
        if not estaActivado and (a.cantidadInfectadas + a.cantidadZombies >= umbralActivacion or self.cargaViral > 40):
            self.nivelAnticuerpos += 25
            self.memoriaInmune += 15
            return EstadoCelular.LinfocitoActivado
    
        if estaActivado:
            # Producción de anticuerpos, se da una inmunidad adaptativa.
            #Regla: Producción acelerada con alta memoria.
            incrementoAnticuerpos = 5
            if self.memoriaInmune > 70:
                incrementoAnticuerpos = 8  
        
            self.nivelAnticuerpos = min(100, self.nivelAnticuerpos + incrementoAnticuerpos)
            self.memoriaInmune = min(100, self.memoriaInmune + 3)

            # Regla: Curación de células infectadas mediante anticuerpos
            if a.cantidadInfectadas > 0 and self.nivelAnticuerpos > 70:
                #Proceso: Curación más efectiva con memoria alta.
                bonusMemoria = self.memoriaInmune / 200.0  # OJO: 0 a 0.5 de bonus.
                probabilidadCuracion = (0.35 + bonusMemoria) * (self.nivelAnticuerpos / 100.0)
            
                #Regla: Reduce más carga viral si tiene memoria
                if random.random() < probabilidadCuracion:
                    reduccionViral = 30 + (self.memoriaInmune // 5)  # 30-50 según memoria
                    self.cargaViral = max(0, self.cargaViral - reduccionViral)
    
            # Regla: Alta resistencia pero sin inmunidad. - Más resistente con memoria alta
            resistenciaBase = 0.2
            if self.memoriaInmune > 50:
                resistenciaBase = 0.1  # Menos probabilidad de infectarse
        
            if a.cantidadZombies >= 5 and self.cargaViral > 85:
                if random.random() < resistenciaBase:
                    return EstadoCelular.CelulaBlancaInfectada
        
            # Regla: Si la amenaza disminuye, se desactivan progresivamente. - Con memoria alta, permanece activado más tiempo (vigilancia)
            tiempoDesactivacion = 8
            if self.memoriaInmune > 80:
                tiempoDesactivacion = 15 
        
            if a.cantidadVirus == 0 and a.cantidadInfectadas == 0 and a.cantidadZombies == 0:
                if self.edadEstado > tiempoDesactivacion:
                    return EstadoCelular.Linfocito
    
        # Regla: Linfocitos inactivos son más resistentes que los neutrófilos (Durabilidad)- Memoria residual protege incluso inactivos
        resistenciaInactivo = 0.15
        if self.memoriaInmune > 40:
            resistenciaInactivo = 0.08  # Mucho más resistente con memoria
    
        if not estaActivado and a.cantidadVirus >= 4 and self.cargaViral > 65:
            if random.random() < resistenciaInactivo:
                return EstadoCelular.CelulaBlancaInfectada
            
        return self.estadoActual
    
    def aplicarReglasMacrofago(self, a:'analisisVecindario') -> EstadoCelular:

        estaActivado = ( self.estadoActual == EstadoCelular.MacrofagoActivado)

        #Regla: Alto requerimiento de virus y celulas infectadas para su activación - Un macrófago es grande, se mueve lento, reacciona más tarde.
        if not estaActivado and (a.cantidadVirus + a.cantidadInfectadas >=  3):
            self.nivelEnergia = 100
            return EstadoCelular.MacrofagoActivado
        
        if estaActivado:

            #Regla: Se hace fagocitosis de las células infectadas y  virus.
            if a.cantidadInfectadas > 0 and self.nivelEnergia > 40:
                probabilidadFagocitosis = 0.55
                if random.random() < probabilidadFagocitosis:
                    self.cargaViral = max(0, self.cargaViral - 25)
                    self.nivelEnergia -= 30

                    #Regla: Muerte del macrofago después de ejecutar ese proceso muchas veces.
                    if self.nivelEnergia < 25 or self.edadEstado > 15:
                        return EstadoCelular.Plasma
            
            #Regla: Entrenamiento de la memoria inmune.
            if a.cantidadInmunes > 0 and self.edadEstado % 3 == 0:
                self.memoriaInmune += 10

            #Regla: Alta resistencia.
            if a.cantidadZombies >= 6 and self.cargaViral > 90:
                probabilidadInfeccion = 0.15 + (self.cargaViral/300.0)
                if random.random() < probabilidadInfeccion:
                    return EstadoCelular.CelulaBlancaInfectada
                
            #Regla: Desactivación Lenta de los macrófagos.
            if (a.cantidadVirus + a.cantidadInfectadas == 0) and self.edadEstado > 10:
                return EstadoCelular.Macrofago
        
        return self.estadoActual
    
    def aplicarReglasPlaqueta(self, a : 'analisisVecindario') -> EstadoCelular:

        #Regla: Las plaquetas forman coágulos para contener la infección.
        if a.cantidadPlaquetas >= 3 and (a.cantidadInfectadas + a.cantidadZombies) > 1:
            probabilidadCoagulo = 0.3 + (a.cantidadZombies * 0.1)
            if random.random() < probabilidadCoagulo:
                return EstadoCelular.CoaguloSangre
            
        #Regla: Conversión a partículas de virus.
        if a.cantidadVirus >= 2 and self.cargaViral > 40:
            return EstadoCelular.ParticulaVirus
        
        return EstadoCelular.Plaqueta
    
    def aplicarReglasParticulaVirus(self, a: 'analisisVecindario') -> EstadoCelular:

        #Regla: Preferencia a la infección de glóbulos rojos.
        if a.cantidadGlobulosRojos > 0  and random.random() < 0.75:
            return EstadoCelular.CelulaRojaInfectada
        
        #Regla: Infecta células del sistema inmune si hay pocas rojas.
        if a.cantidadGlobulosRojos == 0 and a.cantidadInmunes > 0 and random.random() < 0.4:
            return EstadoCelular.CelulaBlancaInfectada
        
        #Regla: Elimina células del sistema inmune.
        if a.cantidadInmunes >= 2 or self.nivelAnticuerpos > 60:
            probabilidadElimminacion = 0.6 + (self.nivelAnticuerpos / 200)
            if random.random() < probabilidadElimminacion:
                return EstadoCelular.Plasma
            
        #Regla: Generación de explosión viral.
        if self.edadEstado > 4 and a.cantidadVirus < 3:
            if random.random() < 0.25:
                return EstadoCelular.ExplosionViral
            
        return EstadoCelular.ParticulaVirus
    
    def aplicarReglasCelulaInfectada(self, a:'analisisVecindario') -> EstadoCelular:

        esRojaInfectada = (self.estadoActual == EstadoCelular.CelulaRojaInfectada)
        
        #Regla: Según el tipo, se da el periodo de infección.
        periodoIncubacion = 3 if esRojaInfectada else 4

        #Regla: Generación de una replicación viral completa.
        if self.edadEstado >= periodoIncubacion:
            return EstadoCelular.ExplosionViral
        
        #Regla: Rescate del sujeto por parte ddel sistena inmune.
        probabilidadRescate = 0.25 -(self.edadEstado * 0.05)

        if esRojaInfectada:
            if a.cantidadInmunes >= 3 and self.nivelAnticuerpos > 70 and random.random() < probabilidadRescate:
                return EstadoCelular.GlobuloRojo
        else:
            if a.cantidadInmunes >=4 and self.nivelAnticuerpos > 80 and random.random() < probabilidadRescate:
                return EstadoCelular.Neutrofilo
            
        return self.estadoActual
    
    def aplicarReglasExplosionViral(self, a: 'analisisVecindario') -> EstadoCelular:
        

        if self.edadEstado >= 2:
            # Regla: Determinar qué tipo de zombie basado en célula original.
            if random.random() < 0.7:
                return EstadoCelular.GlobuloRojoZombie
            else:
                return EstadoCelular.GlobuloBlancoZombie
        
        return EstadoCelular.ExplosionViral
    
    def aplicarReglasZombie(self, a: 'analisisVecindario') -> EstadoCelular:
        #Regla: Eliminación masiva debido al sistema inmune.
        if a.cantidadInmunes >= 5 and self.nivelAnticuerpos > 80:
            if self.edadEstado > 20 and random.random() < 0.15:
                return EstadoCelular.TejidoNecrotico
        
        #Regla: Estado de necrosis natural.
        if self.edadEstado > 50:
            if random.random() < 0.05:
                return EstadoCelular.TejidoNecrotico
        
        return self.estadoActual
    
    def aplicarReglasNecrotico(self, a: 'analisisVecindario') -> EstadoCelular:

        if self.edadEstado > 80:
            if random.random() < 0.1:
                return EstadoCelular.Plasma
        
        return EstadoCelular.TejidoNecrotico
    
    def aplicarReglasCoagulo(self, a: 'analisisVecindario') -> EstadoCelular:
        #Regla: Se disuelven si no hay amenaza.
        if (self.edadEstado > 25 and a.cantidadZombies == 0 and 
            a.cantidadInfectadas == 0):
            if random.random() < 0.2:
                return EstadoCelular.Plasma
        
        #Regla: Se mantienen mientras haya infección cercana.
        return EstadoCelular.CoaguloSangre
    
    def establecerSiguienteEstado(self, estado: EstadoCelular):
        self.estadoSiguiente = estado
    
    def aplicarSiguienteEstado(self):
        if self.estadoActual != self.estadoSiguiente:
            self.estadoActual = self.estadoSiguiente
            self.edadEstado = 0
        else:
            self.edadEstado += 1
        
        #Regla: Decaimiento natural de parámetros.
        self.cargaViral = max(0, self.cargaViral - 2)
        self.nivelAnticuerpos = max(0, self.nivelAnticuerpos - 1)
        self.memoriaInmune = max(0, self.memoriaInmune - 1)
        self.nivelEnergia = min(100, self.nivelEnergia + 1)
    
    def obtenerEstadoActual(self) -> EstadoCelular:
        return self.estadoActual
    
    def establecerEstado(self, estado: EstadoCelular):
        self.estadoActual = estado
        self.estadoSiguiente = estado
        self.edadEstado = 0
    
    # Getters para parámetros internos
    def obtenerCargaViral(self) -> int:
        return self.cargaViral
    
    def obtenerNivelAnticuerpos(self) -> int:
        return self.nivelAnticuerpos
    
    def obtenerMemoriaInmune(self) -> int:
        return self.memoriaInmune
    
    def obtenerNivelEnergia(self) -> int:
        return self.nivelEnergia
    
    
    @dataclass
    class analisisVecindario:
        cantidadVirus: int = 0
        cantidadInfectadas: int = 0
        cantidadZombies: int = 0
        cantidadInmunes: int = 0
        cantidadGlobulosRojos: int = 0
        cantidadPlaquetas: int = 0
        cantidadCoagulos: int = 0
        cantidadPlasma: int = 0
        cargaViralVecindario: int = 0
        totalAnticuerpos: int = 0






        


