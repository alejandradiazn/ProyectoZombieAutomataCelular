# 🧬 Simulador de Infección Zombie en Torrente Sanguíneo

## Descripción General.

Este proyecto es un autómata celualr que pretende simular la propagación de una infección zombie a nivel sanguíneo. El sistema modela el comportamiento del torrente sanguíneo humano durante una infección viral agresiva, visualizando la lucha entre el sistema inmune y un patógeno zombificante.

En su elaboración, la simulación utiliza una grilla donde cada célula representa un componente sanguíneo que evoluciona según reglas probabilísticas inspiradas en procesos biológicos reales.

---

## Objetivos del Proyecto.

- Observar propagación viral en el sistema sanguíneo.
- Generar una aproximación de la respuesta del sistema inmunitario y sus mecanismos de defensa.
- Visualizar la zombificación progresiva del organismo.

---

## Tipos de Células.

### Células Sanas
- **Plasma** (53%): Estado neutro, base del sistema
- **Glóbulos Rojos** (45%): Transportan oxígeno, objetivo principal del virus
- **Neutrófilos** (0.6%): Respuesta rápida ante infecciones
- **Linfocitos** (0.3%): Respuesta adaptativa, producen anticuerpos y memoria inmune
- **Macrófagos** (0.1%): Respuesta lenta pero poderosa, fagocitan células completas
- **Plaquetas** (1%): Forman barreras defensivas mediante coagulación

### Estados de Infección
- **Partícula Viral**: Virus libre buscando infectar células
- **Célula Infectada**: Célula en periodo de incubación (replicación viral)
- **Explosión Viral**: Liberación masiva de virus
- **Célula Zombie**: Célula senescente que no funciona ni muere
- **Tejido Necrótico**: Restos de células zombie destruidas

---

## Reglas y Parámetros del Autómata.

### 🔴 **GLÓBULOS ROJOS**

#### Cálculo del Riesgo de Infección
El riesgo de infección se calcula sumando tres factores:
- La cantidad de virus cercanos multiplicada por 0.25
- La cantidad de células infectadas cercanas multiplicada por 0.15
- La carga viral de la célula dividida entre 200.

#### Reglas Probabilísticas.
1. **Infección por exposición**: Se genera un número aleatorio entre 0 y 1. Si este número es menor que el riesgo calculado, el glóbulo rojo se infecta.

2. **Zombificación directa**: Si el glóbulo rojo está rodeado por 6 o más células zombie, se convierte inmediatamente en glóbulo rojo zombie sin pasar por el periodo de infección.

3. **Protección por anticuerpos**: Si el nivel de anticuerpos es mayor a 60 y hay al menos 3 células inmunes cercanas, la célula reduce su carga viral en 20 puntos, proporcionando resistencia a la infección.

---

### ⚪ **NEUTRÓFILOS** (Representación de Respuesta Rápida)

#### Activación
Los neutrófilos se activan cuando detectan 2 o más virus o células infectadas en su vecindario y, al activarse, su nivel de energía se restaura a 100.

#### Fagocitosis (Se ejecuta con los Neutrófilos Activados).
La probabilidad de fagocitosis exitosa es de 65% pero, disminuye si la célula tiene alta carga viral; es así que por cada 200 puntos de carga viral, la probabilidad baja proporcionalmente.

*Proceso de fagocitosis:*
1. Si hay virus cercanos y el neutrófilo tiene más de 30 puntos de energía:
   - Se genera un número aleatorio para determinar si la fagocitosis tiene éxito.
   - Si tiene éxito: elimina completamente el virus (carga viral a 0) y gasta 40 puntos de energía.
   - **Muerte celular por agotamiento**: Si la energía cae por debajo de 20 o si aleatoriamente (30% de probabilidad) ocurre, el neutrófilo muere y se convierte en plasma.

#### Resistencia a Infección
Los neutrófilos tienen resistencia moderada y su probabilidad de infección base es del 35%, aumentando según la carga viral (cada 150 puntos de carga viral suma proporcionalmente a la probabilidad).

- Si hay 4 o más zombies cercanos o la carga viral supera 75, se evalúa si el neutrófilo se infecta usando esta probabilidad.

#### Desactivación
Si no hay amenazas (cero virus y cero células infectadas) y el neutrófilo ha estado activo por más de 5 turnos, vuelve a su estado inactivo para conservar energía.

---

