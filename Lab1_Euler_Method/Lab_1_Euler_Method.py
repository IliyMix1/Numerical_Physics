#Импортируем библиотеки
import matplotlib.pyplot as plt

#Создаём списки с табличными значениями температур и моменты времени
tabular_values = [83.0, 77.7, 75.1, 73.0, 71.1, 69.4, 67.8, 66.4, 64.7, 63.4, 62.1, 61.0, 59.9, 58.7, 57.8, 56.6]
time_tabular = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


#Вводим функцию, использующую метод Эйлера
def Euler_method(gamma, temperature_start, temperature_end, temperature_room, dt):
    #Функция принимает начальную и конечную температуру + шаг, а на выходе выдаёт списки с аппроксимированными значениями температур в конкретные моменты времени
    temperature_current = temperature_start
    experimental_values = []                  
    time_list = []
    i = 0

    while temperature_current > temperature_end:
        temperature_current = temperature_current - dt * gamma * (temperature_current - temperature_room)

        if (dt * i).is_integer() or temperature_current < temperature_end:        #Второе условие нужно, чтобы получить точный момент времени, в который температура максимально приблизится к желаемому значению
            time_list.append(dt * i)                         
            experimental_values.append(temperature_current)
            
        if temperature_current == temperature_room:
            break
        i += 1
    return experimental_values, time_list

#Вводим функцию, которая использует метод Эйлера ФИКСИРОВАННОЕ количество раз, ТОЛЬКО ради сравнения полученных данных с табличными
def Euler_method_for_gamma(gamma):
    experimental_values = [] 
    temperature_current = tabular_values[0]
    temperature_room = 22.0
    dt = 0.001
    i = 0

    while (dt*i) < 15:
        temperature_current = temperature_current - dt * gamma * (temperature_current - temperature_room)

        if (dt*i).is_integer():
            experimental_values.append(temperature_current)
        i += 1

    return experimental_values

#Вводим функцию для подсчёта наиболее подходящего параметра "гамма"
def Find_best_gamma(pos_start, pos_end, step):
    pos_current = pos_start
    global_deviation = []

    while pos_current < pos_end:
        deviation = []
        experimental_values = Euler_method_for_gamma(pos_current)
        min_len = min(len(tabular_values), len(experimental_values))

        for j in range(min_len):
            deviation.append((tabular_values[j] - experimental_values[j]) ** 2)
        global_deviation.append(sum(deviation) ** 0.5/min_len)

        pos_current = pos_current + step
    min_index = global_deviation.index(min(global_deviation))

    return (pos_start + step*min_index)
best_gamma = Find_best_gamma(0.01, 0.1, 0.0002)
print(best_gamma)

#Считаем за какое время кофе охладится до определённой температуры
for j in range(1, 4):
    _, time_list = Euler_method(best_gamma, 83.0, (22 + 61/(2 ** j)), 22, 0.001)
    print('Кофе охладится до температуры', (22 + 61/(2 ** j)), '°С(Tкофе - Troom =', 61/(2 ** j),  '°С) за', time_list[-1], 'мин')


#С помощью алгоритма решаем дилемму с кофе и молоком
_, time_list = Euler_method(best_gamma, 90.0, 80.0, 22.0, 0.001)
print('\nЕсли сначала ждать, а потом добавлять молоко, то кофе остынет за', time_list[-1], 'мин.')

_, time_list = Euler_method(best_gamma, 85.0, 75.0, 22.0, 0.001)
print('Если сначала добавить молоко, а потом жать, то кофе остынет за', time_list[-1], 'мин.')


#Вычисляем зависимость между шагом dt и разностью между табличным и численным значениями T при t = 1 мин. 
steps = [0.1, 0.05, 0.025, 0.01, 0.005]
tempetature_perfect1 = 80.45
tempetature_perfect5 = 71.29

difference1_list = []
difference5_list = []
for i in range(5):
    values, _ = Euler_method(best_gamma, 83.0, 56.6, 22.0, steps[i])
    difference1 = 80.45 - values[1]
    difference5 = 71.29 - values[5]
    difference1_list.append(difference1)
    difference5_list.append(difference5)
print('\nРазница при t = 1 мин.', difference1_list)
print('\nРазница при t = 5 мин.', difference5_list)

#Аппроксимируем значения температур с помощью уравнения Ньютона и метода Эйлера
experimental_values, time_list = Euler_method(best_gamma, 83.0, 29.625, 22.0, 0.001)
print(experimental_values)

#Визуализируем данные
plt.subplot(1, 2, 1)
plt.plot(time_tabular, tabular_values, marker='o', ms=4, label='Табличные значения')
plt.plot(time_list, experimental_values, color='red', marker='o', ms=4, label='Значения, полученные по формуле теплопроводности Ньютона')
plt.axhline(y = 52.5, color='purple', label='Разница температур 61/2°С')
plt.axhline(y = 37.25, color='purple', label='Разница температур 61/4°С')
plt.axhline(y = 29.625, color='purple', label='Разница температур 61/8°С')

plt.grid()
plt.title("Зависимость температуры кофе от времени")
plt.ylabel("T, °С")
plt.xlabel("t, мин.")
plt.legend()


plt.subplot(1, 2, 2)
plt.plot(steps, difference1_list, marker='o', ms=4, label='Разность при t = 1 мин.')
plt.plot(steps, difference5_list, marker='o', ms=4, label='Разность при t = 5 мин.')
plt.grid()
plt.title("Зависимость разности между численным и точным значениями температур от шага Δt")
plt.ylabel("Разность между численным и точным значениями температур")
plt.xlabel("Δt, мин.")
plt.legend()

plt.show()

