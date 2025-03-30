import random
from collections import defaultdict

class GeneradorCongruencial:
    def __init__(self, semilla=1234, a=1664525, c=1013904223, m=2**32):
        self.xn = semilla
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        self.xn = (self.a * self.xn + self.c) % self.m
        return self.xn / self.m  # Normalizamos a [0,1]
    
generador = GeneradorCongruencial()    
class Arquero:
    def __init__(self, nombre, genero):
        self.nombre = nombre
        self.genero = genero
        self.resetear_estado()
    
    def resetear_estado(self):
        """Reinicia el estado del arquero para un nuevo juego"""
        self.resistencia = random.randint(25, 45)
        self.experiencia = 10
        self.suerte = random.uniform(1, 3)  # Se recalculará cada ronda
        self.puntaje_total = 0
        self.rondas_ganadas = 0
        self.rondas_ganadas_consecutivas = 0
        self.bonus_resistencia = 0
    
    def recalcular_suerte(self):
        """Recalcula la suerte al inicio de cada ronda"""
        self.suerte = random.uniform(1, 3)
    
    def lanzar(self):
        if self.resistencia < 5 and self.rondas_ganadas_consecutivas < 3:
            return 0

        if self.rondas_ganadas_consecutivas < 3:
            costo_resistencia = 1 if self.bonus_resistencia > 0 else 5
            self.resistencia -= costo_resistencia
        
        probabilidad = generador.next() * 100
        
        if self.genero == 'M':
            if probabilidad < 20:
                return 10
            elif probabilidad < 53:
                return 9
            elif probabilidad < 93:
                return 8
            else:
                return 0
        else:
            if probabilidad < 30:
                return 10
            elif probabilidad < 68:
                return 9
            elif probabilidad < 95:
                return 8
            else:
                return 0
            
    def lanzamiento_desempate(self):
        probabilidad = generador.next() * 100  # Usa el generador congruencial
        
        if self.genero == 'M':
            if probabilidad < 20:    # 20% para 10 (hombres)
                return 10
            elif probabilidad < 53:  # 33% para 9 (53-20)
                return 9
            elif probabilidad < 93:  # 40% para 8 (93-53)
                return 8
            else:                    # 7% para 0 (100-93)
                return 0
        else:  # Género 'F'
            if probabilidad < 30:    # 30% para 10 (mujeres)
                return 10
            elif probabilidad < 68:  # 38% para 9 (68-30)
                return 9
            elif probabilidad < 95:  # 27% para 8 (95-68)
                return 8
            else:                    # 5% para 0 (100-95)
                return 0            

def jugar_ronda(equipo1, equipo2):
      
    # Recalcular suerte para todos los arqueros al inicio de cada ronda
    for arquero in equipo1 + equipo2:
        arquero.recalcular_suerte()
    
    puntajes = {"Equipo 1": 0, "Equipo 2": 0}
    
    # Identificar al arquero con más suerte en cada equipo (con suerte recién calculada)
    arquero_suerte_equipo1 = max(equipo1, key=lambda x: x.suerte)
    arquero_suerte_equipo2 = max(equipo2, key=lambda x: x.suerte)
    
    # Lanzamiento de suerte
    lanzamiento_suerte_equipo1 = arquero_suerte_equipo1.lanzar()
    lanzamiento_suerte_equipo2 = arquero_suerte_equipo2.lanzar()
    
    puntajes["Equipo 1"] += lanzamiento_suerte_equipo1
    puntajes["Equipo 2"] += lanzamiento_suerte_equipo2
    
    for arquero1, arquero2 in zip(equipo1, equipo2):
        puntos_arquero1 = 0
        puntos_arquero2 = 0
        
        # Lanzamientos normales
        while arquero1.resistencia >= 5:
            puntos_arquero1 += arquero1.lanzar()
        
        while arquero2.resistencia >= 5:
            puntos_arquero2 += arquero2.lanzar()
        
        # Determinar ganador de la ronda individual
        if puntos_arquero1 > puntos_arquero2:
            arquero1.rondas_ganadas += 1
            arquero1.rondas_ganadas_consecutivas += 1
            arquero2.rondas_ganadas_consecutivas = 0
            arquero1.experiencia += 3
        elif puntos_arquero2 > puntos_arquero1:
            arquero2.rondas_ganadas += 1
            arquero2.rondas_ganadas_consecutivas += 1
            arquero1.rondas_ganadas_consecutivas = 0
            arquero2.experiencia += 3
        else:
            # Desempate
            while True:
                desempate1 = arquero1.lanzamiento_desempate()  # Usa probabilidades por género
                desempate2 = arquero2.lanzamiento_desempate()
    
                if desempate1 > desempate2:
                    arquero1.rondas_ganadas += 1
                    arquero1.rondas_ganadas_consecutivas += 1
                    arquero2.rondas_ganadas_consecutivas = 0
                    arquero1.experiencia += 3
                    break
                elif desempate2 > desempate1:
                    arquero2.rondas_ganadas += 1
                    arquero2.rondas_ganadas_consecutivas += 1
                    arquero1.rondas_ganadas_consecutivas = 0
                    arquero2.experiencia += 3
                    break
        
        # Verificar lanzamiento extra por 3 victorias consecutivas
        for arquero, equipo in [(arquero1, "Equipo 1"), (arquero2, "Equipo 2")]:
            if arquero.rondas_ganadas_consecutivas >= 3:
                lanzamiento_extra = arquero.lanzar()
                puntajes[equipo] += lanzamiento_extra
                arquero.rondas_ganadas_consecutivas = 0
        
        # Aplicar beneficio por experiencia
        for arquero in [arquero1, arquero2]:
            if arquero.experiencia >= 19 and arquero.bonus_resistencia == 0:
                arquero.bonus_resistencia = 2

                if arquero.bonus_resistencia>0:
                    arquero.bonus_resistencia -=1
        
        # Sumar puntos al equipo
        puntajes["Equipo 1"] += puntos_arquero1
        puntajes["Equipo 2"] += puntos_arquero2

        # Actualizar puntaje total del arquero
        arquero1.puntaje_total += puntos_arquero1
        arquero2.puntaje_total += puntos_arquero2

    # Ajustar resistencia para la siguiente ronda
    for arquero in equipo1 + equipo2:
        arquero.resistencia = max(5, arquero.resistencia + random.randint(-2, -1))
        if arquero.bonus_resistencia > 0:
            arquero.bonus_resistencia -= 1

    return puntajes

