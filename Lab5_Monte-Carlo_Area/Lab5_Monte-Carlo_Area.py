#Импортируем библиотеки
import numpy as np
import random
import cv2


#Считываем изображение
image_bgr    = cv2.imread('tahoe_lake.jpg')   #Название такое странное из-за стандарта OpenCV: вместо RGB - BGR(Blue, Green, Red)

#Вводим константы для библиотеки OpenCV
pixel_length = 5/111                #Длина одного пикселя в масштабе изображения(5 км = 111 пикселей)
pixel_area   = pixel_length ** 2
image_width  = image_bgr.shape[1]   #Ширина всего изображения в пикселях 
image_height = image_bgr.shape[0]   #Высота всего изображения в пикселях 
pixels_total = image_width * image_height

#Вводим константы для метода Монте Карло
total_iterations  = 2000000
hits_in_water     = 0
hits_total        = total_iterations
approx_water_area = 0
part_occupied_by_water = 0
                               
                     
#Переходим от массива BGR к HSV(Hue, Sateration, Value - Оттенок, Насыщенность, Яркость)
image_hsv    = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

#Задаём нижний и верхний пределы HSV и создаём маску с этими пределами, чтобы программа отличила воду от суши
bottom_limit = np.array([90, 60, 60])
top_limit    = np.array([140, 255, 255])
mask         = cv2.inRange(image_hsv, bottom_limit, top_limit)

#Найдём число пикселей, которое занимает вода
pixels_water = np.count_nonzero(mask)
water_area   = pixel_area*pixels_water


#Метод Монте-Карло
#Берём случайные точки и считаем сколько из них окажется в воде
for i in range(total_iterations):             
    x = random.randint(0, image_width-1)
    y = random.randint(0, image_height-1)

    if mask[y, x] > 0:
        hits_in_water += 1
    if i % 100000 == 0 and i != 0:
        print(f'Прошло {int(i/1000)}к итераций')
#Находим какую долю занимает водоём от всего изображения
part_occupied_by_water = hits_in_water/hits_total
#Умножаем долю водоёма от всего изображения на площадь всего изображения
approx_water_area = part_occupied_by_water * pixels_total*pixel_area


#Считаем погрешность
abs_error = abs(water_area - approx_water_area)
relative_error = abs_error/water_area * 100


#Выводим общую информацию на экран
print('\n--------------------------------------------------------------------------------------------------')
print(f'Ширина изображения в пикселях: {image_width}\nВысота изображения в пикселях: {image_height}')
print(f'Общее количество пикселей: {image_width*image_height}\nКоличество пикселей занятых водоёмом: {pixels_water}')
print(f'Точная часть изображения, занимаемая водой: {pixels_water/pixels_total}')
print('--------------------------------------------------------------------------------------------------')
print(f'Площадь одного пикселя: {round(pixel_area, 3)} км^2\nПлощадь всего изображения: {round(pixels_total*pixel_area, 3)} км^2\nТочная площадь водоёма: {round(water_area, 3)} км^2')
print('--------------------------------------------------------------------------------------------------')
print(f'Общее кол-во случайных точек(кол-во итераций): {hits_total}\nКол-во точек попавших в воду: {hits_in_water}')
print(f'Часть изображения, занимаемая водой по методу Монте-Карло: {part_occupied_by_water}\nПриблизительная площадь водоёма по методу Монте-Карло: {round(approx_water_area, 3)} км^2')
print('--------------------------------------------------------------------------------------------------')
print(f'Абсолютная погрешность: {round(abs_error, 4)} км^2\nОтносительная погрешность: {round(relative_error, 4)} %')
print('--------------------------------------------------------------------------------------------------\n')



#Выводим изображение на экран
cv2.imshow('Tahoe Lake', image_bgr)
cv2.imshow('Mask', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Сохраняем изображение
cv2.imwrite('mask.png', mask)