### 🔵 **LINFOCITOS** (Representación de Respuesta Adaptativa)

#### Sistema de Memoria Inmune
Los linfocitos cuentan con un sistema de memoria inmune que les permite reaccionar más rápido ante amenazas conocidas:
- **Umbral normal**: Se activan cuando hay 2 o más células infectadas o zombie cercanas.
- **Con memoria alta** (estableccida como mayor a 60): Se activan con solo 1 célula que represente amenaza, reaccionando mucho más rápido.

#### Producción de Anticuerpos (Linfocitos Activados)
Cuando están activos, los linfocitos producen anticuerpos constantemente:
- **Producción normal**: Aumentan 5 puntos de anticuerpos por turno  (Generación de cada celda en la ejecución).
- **Producción acelerada**: Si la memoria inmune supera 70, producen 8 puntos por turno.
- Así mismo, cada turno la memoria inmune aumenta en 3 puntos (máximo 100).

#### Curación de Células Infectadas
Los linfocitos pueden rescatar células infectadas mediante anticuerpos:

*Cálculo del bonus de memoria*: La memoria inmune se divide entre 200, dando un bonus de 0 a 0.5.
*Probabilidad de curación*: Se calcula como (0.35 más el bonus de memoria) multiplicado por el porcentaje de anticuerpos actuales.
*Reducción viral*: Si la curación tiene éxito, reduce la carga viral entre 30 y 50 puntos, dependiendo de la memoria (suma 30 más la memoria dividida entre 5).
*Condiciones*: Debe haber células infectadas cercanas, el nivel de anticuerpos debe superar 70, y se genera un número aleatorio que se compara con la probabilidad calculada.

#### Resistencia Superior
Los linfocitos son más resistentes que los neutrófilos:
- *Resistencia normal*: 20% de probabilidad de infección en condiciones extremas.
- *Con memoria alta* (establecida como mayor a 50): Solo 10% de probabilidad de infección.
- Solo se evalúa infección si hay 5 o más zombies y la carga viral supera 85.

#### Desactivación Inteligente con Vigilancia
Los linfocitos permanecen activos más tiempo cuando tienen memoria:
- *Desactivación normal*: Después de 8 turnos sin amenazas.
- *Con memoria alta* (mayor a 80): Permanecen vigilantes hasta 15 turnos.
- Solo se desactivan si no hay virus, infectadas ni zombies en el área.

---

### 🔵⚫ **MACRÓFAGOS** (Los Gigantes- Referencia a Tanques)

#### Activación Tardía
Los macrófagos requieren un umbral más alto para activarse, necesitan detectar 3 o más virus o células infectadas en su vecindario; esta respuesta más lenta refleja su naturaleza de células grandes y lentas que reaccionan después que los neutrófilos.

#### Fagocitosis de Células Completas
A diferencia de los neutrófilos, los macrófagos pueden devorar células infectadas enteras con una probabilidad fija del 55%.

#### Entrenamiento de Memoria Inmune
Los macrófagos tienen un rol educativo en el sistema inmune. Cada 3 turnos, si hay células inmunes cercanas, aumentan la memoria inmune del área en 10 puntos. Esto representa cómo los macrófagos "enseñan" y presentan antígenos a otras células inmunes.

#### Alta Resistencia
Los macrófagos son las células más resistentes del sistema. Su probabilidad base de infección es solo del 15%, aumentando ligeramente con la carga viral (cada 300 puntos de carga viral suman proporcionalmente).

Solo se evalúa infección en condiciones extremas: cuando hay 6 o más zombies cercanos y la carga viral supera 90.

#### Desactivación Lenta
Los macrófagos permanecen activos más tiempo que otras células. Solo se desactivan después de 10 turnos sin amenazas (cero virus y cero células infectadas).

---

### **PLAQUETAS** (Defensa por Barreras)

#### Formación de Coágulos
Las plaquetas forman barreras físicas mediante coagulación. La probabilidad de formar un coágulo es del 30% base, aumentando un 10% por cada célula zombie cercana.

*Condiciones para coagulación:*
- Debe haber al menos 3 plaquetas en el área
- Debe haber más de 1 célula infectada o zombie cerca
- Se genera un número aleatorio que se compara con la probabilidad calculada
- Si tiene éxito, la plaqueta se convierte en coágulo sanguíneo

