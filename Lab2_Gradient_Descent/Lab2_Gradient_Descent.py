#Импортируем библиотеки
import numpy as np
import matplotlib.pyplot as plt
from   mpl_toolkits.mplot3d import Axes3D
import random

#Вводим переменные
x_start       = random.uniform(-25, 25)
y_start       = random.uniform(-25, 25)
x_current     = x_start
y_current     = y_start
func_value    = []      #Cписок для визуализации изменения значений функции
counter_value = []      #Cписок для кол-ва итераций при соответвующем значении функции       

lambd   = 0.0001        #Специально написано с ошибкой, т.к. в Python есть команда "lambda"
delta   = 0.00001
counter = 0


#Вводим функции для расчётов
#Вводим функцию, у которой будем вычислять минимум
def Func(x, y):
    function = ((y - x*x)*(y - x*x) + (1-x)*(1-x)) #(x + y*y) + 4*y*y - x
    return function


#Вычисляем шаги для обеих координат
def Step():
    step_x = random.uniform(-delta, delta)
    step_y = random.uniform(-delta, delta)

    #Делаем так, чтобы шаг ВСЕГДА был отличен от нуля
    while step_x == 0:
         step_x = random.uniform(-delta, delta)
    while step_y == 0:
         step_y = random.uniform(-delta, delta)   
    return step_x, step_y

#Вычисляем градиенты
def Calc_grad(x, y):
    step_x, step_y = Step()
    grad_x = (Func(x + step_x, y) - Func(x, y))/step_x
    grad_y = (Func(x, y + step_y) - Func(x, y))/step_y
    return grad_x, grad_y

#Вычисляем новые координаты
def Calc_new_coords(x_current, y_current, grad_x, grad_y):
    x_new = x_current - lambd*grad_x
    y_new = y_current - lambd*grad_y
    return x_new, y_new


#Метод градиентного спуска
while True:
    if counter > 0:              #Пропускаем это в 1-ю итерацию, т.к. x_new, y_new ещё не посчитаны
        x_current, y_current = x_new, y_new   #Обновляем значение координат в каждой новой итерации
    
    grad_x, grad_y = Calc_grad(x_current, y_current)
    x_new, y_new = Calc_new_coords(x_current, y_current, grad_x, grad_y)

    counter +=1

    if counter == 0 or counter % 10 == 0:
        counter_value.append(counter)
        func_value.append(Func(x_new, y_new))

    if counter % 100000 == 0:
        print('Функция на предыдущей итерации:', Func(x_current, y_current))
        print('Функция на текущей итерации:', Func(x_new, y_new))
        print('Прошло', counter / 1000, 'к итераций\n')

    if Func(x_new, y_new) > Func(x_current, y_current) or counter == 1000000:   
        x_min, y_min = x_new, y_new 
        print('Минимум функции находится на координатах [', round(x_min, 3), ',', round(y_min, 3), ']')
        print('В точке минимума функция равна:', Func(x_min, y_min))
        break


#Вводим функции для визуализации
#Визуализируем 2D график изменения функции при её минимизации
def Draw_2d():
    plt.plot(counter_value, func_value)
    plt.grid()
    plt.title("Эволюция функции при градиентом спуске")
    plt.ylabel("Значение функции")
    plt.xlabel("Количество выполненных итераций")

    plt.show()

#Визуализируем 3D график функции в окрестности точки минимума
def Draw_3d():
    #Создаём поле для создания графика
    x = np.linspace(-20, 20, 1000)
    y = np.linspace(-5, 5, 100)
    x_grid, y_grid = np.meshgrid(x, y)
    z = Func(x_grid, y_grid)

    #Визуализируем график
    fig = plt.figure()
    axes = fig.add_subplot(projection='3d')
    axes.plot_surface(x_grid, y_grid, z, cmap="inferno", alpha=0.9, label="f(x, y) = (y - x*x)*(y - x*x) + (1-x)*(1-x)")

    axes.set_title("График функции в окрестности точки минимума")
    axes.set_xlabel("x")
    axes.set_ylabel("y")
    axes.set_zlabel("f(x,y)")

    #Добавляем точку минимума
    z_min = Func(x_min, y_min)
    axes.scatter(x_min, y_min, z_min, color="red", s=100, label="Точка минимума")

    axes.legend()

    plt.show()
