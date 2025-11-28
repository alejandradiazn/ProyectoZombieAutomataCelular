from enum import Enum
from dataclasses import dataclass

@dataclass
class CellState:
    codigo: int
    color: tuple  
    nombre: str

class EstadoCelular(Enum):
    
    # Células sanas - INCLUÍ ESPECIFICACIÓN DE LOS GLÓBULOS BLANCOS
    Plasma = CellState(0, (255, 240, 240), "Plasma")
    GlobuloRojo = CellState(1, (220, 20, 60), "Glóbulo Rojo (Eritrocito)")
    Neutrofilo = CellState(2, (200, 200, 255), "Neutrófilo")
    Linfocito = CellState(3, (100, 149, 237), "Linfocito")
    Macrofago = CellState(4, (70, 130, 180), "Macrófago")
    Plaqueta = CellState(5, (255, 182, 193), "Plaqueta")
    
    # Sistema inmune activado - Células Peleando
    NeutrofiloActivado = CellState(6, (0, 191, 255), "Neutrófilo Activado")
    LinfocitoActivado = CellState(7, (30, 144, 255), "Linfocito Activado")
    MacrofagoActivado = CellState(8, (0, 100, 200), "Macrófago Activado")
    
    # Proceso de infección
    ParticulaVirus = CellState(9, (255, 255, 0), "Partícula Viral")
    CelulaRojaInfectada = CellState(10, (255, 140, 0), "Glóbulo Rojo Infectado")
    CelulaBlancaInfectada = CellState(11, (255, 165, 0), "Glóbulo Blanco Infectado")
    ExplosionViral = CellState(12, (255, 69, 0), "Explosión Viral")
    
    # Transformación zombie
    GlobuloRojoZombie = CellState(13, (139, 0, 0), "Glóbulo Rojo Zombificado")
    GlobuloBlancoZombie = CellState(14, (128, 0, 0), "Glóbulo Blanco Zombificado")
    TejidoNecrotico = CellState(15, (80, 0, 0), "Tejido Necrótico")
    
    # Coagulación y barreras - Hacer que detecte obstáculos, para marcar el flujo celular
    CoaguloSangre = CellState(16, (100, 50, 50), "Coágulo de Sangre")
    ParedVaso = CellState(17, (0, 0, 0), "Pared de Vaso Sanguíneo")
    
    def obtenerCodigo(self):
        return self.value.codigo
    
    def obtenerColor(self):
        return self.value.color
    
    def obtenerNombre(self):
        return self.value.nombre
    
    def esCelulaInmune(self):
        return self in {
            EstadoCelular.Neutrofilo,
            EstadoCelular.Linfocito,
            EstadoCelular.Macrofago,
            EstadoCelular.NeutrofiloActivado,
            EstadoCelular.LinfocitoActivado,
            EstadoCelular.MacrofagoActivado
        }
    
    def estaInfectada(self):
        return self in {
            EstadoCelular.CelulaRojaInfectada,
            EstadoCelular.CelulaBlancaInfectada,
            EstadoCelular.ExplosionViral
        }
    
    def esZombie(self):
        return self in {
            EstadoCelular.GlobuloRojoZombie,
            EstadoCelular.GlobuloBlancoZombie,
            EstadoCelular.TejidoNecrotico
        }
    
    def esVirus(self):
        return self in {
            EstadoCelular.ParticulaVirus,
            EstadoCelular.ExplosionViral
        }
    
    def estaSana(self):
        return self in {
            EstadoCelular.GlobuloRojo,
            EstadoCelular.Neutrofilo,
            EstadoCelular.Linfocito,
            EstadoCelular.Macrofago,
            EstadoCelular.Plaqueta
        }


