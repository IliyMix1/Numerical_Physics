#Импортируем библиотеки
import matplotlib.pyplot as plt
import numpy as np
import random


#Вводим константы
total_iterations = 500000
left_border      = 0
right_border     = 3
delta            = 2.7
x    = []
x.append(random.uniform(left_border, right_border))
counter_accepted = 0
#Создаём массив абсцисс, по которым будем строить график функции
abscissa = np.linspace(left_border, right_border, 100)

#Вводим функцию распределения
def distribution_func(x):
    return 2*x * np.exp(-(x)**2)

#Создаём массив ординат, по которым будем строить график функции
ordinate = [distribution_func(abscissa[i]) for i in range(100)]


#Метод Метрополиса
for i in range(total_iterations):
    step  = random.uniform(-delta, delta)
    x_new = x[i] + step

    if x_new < left_border or x_new > right_border:
        x_new = x[i] + step

    r = distribution_func(x_new) / distribution_func(x[i])
    u = random.random()

    if r >= 1 or u <= r:
        x.append(x_new)

        counter_accepted += 1
    else:
        x.append(x[i])

    if i % 10000 == 0:
        print(f'Прошло {int(i/1000)}к итераций')

#Выводим количество принятых точек
print(f'Было принято {round(counter_accepted/total_iterations*100)}% шагов')


#Визуализируем
plt.hist(x, density=True, bins=100, color='red', alpha=0.6)
plt.plot(abscissa, ordinate, linewidth=2, color='black')
plt.xlabel('x')
plt.ylabel('p(x)')
plt.title('Функция распределения Вейбулла')
plt.grid()


plt.show()

