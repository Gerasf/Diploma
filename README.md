# Детектор парковки

### Веб-интерфейс приложения  
[Ссылка на видео](https://user-images.githubusercontent.com/58944748/218282781-35e7a09f-0e87-4e06-93f1-61162b645a69.mp4)

## Описание проекта

**Parking Detector** — это приложение компьютерного зрения, разработанное на **Python**, которое в режиме реального времени определяет свободные парковочные места и отслеживает занятые, помогая водителям быстро находить доступные места.

Приложение также имеет веб-интерфейс на основе **Flask**, который отображает информацию о доступных парковочных местах. Данные хранятся в базе данных **MongoDB**, что облегчает их извлечение и обработку.

Для повышения производительности используются **многопоточность и многопроцессность**, что обеспечивает стабильную работу приложения даже при высокой нагрузке. Также реализовано подключение к IP-камере по **HTTP**, что позволяет получать актуальное видео с парковки.

## Основные функции

- Python  
- Компьютерное зрение  
- Веб-приложение на Flask  
- База данных MongoDB  
- Многопоточность и многопроцессность  
- Динамическое программирование  
- HTTP-соединение с IP-камерой  
- Фронтенд: JavaScript, HTML, CSS  

## Как это работает?

**На основном видео показан результат веб-приложения — красные отметки обозначают занятые места (обнаруженные моделью Yolov5), зелёные — свободные парковочные позиции.**

### Используются две коллекции: `parking_areas` и `parking_positions`  
1. **parking_areas** — данные, которые пользователь указывает вручную. (Остальное — автоматически).  
2. **parking_positions** — содержит список потенциальных парковочных позиций. Каждая позиция добавляется, когда автомобиль заезжает на парковку, и определяется как оптимальная в рамках заданной зоны.

### Основные классы:

#### Parking Position Detector  
Отвечает за создание потенциальных свободных парковочных позиций.

#### Parking Model  
Использует модель Yolov5 для определения занятых мест и выбора наибольшего числа свободных мест из коллекции `parking_positions`.

#### Пример работы

1. Начинаем с видео:

   ![step 1](https://user-images.githubusercontent.com/58944748/218277649-12947e8a-3bc0-4180-af1e-2154931c5887.png)

2. Выделяем парковочную зону:

   ![step 2](https://user-images.githubusercontent.com/58944748/218277730-0616bb78-1b63-443a-a17a-c5ec8736c48b.png)

3. Алгоритм определяет момент въезда автомобиля, выбирает оптимальное место и добавляет его в `parking_positions`.

   [Ссылка на видео](https://user-images.githubusercontent.com/58944748/218277975-711796f7-0708-4dce-a1bf-5b4bd51ae9ed.mp4)

4. Результат:

   ![step 4](https://user-images.githubusercontent.com/58944748/218277882-8294c70a-d4f7-45eb-b01b-a81d570dd2af.png)

---

## Проблемы

Использование Yolov5 для определения занятых мест не всегда идеально.  
На изображении ниже можно заметить занятые места, не зафиксированные моделью:

![ошибка 1](https://user-images.githubusercontent.com/58944748/218128212-fb393097-bb5b-430c-abce-ce5e77851a5f.png)

Здесь зелёная метка показывает свободное место, хотя оно занято — результат работы Parking Position Detector:

![ошибка 2](https://user-images.githubusercontent.com/58944748/218128937-3348fe8e-0454-4772-bc33-97ff2e397575.png)

А в этом примере почти идеальное определение (хотя пара машин пропущена):

![почти идеал](https://user-images.githubusercontent.com/58944748/218129495-15cfbd82-3d6c-4313-891d-b7f801c480e6.png)

---

## Классы

### Server  
Скрипт Flask-приложения, обеспечивающего мониторинг парковки.  
Функции:

- Создаёт экземпляр `parking_model`, запускает поток `stream` — видеопоток и обновление информации о местах.
- Создаёт экземпляр `parkingPositionsDetector`, запускает поток `detectionAlgorithm`.
- Подключает базу данных через `DbHandler`.
- Четыре маршрута:
  - `/video_feed` — видеопоток.
  - `/info` — JSON с данными о количестве свободных/всего мест.
  - `/` — основной маршрут.

### Parking Model  
Использует **YOLOv5** через **PyTorch Hub** и видеопоток с камеры.  
Загружает данные о зонах/местах из БД.  
Методы:

- Обработка кадров для выявления занятых мест.
- Разметка кадров.
- Подсчёт количества свободных/занятых мест.
- Оптимизация выбора мест с помощью **динамического программирования** и задачи о **максимальном независимом множестве**.

### Parking Position Detector  
Использует **OpenCV** и фоновое вычитание для выявления изменений.  
- Зоны парковки задаются 4 точками.
- Определяет въезд автомобиля и добавляет его позицию.
- Поддержка операций добавления/удаления зон и мест.
- Отрисовка зон и потенциальных мест.

### Tracker  
Отслеживает объекты (машины) и минимизирует количество парковочных позиций.  
Сохраняет позиции, возвращает оптимальное место после остановки машины.

### DbHandler  
Работает с базой MongoDB с помощью **PyMongo**.  
Поддерживает добавление, удаление и получение данных о зонах и местах.

---
