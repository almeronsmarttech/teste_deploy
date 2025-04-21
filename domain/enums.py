from enum import Enum

# Enum do tipo de pilar
class TipoPilarEnum(Enum):
    INTERIOR = "interior"
    BORDA = "borda"
    CANTO = "canto"

class TipoAgregado(Enum):
    BASALTO_DIABASIO = 1.2
    GRANITO_GNAISSE = 1.0
    CALCARIO = 0.9
    ARENITO = 0.7