#### Vulnerabilidad ante Virus
Las plaquetas son vulnerables a la infección viral directa; así se plantea que hay 2 o más virus cercanos y la carga viral de la plaqueta supera 40, se convierte en una partícula de virus.

---

### **PARTÍCULAS VIRALES**

#### Estrategia de Infección Preferencial
Los virus tienen una estrategia inteligente de infección:

1. *Preferencia por glóbulos rojos*: Como son las células más abundantes (45% del sistema), los virus las atacan primero. Si hay glóbulos rojos cercanos, existe un 75% de probabilidad de infectar uno en lugar de buscar otros objetivos.

2. *Ataque a células inmunes como plan B*: Si no hay glóbulos rojos disponibles pero hay células inmunes cercanas, el virus intenta infectarlas con un 40% de probabilidad.

---

### 🔥 **CÉLULAS INFECTADAS** (Periodo de Incubación)

#### Tiempo de Incubación Variable.
El periodo de incubación depende del tipo de célula infectada:
- **Glóbulos rojos infectados**: 3 turnos de incubación
- **Células blancas infectadas**: 4 turnos de incubación (más resistentes)

#### Explosión Viral Inevitable
Una vez que el periodo de incubación se completa, la célula inevitablemente explota liberando nuevos virus, no hay forma de evitar esto si no se rescata a tiempo.

#### Rescate por Sistema Inmune (Ventana Decreciente)
El sistema inmune tiene una ventana de tiempo limitada para rescatar células infectadas. La probabilidad de rescate comienza en 25% pero disminuye un 5% por cada turno que pasa la célula infectada.

*Para glóbulos rojos infectados:*
- Requiere al menos 3 células inmunes cercanas.
- El nivel de anticuerpos debe superar 70.
- Si el rescate tiene éxito, vuelve a ser un glóbulo rojo saludable.

*Para células blancas infectadas:*
- Requiere al menos 4 células inmunes cercanas (umbral más alto).
- El nivel de anticuerpos debe superar 80.
- Si el rescate tiene éxito, vuelve a ser un neutrófilo.



---

###  **EXPLOSIÓN VIRAL**

#### Transformación a Zombie
Después de permanecer 2 turnos en estado de explosión viral, la célula se transforma definitivamente en zombie:
- **70% de probabilidad**: Se convierte en glóbulo rojo zombie
- **30% de probabilidad**: Se convierte en glóbulo blanco zombie

La explosión viral representa el momento en que el virus ha destruido completamente la célula y la ha convertido en una "célula zombie" que ya no funciona correctamente.

---

### 🧟 **CÉLULAS ZOMBIE**

#### Eliminación Masiva por Sistema Inmune
Las células zombie son extremadamente difíciles de eliminar, lo que termina requiriendo una respuesta inmune masiva.

**Condiciones necesarias:**
- Al menos 5 células inmunes cercanas (respuesta coordinada)
- Nivel de anticuerpos superior a 80
- La célula zombie debe tener más de 20 turnos de edad
- Solo un 15% de probabilidad de éxito incluso cumpliendo todas las condiciones

Si la eliminación tiene éxito, la célula zombie se convierte en tejido necrótico (restos celulares).

#### Necrosis Natural (Extremadamente Lenta)
Las células zombie pueden degradarse naturalmente con el tiempo, pero este proceso es extremadamente lento:
- Debe tener más de 50 turnos de edad.
- Solo un 5% de probabilidad por turno de convertirse en tejido necrótico.


---

### 🩸 **COÁGULOS SANGUÍNEOS**

Los coágulos actúan como barreras temporales y tienen la capacidad de disolverse cuando ya no son necesarios.

**Condiciones para disolución:**
- El coágulo debe tener más de 25 turnos de edad (debe ser maduro)
- No debe haber células zombie en el área
- No debe haber células infectadas en el área
- Solo un 20% de probabilidad por turno de disolverse (proceso gradual)

Si se disuelve, el coágulo se convierte en plasma, permitiendo que el flujo sanguíneo vuelva a la normalidad.

**Función biológica:** Las plaquetas crean barreras físicas para contener infecciones, pero estas barreras deben ser temporales para no bloquear permanentemente el torrente sanguíneo.

---

### ☠️ **TEJIDO NECRÓTICO**

#### Regeneración Extremadamente Lenta
El tejido necrótico representa el daño residual más severo causado por la infección zombie. Su regeneración es casi imperceptible:

