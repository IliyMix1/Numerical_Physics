#Импортируем библиотеки
import matplotlib.pyplot as plt
import numpy as np


#Вводим константы
rows              = 10
columns           = 10
highest_potential = 10.0
lowest_potential  = 0.0
max_iterations    = 10000


#Вводим функцию для инициализации матрицы(все значения, кроме граничных, - рандомны)
def Init_matrix(rows, columns, highest_potential, lowest_potential=0.0):
    matrix = [[lowest_potential for _ in range(columns)] for _ in range(rows)]
    #matrix[5][5] = 4
    matrix = np.array(matrix)          #Переходим к типу массивов Numpy ради повышения удобства работы

    #Задаём потенциал всех на границах
    matrix[0, :]  = highest_potential
    matrix[-1, :] = highest_potential/2
    matrix[:, 0]  = highest_potential/2
    matrix[:, -1] = highest_potential

    #Создаём массив, в котором граничные значения несут значение True, а внутренние - False
    is_border_matrix = [[False for _ in range(columns)] for _ in range(rows)]
    is_border_matrix = np.array(is_border_matrix)
    is_border_matrix[0, :]  = True
    is_border_matrix[-1, :] = True
    is_border_matrix[:, 0]  = True
    is_border_matrix[:, -1] = True

    return matrix, is_border_matrix

#Вводим функцию для вычисления среднего потенциала в каждой точке
def Calc_average_potential(matrix, is_border_matrix, total_iterations=10000, precision=0.01):
    rows, columns = matrix.shape        #Получаем размерность матрицы
    counter = 0
    matrix_old = np.zeros_like(matrix)  #Вводим этот массив вне цикла, чтобы можно было поставить его в условие цикла

    while np.max(np.abs(matrix - matrix_old)) > precision and counter < total_iterations:   #Прерываем цикл, если равны матрицы на прошлом и текущем шагах np.max(np.abs(matrix - matrix_old)) >= 0.01
        matrix_old = np.copy(matrix)

        for i in range(rows):
            for j in range(columns):
                if is_border_matrix[i][j]:
                    continue
                
                potential = (matrix_old[i+1][j] + matrix_old[i-1][j] + matrix_old[i][j+1] + matrix_old[i][j-1])/4      #Считаем среднее арифметическое
                matrix[i][j] = potential
        counter += 1
        
        if counter % 10 == 0:
            print('Прошло', counter, 'итераций')    #Для отладки

    print('Общее количество итераций:', counter)
    return matrix, counter


#Инициализируем матрицу
matrix, is_border_matrix = Init_matrix(rows, columns, highest_potential, lowest_potential)
print(matrix)
#Высчитываем значения внутри матрицы
matrix, total_iterations = Calc_average_potential(matrix, is_border_matrix)
print(matrix)

#Визуализируем
plt.imshow(matrix, cmap='inferno')
plt.title('Изменение потенциала после ' + str(total_iterations) + ' итераций')
plt.xlabel('X')
plt.ylabel('Y')
plt.colorbar(label='Потенциал, В.')

plt.show()