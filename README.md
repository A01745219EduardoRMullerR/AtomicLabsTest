# AtomicLabsTest
### Examen de programacion para Atomic Labs


Se uso la cuadricula como un plano de coordinadas x,y

Como todos tienen que recorrer hacia abajo donde esta la salida de tomo como origen (0,0) la parte superior izquierda de la cuadricula
X aumentaba a la derecha y Y hacia abajo

Se crearon listas de las posiciones de todos los elementos:

- Zombies
- Empleados
- Ventanas
- Salidas
- Paredes (para estas se guardaron todas las coordenadas o cuadritos que ocupaban)
- Humanos salvados

```python
#Variables globales, aqui estaran listas conformadas por listas de tamaño 2 para representar la forma (x,y)
# (referencia: el punto de origen (0, 0) esta ubicado en la parte superior izquierda de la cuadricula y esta es de 18x18
# las ventanas se tomaran como 0 en y las salidas como 19 en x)
#Posiciones de las ventanas en una lista
windows = [[3, 0], [4, 0], [5, 0], [6, 0], [13, 0], [14, 0], [15, 0], [16, 0]]
#Lista de las posiciones de los empleados
employees = [[9, 1], [3, 3], [6, 3], [11, 3], [15, 3], [4, 5], [15, 6], [2, 7], [7, 7], [3, 8], [17, 8]
             ,[11, 9], [13, 12], [3, 13], [17, 13], [6, 14], [10, 15], [3, 17], [7, 17], [13, 17]]
#Lista de las paredes, se van a anotar todos los cuadros individuales que ocupan
walls = [[2,4], [3, 4], [5, 4], [6, 4], [7, 4],
         [10, 4], [11, 4], [12, 4], [13, 4], [14, 4], [15, 4], [16, 4],
         [13, 5], [13, 6], [13, 7],
         [1, 10], [2, 10], [3, 10], [4, 10], [5, 10], [6, 10], [7, 10], [8, 10],
         [12, 10], [13, 10], [14, 10], [15, 10], [16, 10], [17, 10], [18, 10],
         [2, 12], [3, 12], [4, 12], [5, 12], [6, 12], [7, 12],
         [12, 12], [12, 13], [12, 14], [12, 15],
         [16, 12], [16, 13], [16, 14], [16, 15],
         [2, 16], [3, 16], [4, 16], [5, 16], [6, 16], [6, 16]]
#Lista de los cuadros de salida
exits = [[19, 15], [19, 16], [19, 17], [19, 18]]
#Lista de Zombies, empieza vacia
zombies = []
#lista de empleados salvados
saved = []


```

Para el movimiento de los zombies se uso la funcion randint de la libreria Random y solo se hicieron funciones extra para revisar colisiones. Estas funciones solo regresaban True o False dependiendo si estaban a lado o arriba/abajo de una pared.

Para el movimiento de los empleados se dividieron por sectores dado que estos siempre empezaban en el mismo lugar.
Se buscaba que todos los empleados de la altura 1 a 3 se alinearan en la columna 9 ya que esta era la forma mas directa a la parte estrecha de la oficina
Para los que se encontraban entre la 4 y la 9, primero habia que ver que no colisionaran con la pared de la derecha, entonces todos de la columna 13 a la izquierda recorrian hasta llegar a una altura entre 9 y 11, los de la derecha de la columna 13 tenian que bajar hasta la altura 8 y entonces si moverse hacia la columna 11
Los humanos 14 y 16 recorrian a la derecha hasta llegar a la columna 8, una vez ahi bajaban hasta la 15 y ya solo recorrian a la derecha
Los humanos 13 y 15 tenian que bajar a la altura 16 y 15 respectivamente y entonces ya podian recorrer a la derecha. El humano 17 solo bajaba una fila y de ahi recorria a la derecha hasta la salida. Finalmente, el humano 20 solo recorria a la derecha.
El algoritmo de decision para esto quedo asi:

```python
x_employee = employee[0]
            y_employee = employee[1]
            if y_employee <= 3:
                if x_employee < 9:
                    employee[0] += 1
                elif x_employee > 9:
                    employee[0] -= 1
                elif x_employee == 9:
                    employee[1] += 1
            if 4 <= y_employee <= 10:
                if x_employee < 9:
                    employee[0] += 1
                elif x_employee > 11:
                    if y_employee > 7:
                        employee[0] -= 1
                    elif y_employee < 7:
                        employee[1] += 1
                elif 9 <= x_employee <= 11:
                    employee[1] += 1
            if y_employee > 10 and y_employee < 15:
                if x_employee < 9:
                    employee[0] += 1
                elif x_employee >= 11 and y_employee < 15:
                    employee[1] += 1
            if y_employee >= 15 and y_employee < 18:
                if x_employee <= 18:
                    employee[0] += 1
```

Para los infectados se revisaban las coordanadas de cada Zombie y se comparaban con las de cada humano con forma de for anidado, si la diferencia de coordenadas en x o en y era de 1 es que estaba a lado el zombie y entonces podia infectarlo.

Finalmente para llegar a la salida tenian que estar en las posiciones (19, 15), (19, 16), (19, 17) y (19, 18). Se comprobaba su posicion y se marcaba como salvado
