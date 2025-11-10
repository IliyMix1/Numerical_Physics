#Импортируем библиотеки
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


#Задаём константы
dx, dt = 0.01, 0.001
x_start, string_len = 0.5, 1.0
num_of_x = int(string_len/dx)
num_of_t = int(1/dt)

c = dx/dt
r = c*dt/dx      
k = 60


#Вводим несколько функций, задающих начальную конфигурацию струны
def Config_func_1(x, x_start=0.0):
    return np.exp(-k*(x - x_start)**2)
def Config_func_2(x, x_start=0.0):
    return np.cos(np.pi*(x - x_start))**2


#Дискретизируем пространство
x = np.linspace(0.0, string_len, num_of_x)

#Создаём отдельные массивы под прошлый, текущий и следующий моменты времени
wave_past    = np.zeros(num_of_x)
wave_present = np.zeros(num_of_x)
wave_future  = np.zeros(num_of_x)

#Инициализируем массив с помощью конфигурационной функции
wave_present = Config_func_1(x, x_start)
wave_past = np.copy(wave_present)    #В начальный момент времени, значения в прошлый и текущий моменты времени равны(т.к. прошлого ещё как бы нет)

#Создаём массив, хранящий все значения координат во все моменты времени. В каждой строке хранится значение всех координат в какой-то конкретный момент времени
wave_coords_and_time = np.zeros([num_of_t, num_of_x])
wave_coords_and_time[0, :] = wave_present

#Численно вычисляем координаты волны
for i in range(1, num_of_t):           
    for n in range(1, num_of_x - 1):   #Меняем только внутренние точки, пропуская граничные
        wave_future[n] = 2*(1 - r*r)*wave_present[n] - wave_past[n] + r*r*(wave_present[n+1] + wave_present[n-1])

    #Граничные точки зафиксированы в нуле
    wave_future[0]  = 0.0
    wave_future[-1] = 0.0

    #Обновляем массивы
    wave_past    = np.copy(wave_present)
    wave_present = np.copy(wave_future)
    wave_coords_and_time[i, :] = wave_present



#Вводим 2 функции для визуализации данных: первая выдаёт анимацию, вторая выдаёт множество фото
def Show_wave_animation(x, Y, interval=20):
    fig, ax = plt.subplots()
    line, = ax.plot(x, Y[0, :])
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlabel('x, м.')
    ax.set_ylabel('y, м.')
    ax.set_title('Симуляция колебаний струны')

    def update(frame):
        line.set_ydata(Y[frame, :])
        return line,

    ani = animation.FuncAnimation(fig, update, frames=Y.shape[0], interval=interval, blit=True)
    plt.show()

def Show_wave_photos(x, Y):
    time_steps = [
        0,
        int(num_of_t/9),
        int(num_of_t*2/12),
        int(num_of_t*3/12),
        int(num_of_t*4/12),
        int(num_of_t*5/12),
        int(num_of_t*6/12),
        int(num_of_t*7/12),
        int(num_of_t*8/12),
        int(num_of_t*9/12),
        int(num_of_t*10/12),
        int(num_of_t*11/12),
    ]

    # Делать массив снимков
    snapshots = []
    for i in time_steps:
        snapshots.append((i * dt, Y[i, :]))

    # Рисуем 12 графиков в одном окне
    fig, axs = plt.subplots(4, 3, figsize=(12, 6))
    for idx, (t_i, y_i) in enumerate(snapshots):
        row = idx // 3
        col = idx % 3
        ax = axs[row, col]
        ax.plot(x, y_i)
        ax.set_title(f"t = {t_i:.3f} c.")
        ax.set_xlabel('x, м.')
        ax.set_ylabel('y, м.')
        ax.grid(True)

    plt.tight_layout()
    plt.show()   


#Выводим результат на экран
Show_wave_animation(x, wave_coords_and_time)
#Show_wave_photos(x, wave_coords_and_time)