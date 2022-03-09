#Autor: Eduardo R. Muller Romero
#Creado: 6 de marzo 2022

import os
from random import randint

#------------------------------------------------------------------------------
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


def generateZombie():
    randomWindow = randint(0, len(windows)-1)
    entry = windows[randomWindow]
    return entry

def checkCollisionX(x):  #recorre la lista de paredes para ver si colisiona en X, regresa True si es el caso, False si no
    for wall in walls:
        x_wall = wall[0]
        if (x_wall+1 == x) or (x_wall-1 == x):
            return True
    return False

def checkCollisionY(y): #recorre la lista de paredes para ver si colisiona en Y, regresa True si es el caso, False si no
    for wall in walls:
        y_wall = wall[1]
        if (y_wall + 1 == y) or (y_wall - 1 == y):
            return True
    return False

def moveZombie():
    for zombie in zombies:
        for n in range(4):  # Los cuatro movimientos que va a hacer el zombie:
            j = randint(0,1) #0 se mueve en x, 1 se mueve en y
            if j == 0 and zombie[0]<17:
                if not(checkCollisionX(zombie[0])):
                    zombie[0] += 1
                elif not(checkCollisionY(zombie[1])):
                    zombie[1] += 1

            elif j == 1 and zombie[1]<17:
                if not(checkCollisionY(zombie[1])):
                    zombie[1] += 1
                elif not(checkCollisionX(zombie[0])):
                    zombie[0] += 1


def moveEmployee():
    for employee in employees:
        for n in range(2):
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


def checkInfections(file):
    for zombie in zombies:
        x_zombie = zombie[0]
        y_zombie = zombie[1]
        for employee in employees:
            x_employee = employee[0]
            y_employee = employee[1]
            if (abs(x_employee - x_zombie) == 1) or (abs(y_employee - y_zombie) == 1): #empleado se va a infectar por zombie
                file.write("Humano " + str(employees.index(employee) + 1) + " infectado en " + str(employee) + "\n")
                zombies.append(employee)
                employees.remove(employee)
                break

def checkSaved(file):
    for employee in employees:
        if (employee[0] == 19) and (employee[1] in range(15, 19)):
            file.write("Humano " + str(employees.index(employee) + 1) + " salvado " + str(employee) + "\n")
            saved.append(employee)
            employees.remove(employee)



def main():
    file = open("Output", 'w')
    file.write("Bienvenido: " + os.getlogin())
    file.write("\n------------------------------------\nAtaque en Atomic Labs\n\n")
    file.write("\nIteracion | Numero de Zombies | Numero de empleados en la oficina | Numero de humanos salvados\n")
    iterations = 1
    zombie1Pos = generateZombie()
    zombies.append(zombie1Pos)
    file.write("Zombie llegó por la ventana de la casilla " + str(zombie1Pos) + "\n")
    zombie2Pos = generateZombie()
    zombies.append(zombie2Pos)
    file.write("Zombie llegó por la ventana de la casilla " + str(zombie2Pos) + "\n")
    while (len(employees) > 0):
        string_lst = [str(iterations), " | ", str(len(zombies)), " | ", str(len(employees)), " | ", str(len(saved)), '\n']
        string = ''.join(string_lst)
        file.write(string)
        moveZombie()
        moveEmployee()
        checkInfections(file)
        checkSaved(file)
        iterations += 1

main()