*Condiciones para regeneración:*
- Debe tener más de 80 turnos de edad (período extremadamente largo).
- Solo un 10% de probabilidad por turno de regenerarse a plasma.

**Significado biológico:** Este tejido representa el daño duradero y casi permanente causado por las células zombie. La recuperación es tan lenta que refleja cómo el daño causado por la senescencia celular es difícil de reparar.

---

## Parámetros Globales del Sistema

### Actualización de Carga Viral (Por Turno)
La carga viral de cada célula se actualiza en cada turno considerando lo siguiente.

*Incrementos (factores que aumentan la carga):*
- Cada virus cercano suma 12 puntos
- Cada célula infectada cercana suma 6 puntos
- Cada célula zombie cercana suma 10 puntos

*Decrementos (factores que reducen la carga):*
- Cada célula inmune cercana resta 18 puntos
- Los anticuerpos totales del vecindario se suman y dividen entre 10, restando ese valor

Es importante mencionar que la carga viral siempre se mantiene entre 0 y 100 puntos.

### Nivel de Anticuerpos
Si hay células inmunes cercanas, el nivel de anticuerpos aumenta gradualmente; esto tomando el total de anticuerpos del vecindario, se divide entre 20, y ese valor se suma al nivel actual. 

### Consumo de Energía
Cada célula gasta energía según su carga viral; por cada 50 puntos de carga viral, se resta 1 punto de energía- La energía no puede bajar de 0.

---

## 🌡️ Métricas del Sistema

### Temperatura Corporal
La temperatura corporal refleja el estado de la infección y la respuesta inmune.

### Tasa de Infección
Se calcula como el porcentaje de células comprometidas del total:

Tasa de Infección = ((Células Infectadas + Células Zombie) / Total de Células) × 100

Esta métrica determina qué tan avanzada está la infección en el sistema.

### Eficiencia Inmune
Mide qué tan activo está el sistema inmune:

Eficiencia Inmune = (Células Inmunes Activas / Total de Glóbulos Blancos) × 100

Un 100% significa que todas las células inmunes están combatiendo activamente la infección.

### Umbral de Zombificación
El organismo se considera completamente zombificado cuando la tasa de infección alcanza o supera el 60%.

---

##  Etapas de Infección

| Tasa de Infección | Etapa |
|-------------------|-------|
| 0% | SALUDABLE |
| >0% | TEMPRANO |
| >5% | MODERADO |
| >20% | SEVERO |
| >40% | CRÍTICO |
| ≥60% | **ZOMBIFICADO** |

---
### Lógica y ejecución.

## Vecindario de Moore

Cada célula analiza sus **8 vecinos** (arriba, abajo, izquierda, derecha y diagonales) para tomar decisiones basadas en:
- Cantidad de virus cercanos.
- Células infectadas.
- Células zombie.
- Células inmunes activas.
- Carga viral del vecindario.
- Nivel de anticuerpos del área.

---

## Estado Médico del Sujeto en Tiempo Real

La interfaz muestra las siguientes métricas vitales:

### Temperatura Corporal
- *Rango normal*: 36-38°C.
- *Color verde*: Temperatura saludable.
- *Color naranja*: Fiebre moderada (>38°C).
- *Color rojo*: Fiebre alta (>39.5°C).
- *Color azul*: Hipotermia (<36°C) o zombificación.

### Nivel de Infección
- Muestra el porcentaje de células comprometidas (infectadas + zombie).
- Barra de progreso que cambia de color según la severidad:
  - Gris: Infección mínima (<10%).
  - Naranja: Infección moderada (10-40%).
  - Rojo: Infección severa (40-70%).
  - Rojo oscuro: Infección crítica (>70%).

### Estado de Zombificación
- **✓ Saludable**: Tasa de infección < 60%.
- **☠ Zombificado**: Tasa de infección ≥ 60% (estado terminal).
- Muestra la etapa actual de la infección.

### Sistema Inmune
- Barra que muestra la eficiencia del sistema inmunitario.
- Indica qué porcentaje de glóbulos blancos están activamente combatiendo.

### 🔬 Análisis Celular
Conteo en tiempo real de:
- **Eritrocitos** (glóbulos rojos)
- **Leucocitos** (glóbulos blancos) con células activas
- **Infectadas** (células en periodo de incubación)
- **Virus** (partículas virales libres)
- **Zombie** (células senescentes)
