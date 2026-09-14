import pandas as pd

class vehiculo:
    def __init__(self, matricula, modelo, kilometros, latitud, longitud):
        self.matricula = matricula
        self.modelo = modelo
        self.latitud = latitud
        self.longitud = longitud
        self.__kilometros = kilometros
        

    
    def requiere_mantenimiento(self):
        if self.__kilometros < 0:
            "No puede tener valores negativos"
            pass
        
class furgoneta(vehiculo):
    def requiere_mantenimiento(self):
        if self.__kilometros >= 15000:
            "El vehiculo requiere mantenimiento"
        else:
            "el vehiculo esta operativo"
            return 
    
class VehiculoElectrico(vehiculo):
    def requiere_mantenimiento(self):
        if self.__kilometros >= 5000:
            "El vehiculo requiere mantenimiento"
        else:
            "el vehiculo esta operativo"
            return 

datos = {
    "Matricula":["1552 VX", "1889 BG", "2555 HH"],
    "Modelo":["Mercedes 2", "BMV 4", "Nissan 3"],
    "Vehiculo":["Electrico", "Gasolina", "Electrico"],
    "Latitud":[42.8550, 42.8467, 42.8380],
    "Longitud":[-2.6716, -2.6716,-2.6750 ],
    "Kilometros":[13500, 8000, 3000]
}

df = pd.DataFrame(datos)

def cargar_flota(self):
    return pd.DataFrame(datos)    

def obtener_flota_inicial(vehiculo):
    return[
            VehiculoElectrico( "1552 VX", "Mercedes 2",13500,42.8550,-2.6716),
            furgoneta( "1889 BG","BMV 4",8000,42.8467,-2.6716),
            VehiculoElectrico( "2555 HH","Nissan 3",3000,42.8380,-2.6750)
    ]