def jugar_juego_completo():
    # Crear equipos (los mismos para todos los juegos)
    equipo1 = [Arquero(f"Arquero {i+1} del equipo 1", random.choice(['M', 'F'])) for i in range(5)]
    equipo2 = [Arquero(f"Arquero {i+6} del equipo 2", random.choice(['M', 'F'])) for i in range(5)]
    
    puntaje_global = {"Equipo 1": 0, "Equipo 2": 0}
    victorias = {"Equipo 1": 0, "Equipo 2": 0, "Empates": 0}

    mejores_arqueros = defaultdict(int)
    jugadores_mas_suerte = defaultdict(int)

    lista_suerte_por_juego = []
    lista_experiencia_por_juego = []


    for juego in range(20000):
        # Reiniciar estado para nuevo juego
        for arquero in equipo1 + equipo2:
            arquero.resetear_estado()
        
        puntaje_juego = {"Equipo 1": 0, "Equipo 2": 0}


        for ronda in range(10):
            puntajes_ronda = jugar_ronda(equipo1, equipo2)
            puntaje_juego["Equipo 1"] += puntajes_ronda["Equipo 1"]
            puntaje_juego["Equipo 2"] += puntajes_ronda["Equipo 2"]


        # Actualizar estadísticas globales
        puntaje_global["Equipo 1"] += puntaje_juego["Equipo 1"]
        puntaje_global["Equipo 2"] += puntaje_juego["Equipo 2"]
        
        if puntaje_juego["Equipo 1"] > puntaje_juego["Equipo 2"]:
            victorias["Equipo 1"] += 1
        elif puntaje_juego["Equipo 2"] > puntaje_juego["Equipo 1"]:
            victorias["Equipo 2"] += 1
        else:
            victorias["Empates"] += 1
        
        # Registrar mejor arquero de este juego
        mejor_arquero_juego = max(equipo1 + equipo2, key=lambda x: x.rondas_ganadas)
        mejores_arqueros[mejor_arquero_juego.nombre] += 1

        arquero_mas_suerte = max(equipo1 + equipo2, key=lambda x: x.suerte)
        jugadores_mas_suerte[arquero_mas_suerte.nombre] += 1

        lista_suerte_por_juego.append(arquero_mas_suerte.nombre)

        arquero_mas_experiencia = max(equipo1 + equipo2, key=lambda x: x.experiencia)
        lista_experiencia_por_juego.append(arquero_mas_experiencia.nombre)


    total_m = sum(1 for arquero in equipo1 + equipo2 if arquero.genero == 'M')
    total_f = sum(1 for arquero in equipo1 + equipo2 if arquero.genero == 'F')
    print(f"Total arqueros masculinos: {total_m}, Total arqueros femeninos: {total_f}")    

    print("\nLista de jugadores con más suerte en cada juego:")
    for i, nombre in enumerate(lista_suerte_por_juego[:20], start=1):  # Mostramos solo los primeros 100
        print(f"Juego {i}: {nombre}")    

    print("\nLista de jugadores con más experiencia en cada juego:")
    for i, nombre in enumerate(lista_experiencia_por_juego[:20], start=1):  # Mostramos solo los primeros 100
        print(f"Juego {i}: {nombre}")

    print("\n" + "="*50)
    print("RESULTADOS FINALES DESPUÉS DE 20,000 JUEGOS")
    print("="*50)
    print(f"\n Victorias totales:")
    print(f"  Equipo 1: {victorias['Equipo 1']} juegos ganados")
    print(f"  Equipo 2: {victorias['Equipo 2']} juegos ganados")
    print(f"  Empates: {victorias['Empates']} juegos")
    
    print(f"\n Puntaje global acumulado:")
    print(f"  Equipo 1: {puntaje_global['Equipo 1']} puntos")
    print(f"  Equipo 2: {puntaje_global['Equipo 2']} puntos")
    
    print("\n Mejores arqueros (veces que fue el mejor en un juego):")
    for arquero, veces in sorted(mejores_arqueros.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {arquero}: {veces} veces")



if __name__ == "__main__":
    jugar_juego_completo()