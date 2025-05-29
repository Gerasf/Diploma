import cv2
import numpy as np
from shapely.geometry import Point, Polygon
from tracker import *
FREE_COLOR     = (0, 255, 0)   # зелёный
OCCUPIED_COLOR = (0,   0, 255) # красный

class Detector:
    def __init__(self, stream, db):
        self.__cap = cv2.VideoCapture(stream)
        if not self.__cap.isOpened():
            raise ValueError(f"Не удалось открыть видеопоток: {stream}")
        self.__parkingArea = []
        self.__object_detector = cv2.createBackgroundSubtractorKNN()
        self.__tracker = Tracker()
        self.__db = db
        self.__parkingAreas = self.__db.getParkingArea()
        self.__parkingPositions = self.__db.getParkingPositions()


    # *****************************
    # Mark parking Area functions
    # *****************************

    # Arrange points clock wise direction
    # def rearrangeParkingAreaPoint(parkingArea):


    # Append to the parking area the point which was chosen using mouse
    def __chooseborderPoint(self, events, x, y, flags, params):
        if events == cv2.EVENT_LBUTTONDOWN:
            self.__parkingArea.append((x, y))


    # Mark 4 points of parking area
    def __markParkingArea(self, frame):
        while True:
            cv2.imshow("parkingMarker", frame)

            cv2.setMouseCallback("parkingMarker", self.__chooseborderPoint)

            cv2.waitKey(1)

            if len(self.__parkingArea) == 4:
                cv2.destroyWindow('parkingMarker')
                break

        # MAYBE need to reArrange the point by (point1,point2,point3,point4) = (upper_left, upper_right, bottom_right, bottom_left)
        # rearrangeParkingAreaPoint(parkingArea)

        self.__parkingAreas.append(self.__parkingArea)
        self.__db.addParkingArea(self.__parkingArea[0], self.__parkingArea[1], self.__parkingArea[2],
                                 self.__parkingArea[3])
        print("Добавлена парковочная зона:", self.__parkingArea)
        self.__parkingArea = []


    # Delete using mouse:
    # Right click for parking area
    # Left click for parking position
    def __deleteByClick(self, events, x, y, flags, params):
        if events == cv2.EVENT_RBUTTONDOWN:
            # check if click is in a parking area - delete it
            for i, pos in enumerate(self.__parkingAreas):
                polyg = Polygon(pos)
                point = Point(x, y)
                if point.within(polyg):
                    self.__parkingAreas.pop(i)
                    self.__db.deleteParkingArea(pos[0], pos[1], pos[2], pos[3])

        if events == cv2.EVENT_LBUTTONDOWN:
            # check if click is in a parking area - delete it
            for i, pos in enumerate(self.__parkingPositions):
                px, py, pw, ph = pos
                polyg = Polygon([(px, py), (px + pw, py), (px, py + ph), (px + pw, py + ph)])
                point = Point(x, y)
                if point.within(polyg):
                    self.__parkingPositions.pop(i)
                    self.__db.deleteParkingPosition(pos[0], pos[1], pos[2], pos[3])

    # ****************************
    # end marking Area functions
    # ****************************


    # if car is inside parking area, append it to list and save position
    def __addPotentialParkingPositions(self, x, y, w, h, potentialParkingPositions):
        # check if car is in area of parking, if tes add area to parkingPositions
        # check if point inside area
        for coord in self.__parkingAreas:
            poly = Polygon(coord)
            p1 = Point(x, y)
            p2 = Point(x + w, y)
            p3 = Point(x, y + h)
            p4 = Point(x + w, y + h)
            if p1.within(poly) and p2.within(poly) and p3.within(poly) and p4.within(poly):
                potentialParkingPositions.append([x, y, w, h])


    # Draw on main window all Parking areas
    def __drawParkingAreas(self, img):
        for pos in self.__parkingAreas:
            size = len(pos)
            for i in range(size):
                cv2.line(img, pos[i % size], pos[(i + 1) % size], (255, 0, 255), 2)


    # Draw Parking Positions
    def __drawParkingPositions(self, img, occupied_flags=None):
     for idx, (x, y, w, h) in enumerate(self.__parkingPositions):
        if occupied_flags:
            color = OCCUPIED_COLOR if occupied_flags[idx] else FREE_COLOR
        else:
            color = (0, 191, 255)  # прежний жёлтый
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)


    # Parking positions detection algorithm
    def detectionAlgorithm(self):
        while True:
            ret, frame = self.__cap.read()
            if not ret or frame is None or frame.size == 0:
                print("Ошибка: кадр не получен, пустой или с нулевыми размерами")
                continue
            else:
                view_frame = frame.copy()

                occupied_flags = [False] * len(self.__parkingPositions)

                potentialParkingPositions = []

                imgBlur = cv2.GaussianBlur(frame, (51, 51), 2)
                imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
                mask = self.__object_detector.apply(imgGray)
                _, mask = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)
                kernel = np.ones((5, 5), np.uint8)
                imgDilate = cv2.dilate(mask, kernel, iterations=2)

                self.__drawParkingPositions(view_frame, occupied_flags)
                self.__drawParkingAreas(view_frame)

                contours, _ = cv2.findContours(imgDilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                print(f"Найдено контуров: {len(contours)}")
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    (x, y, w, h) = cv2.boundingRect(cnt)
                    print(f"Контур: x={x}, y={y}, w={w}, h={h}, area={area}")
                    if area > 800:
                        if self.__addPotentialParkingPositions(x, y, w, h, potentialParkingPositions):
                            cv2.rectangle(view_frame, (x, y), (x + w, y + h), OCCUPIED_COLOR, 2)
                            cv2.putText(view_frame, str(area), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                
                                # --------------------- вычисляем занятость ---------------------
                occupied_flags = []                      # True / False для каждого слота
                for sx, sy, sw, sh in self.__parkingPositions:
                    # центр слота
                    slot_center = Point(sx + sw / 2, sy + sh / 2)
                    busy = False
                    # проверяем, попала ли хоть одна машина в слот
                    for cx, cy, cw, ch in potentialParkingPositions:
                        car_center = Point(cx + cw / 2, cy + ch / 2)
                        # достаточно, чтобы центры были близко (быстро) или
                        # чтобы car-прямоугольник пересёкся со slot-прямоугольником (надёжнее)
                        if slot_center.distance(car_center) < max(sw, sh)/4:
                            busy = True
                            break
                    occupied_flags.append(busy)


                self.__tracker.update(potentialParkingPositions)
                newParkingPositions = self.__tracker.getOptimalParkingPositions()
                print(f"Потенциальные позиции: {potentialParkingPositions}")
                print(f"Оптимальные позиции: {newParkingPositions}")
                if len(newParkingPositions) > 0:
                    for pos in newParkingPositions:
                        if pos not in self.__parkingPositions:
                            self.__parkingPositions.append(pos)
                            self.__db.addParkingPosition(pos[0], pos[1], pos[2], pos[3])
                            print("Добавлено парковочное место:", pos)

                cv2.imshow("marked", view_frame)
                cv2.setMouseCallback("marked", self.__deleteByClick)

                key = cv2.waitKey(1)
                if key == ord('p'):
                    self.__markParkingArea(frame)
                if key == ord('q'):
                    break