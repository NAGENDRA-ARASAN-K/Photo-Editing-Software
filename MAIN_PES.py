from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage, QIcon
from tkinter.filedialog import asksaveasfilename
import imutils
import cv2
import pygame
import numpy as np


class Ui_MainWindow(object):

    def insert(self):
        self.filename = QFileDialog.getOpenFileName(
            filter='Image (*.png *.jpg *.jpeg *.bmp*)'
            )[0]
        if self.filename:
            self.image = cv2.imread(self.filename)
            self.undo_stack.append(self.image)
            self.setPhoto(self.image)

    def setPhoto(self, image, s=False):
        self.tmp = image
        image = imutils.resize(image, height=1200, width=700)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0],
                       frame.strides[0], QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
        self.undo_stack.append(self.image)
        if s:
            self.undo_stack.append(self.tmp)

    def show_color_palette(self):
        if self.image is not None:
            pygame.init()
            palette_width = 240
            palette_height = 240
            color_box_size = 20
            columns = 12
            colors = [
                (255, 0, 0), (0, 255, 0), (0, 0, 255),
                (255, 255, 0), (255, 0, 255), (0, 255, 255),
                (128, 0, 0), (0, 128, 0), (0, 0, 128),
                (128, 128, 0), (128, 0, 128), (0, 128, 128),
                (255, 255, 255), (0, 0, 0), (128, 128, 128),
                (255, 128, 0), (255, 192, 203), (255, 99, 71),
                (210, 105, 30), (128, 0, 128)
            ]

            for r in range(5):
                for g in range(5):
                    for b in range(5):
                        if (r, g, b) not in colors:
                            colors.append((r * 51, g * 51, b * 51))
            colors.sort()

            palette_surface = pygame.Surface((palette_width, palette_height))
            palette_surface.fill((255, 255, 255))

            screen = pygame.display.set_mode((palette_width, palette_height))
            pygame.display.set_caption('Color Palette')
            index = None

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse_pos = pygame.mouse.get_pos()
                            column = mouse_pos[0] // color_box_size
                            row = mouse_pos[1] // color_box_size
                            index = row * columns + column

                for i, color in enumerate(colors):
                    x = (i % columns) * color_box_size
                    y = (i // columns) * color_box_size
                    pygame.draw.rect(palette_surface, color,
                                     (x, y, color_box_size, color_box_size))
                screen.blit(palette_surface, (0, 0))
                pygame.display.flip()
            pygame.quit()
            if index is not None:
                self.draw_on_image(self.brush, colors[index])

        def draw_on_image(self, brush_size, brush_colour):
            self.image = cv2.resize(self.image, (1200, 800))
            drawing = False
            last_x, last_y = -1, -1

            def draw_circle(event, x, y, flags, param):
                nonlocal drawing, last_x, last_y
                if event == cv2.EVENT_LBUTTONDOWN:
                    drawing = True
                    last_x, last_y = x, y
                elif event == cv2.EVENT_LBUTTONUP:
                    drawing = False
                elif event == cv2.EVENT_MOUSEMOVE:
                    if drawing:
                        if brush_size:
                            cv2.circle(self.image,
                                       (x, y), brush_size, (brush_colour[2],
                                                            brush_colour[1],
                                                            brush_colour[0]),
                                       -1)
                            cv2.line(self.image, (last_x, last_y),
                                     (x, y), (brush_colour[2],
                                              brush_colour[1],
                                              brush_colour[0]), brush_size)
                            last_x, last_y = x, y

            cv2.namedWindow('Image - Press Enter to Confirm Changes')
            cv2.setMouseCallback('Image - Press Enter to Confirm Changes',
                                 draw_circle)

            while True:
                cv2.imshow('Image - Press Enter to Confirm Changes',
                           self.image)
                key = cv2.waitKey(1) & 0xFF
                if key == 13:
                    self.setPhoto(self.image)
                    cv2.destroyAllWindows()
                    break

    def crop(self, image):
        pygame.init()
        screen = pygame.display.set_mode((1200, 1000))
        fit_imag = self.image
        fit_imag = np.swapaxes(fit_imag, 1, 0)
        fit_imag = cv2.cvtColor(fit_imag, cv2.COLOR_BGR2RGB)
        fit_imag = pygame.surfarray.make_surface(fit_imag)
        fit_imag = pygame.transform.scale(fit_imag, (1200, 1000))
        crop_rect = pygame.Rect(0, 0, 0, 0)
        cropping = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        cropping = True
                        crop_rect.topleft = event.pos
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == pygame.BUTTON_LEFT:
                        cropping = False
                        running = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    return fit_imag

            if cropping:
                crop_rect.width = pygame.mouse.get_pos()[0] - crop_rect.x
                crop_rect.height = pygame.mouse.get_pos()[1] - crop_rect.y
            screen.fill((0, 0, 0))
            screen.blit(fit_imag, (0, 0))
            pygame.draw.rect(screen, (255, 0, 0), crop_rect, 2)
            pygame.display.flip()

        if crop_rect.width <= 0 or crop_rect.height <= 0:
            pygame.quit()
            return fit_imag

        cropped_image = pygame.Surface((crop_rect.width, crop_rect.height))
        cropped_image.blit(fit_imag, (0, 0), crop_rect)
        cropped_screen = pygame.display.set_mode((crop_rect.width,
                                                  crop_rect.height))
        cropped_screen.blit(cropped_image, (0, 0))
        pygame.display.flip()
        pygame.quit()
        return cropped_image

    def zoom_and_pan(self, image):
        if self.image is not None:
            pygame.init()
            screen_width, screen_height = 800, 600
            screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("Pan")
            fit_imag = imutils.resize(self.image, height=1200, width=900)
            fit_imag = np.swapaxes(fit_imag, 1, 0)
            fit_imag = cv2.cvtColor(fit_imag, cv2.COLOR_BGR2RGB)
            image = pygame.surfarray.make_surface(fit_imag)
            width, height = image.get_size()
            scale_factor = 1.0
            image_rect = image.get_rect()
            image_x, image_y = 0, 0

            is_panning = False
            start_x, start_y = 0, 0

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            is_panning = True
                            start_x, start_y = event.pos
                        elif event.button == 4:  # Mouse wheel scroll up
                            scale_factor *= 1.1

                        elif event.button == 5:  # Mouse wheel scroll down
                            scale_factor *= 0.9

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:  # Left mouse button
                            is_panning = False

                    elif event.type == pygame.MOUSEMOTION:
                        if is_panning:
                            dx = event.pos[0] - start_x
                            dy = event.pos[1] - start_y
                            start_x, start_y = event.pos

                            image_x += dx
                            image_y += dy

                screen.fill((0, 0, 0, 0))
                new_width = int(image_rect.width * scale_factor)
                new_height = int(image_rect.height * scale_factor)
                scaled_image = pygame.transform.scale(image,
                                                      (new_width, new_height))

                # Calculate the position to center the image on the screen
                pan_x = (screen_width - new_width) // 2 + image_x
                pan_y = (screen_height - new_height) // 2 + image_y

                screen.blit(scaled_image, (pan_x, pan_y))
                pygame.display.flip()

    def fliplr(self, image):
        image = cv2.flip(image, 1)
        return image

    def flipud(self, image):
        image = cv2.flip(self.image, 0)
        return image

    def clockrotate(self, image):
        image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        return image

    def counterclockrotate(self, image):
        image = cv2.rotate(self.image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return image

    def grayscale(self, image):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return image

    def hsv(self, image):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        return image

    def rgb(self, image):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        return image

    def lab(self, image):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
        return image

    def blur(self, image, bi):
        kernel = (self.bi, self.bi)
        image = cv2.blur(self.image, kernel)
        return image

    def bac(self, image, ci, bri):
        adjusted_image = cv2.convertScaleAbs(
            self.image, alpha=(self.bri)*0.1, beta=self.ci)
        return adjusted_image

    def saturate(self, image, si):
        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)
        s = cv2.multiply(s, (self.si)*0.1)
        s = np.clip(s, 0, 255)
        hsv_image = cv2.merge((h, s, v))
        saturated_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        saturated_image = cv2.convertScaleAbs(saturated_image)
        return saturated_image

    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.image = self.undo_stack[-1]
            self.setPhoto(self.image)
            self.undo_stack.pop()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack.pop())
            self.image = self.undo_stack[-1]
            self.setPhoto(self.image)
            self.undo_stack.pop()

    def brushsize(self, brush):
        self.brush = brush

    def updatecrop(self, image):
        if self.image is not None:
            self.image = self.tmp
            self.image = self.crop(self.image)
            self.image = pygame.surfarray.array3d(self.image)
            self.image = np.swapaxes(self.image, 1, 0)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.setPhoto(self.image)

    def updateflr(self, image):
        if self.image is not None:
            self.image = self.tmp
            self.image = self.fliplr(self.image)
            self.setPhoto(self.image)

    def updatefud(self, image):
        if self.image is not None:
            self.image = self.tmp
            self.image = self.flipud(self.image)
            self.setPhoto(self.image)

    def updatecrot(self, image):
        if self.image is not None:
            self.image = self.tmp
            self.image = self.clockrotate(self.image)
            self.setPhoto(self.image)

    def updateccrot(self, image):
        if self.image is not None:
            self.image = self.tmp
            self.image = self.counterclockrotate(self.image)
            self.setPhoto(self.image)

    def updategray(self, image):
        if self.image is not None:
            try:
                self.image = self.tmp
                self.image = self.grayscale(self.image)
                self.setPhoto(self.image)
            except Exception:
                print("Can't apply Grayscale on Current Image ")

    def updatehsv(self, image):
        if self.image is not None:
            try:
                self.image = self.tmp
                self.image = self.hsv(self.image)
                self.setPhoto(self.image)
            except Exception:
                print("Can't apply HSV on Current Image ")

    def updatergb(self, image):
        if self.image is not None:
            try:
                self.image = self.tmp
                self.image = self.rgb(self.image)
                self.setPhoto(self.image)
            except Exception:
                print("Can't apply RGB on Current Image ")

    def updatelab(self, image):
        if self.image is not None:
            try:
                self.image = self.tmp
                self.image = self.lab(self.image)
                self.setPhoto(self.image)
            except Exception:
                print("Can't apply LAB on Current Image ")

    def updatebac(self):
        if self.image is not None:
            self.tmp = self.image
            self.tmp = self.bac(self.image, self.ci, self.bri)
            self.setPhoto(self.tmp, True)

    def brindex(self, bri):
        self.bri = bri
        self.updatebac()

    def cindex(self, ci):
        self.ci = ci
        self.updatebac()

    def updatesaturation(self):
        if self.image is not None:
            self.tmp = self.image
            self.tmp = self.saturate(self.image, self.si)
            self.setPhoto(self.tmp, True)

    def sindex(self, si):
        self.si = si
        self.updatesaturation()

    def updateblur(self):
        if self.image is not None:
            self.tmp = self.image
            self.tmp = self.blur(self.image, self.bi)
            self.setPhoto(self.tmp, True)

    def bindex(self, bi):
        self.bi = bi
        self.updateblur()

    def save(self):
        if self.image is not None:
            cv2.imwrite(self.filename, self.tmp)

    def save_as(self):
        if self.image is not None:
            self.newfilename = asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
            if self.newfilename:
                cv2.imwrite(self.newfilename, self.tmp)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1662, 951)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.undoButton = QtWidgets.QToolButton(self.centralwidget)
        self.undoButton.clicked.connect(self.undo)
        self.undoButton.setGeometry(QtCore.QRect(50, 820, 62, 62))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Icon/Undo Icon.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.undoButton.setIcon(icon)
        self.undoButton.setIconSize(QtCore.QSize(62, 62))
        self.undoButton.setObjectName("undoButton")
        self.redoButton = QtWidgets.QToolButton(self.centralwidget)
        self.redoButton.clicked.connect(self.redo)
        self.redoButton.setGeometry(QtCore.QRect(130, 820, 62, 62))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Icon/Redo Icon.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.redoButton.setIcon(icon1)
        self.redoButton.setIconSize(QtCore.QSize(62, 62))
        self.redoButton.setObjectName("redoButton")
        self.cropButton = QtWidgets.QToolButton(self.centralwidget)
        self.cropButton.setGeometry(QtCore.QRect(10, 200, 102, 102))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../Icon/Crop Icon.jpeg"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cropButton.setIcon(icon2)
        self.cropButton.setIconSize(QtCore.QSize(160, 80))
        self.cropButton.setObjectName("cropButton")
        self.cropButton.clicked.connect(self.updatecrop)
        self.zapButton = QtWidgets.QToolButton(self.centralwidget)
        self.zapButton.setGeometry(QtCore.QRect(130, 200, 102, 102))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../Icon/Zoom and Pan Icon.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zapButton.setIcon(icon3)
        self.zapButton.setIconSize(QtCore.QSize(102, 102))
        self.zapButton.setObjectName("zapButton")
        self.zapButton.clicked.connect(self.zoom_and_pan)
        self.flrButton = QtWidgets.QToolButton(self.centralwidget)
        self.flrButton.clicked.connect(self.updateflr)
        self.flrButton.setGeometry(QtCore.QRect(10, 320, 102, 102))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../Icon/Flip.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.flrButton.setIcon(icon4)
        self.flrButton.setIconSize(QtCore.QSize(102, 102))
        self.flrButton.setObjectName("flrButton")
        self.fudButton = QtWidgets.QToolButton(self.centralwidget)
        self.fudButton.clicked.connect(self.updatefud)
        self.fudButton.setGeometry(QtCore.QRect(130, 320, 102, 102))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../Icon/FlipUD.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fudButton.setIcon(icon5)
        self.fudButton.setIconSize(QtCore.QSize(102, 102))
        self.fudButton.setObjectName("fudButton")
        self.rotateantiButton = QtWidgets.QToolButton(self.centralwidget)
        self.rotateantiButton.clicked.connect(self.updateccrot)
        self.rotateantiButton.setGeometry(QtCore.QRect(130, 440, 102, 102))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("../Icon/rotationanti.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rotateantiButton.setIcon(icon6)
        self.rotateantiButton.setIconSize(QtCore.QSize(90, 90))
        self.rotateantiButton.setObjectName("rotateantiButton")
        self.rotateclockButton = QtWidgets.QToolButton(self.centralwidget)
        self.rotateclockButton.clicked.connect(self.updatecrot)
        self.rotateclockButton.setGeometry(QtCore.QRect(10, 440, 102, 102))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("../Icon/rotaioncl.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rotateclockButton.setIcon(icon7)
        self.rotateclockButton.setIconSize(QtCore.QSize(90, 90))
        self.rotateclockButton.setObjectName("rotateclockButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 10, 1401, 791))
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 560, 231, 241))
        font = QtGui.QFont()
        font.setFamily("Poor Richard")
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet(
            '''border-color: qlineargradient(spread:pad, x1:0, y1:0,
                                             x2:1, y2:0,
                                             stop:0 rgba(0, 0, 0, 255),
                                             stop:1 rgba(255, 255,
                                                         255, 255));''')
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.grayButton = QtWidgets.QPushButton(self.tab)
        self.grayButton.clicked.connect(self.updategray)
        self.grayButton.setGeometry(QtCore.QRect(30, 10, 161, 31))
        self.grayButton.setObjectName("grayButton")
        self.hsvButton = QtWidgets.QPushButton(self.tab)
        self.hsvButton.clicked.connect(self.updatehsv)
        self.hsvButton.setGeometry(QtCore.QRect(30, 60, 161, 31))
        self.hsvButton.setObjectName("hsvButton")
        self.rgbButton = QtWidgets.QPushButton(self.tab)
        self.rgbButton.clicked.connect(self.updatergb)
        self.rgbButton.setGeometry(QtCore.QRect(30, 110, 161, 31))
        self.rgbButton.setObjectName("rgbButton")
        self.labButton = QtWidgets.QPushButton(self.tab)
        self.labButton.clicked.connect(self.updatelab)
        self.labButton.setGeometry(QtCore.QRect(30, 160, 161, 31))
        self.labButton.setObjectName("labButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.toolBox = QtWidgets.QToolBox(self.tab_2)
        self.toolBox.setGeometry(QtCore.QRect(0, 0, 221, 201))
        font = QtGui.QFont()
        font.setFamily("Poor Richard")
        font.setPointSize(11)
        self.toolBox.setFont(font)
        self.toolBox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.toolBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.toolBox.setObjectName("toolBox")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 219, 99))
        self.page.setObjectName("page")
        self.brightnessSlider = QtWidgets.QSlider(self.page)
        self.brightnessSlider.setMinimum(1)
        self.brightnessSlider.setMaximum(25)
        self.brightnessSlider.setValue(10)
        self.brightnessSlider.valueChanged.connect(self.brindex)
        self.brightnessSlider.setGeometry(QtCore.QRect(0, 0, 211, 31))
        self.brightnessSlider.setOrientation(QtCore.Qt.Horizontal)
        self.brightnessSlider.setObjectName("brightnessSlider")
        self.toolBox.addItem(self.page, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 219, 99))
        self.page_2.setObjectName("page_2")
        self.contrastSlider = QtWidgets.QSlider(self.page_2)
        self.contrastSlider.setMinimum(-127)
        self.contrastSlider.setMaximum(127)
        self.contrastSlider.setValue(0)
        self.contrastSlider.valueChanged.connect(self.cindex)
        self.contrastSlider.setGeometry(QtCore.QRect(0, 0, 211, 31))
        self.contrastSlider.setOrientation(QtCore.Qt.Horizontal)
        self.contrastSlider.setObjectName("contrastSlider")
        self.toolBox.addItem(self.page_2, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 219, 99))
        self.page_3.setObjectName("page_3")
        self.saturationSlider = QtWidgets.QSlider(self.page_3)
        self.saturationSlider.setMinimum(0)
        self.saturationSlider.setMaximum(70)
        self.saturationSlider.setValue(10)
        self.saturationSlider.valueChanged.connect(self.sindex)
        self.saturationSlider.setGeometry(QtCore.QRect(0, 0, 211, 31))
        self.saturationSlider.setOrientation(QtCore.Qt.Horizontal)
        self.saturationSlider.setObjectName("saturationSlider")
        self.toolBox.addItem(self.page_3, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 219, 99))
        self.page_4.setObjectName("page_4")
        self.blurSlider = QtWidgets.QSlider(self.page_4)
        self.blurSlider.setMinimum(1)
        self.blurSlider.setMaximum(50)
        self.blurSlider.setValue(1)
        self.blurSlider.valueChanged.connect(self.bindex)
        self.blurSlider.setGeometry(QtCore.QRect(0, 0, 211, 31))
        self.blurSlider.setOrientation(QtCore.Qt.Horizontal)
        self.blurSlider.setObjectName("blurSlider")
        self.toolBox.addItem(self.page_4, "")
        self.tabWidget.addTab(self.tab_2, "")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 221, 171))
        font = QtGui.QFont()
        font.setFamily("Poor Richard")
        font.setPointSize(18)
        self.groupBox.setFont(font)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(80, 90, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.brushSlider = QtWidgets.QSlider(self.groupBox)
        self.brushSlider.valueChanged.connect(self.brushsize)
        self.brushSlider.setGeometry(QtCore.QRect(10, 130, 201, 31))
        self.brushSlider.setOrientation(QtCore.Qt.Horizontal)
        self.brushSlider.setObjectName("brushSlider")
        self.colourButton = QtWidgets.QPushButton(self.groupBox)
        self.colourButton.setGeometry(QtCore.QRect(50, 40, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.colourButton.setFont(font)
        self.colourButton.setObjectName("colourButton")
        self.colourButton.clicked.connect(self.show_color_palette)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 41, 41))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("../Icon/brush1.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1662, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.triggered.connect(self.insert)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.triggered.connect(self.save)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.triggered.connect(self.save_as)
        self.actionSave_As.setObjectName("actionSave_As")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.toolBox.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.filename = None
        self.newfilename = None
        self.tmp = None
        self.image = None
        self.bri = 1
        self.ci = 10
        self.si = 0
        self.bi = 0
        self.brush = 0
        self.undo_stack = []
        self.redo_stack = []

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow",
                                             "Photo Editing Software"))
        MainWindow.setWindowIcon(QIcon(
            'C:/Users/nikhi/Desktop/CS Project - V2/Icon/brush1.png'))
        self.undoButton.setText(_translate("MainWindow", "..."))
        self.undoButton.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.redoButton.setText(_translate("MainWindow", "..."))
        self.redoButton.setShortcut(_translate("MainWindow", "Ctrl+Shift+Z"))
        self.cropButton.setText(_translate("MainWindow", "..."))
        self.zapButton.setText(_translate("MainWindow", "..."))
        self.flrButton.setText(_translate("MainWindow", "..."))
        self.fudButton.setText(_translate("MainWindow", "..."))
        self.rotateantiButton.setText(_translate("MainWindow", "..."))
        self.rotateclockButton.setText(_translate("MainWindow", "..."))
        self.grayButton.setText(_translate("MainWindow", "GRAYSCALE"))
        self.hsvButton.setText(_translate("MainWindow", "HSV"))
        self.rgbButton.setText(_translate("MainWindow", "RGB"))
        self.labButton.setText(_translate("MainWindow", "LAB"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),
                                  _translate("MainWindow", "FILTERS"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page),
                                 _translate("MainWindow", "BRIGHTNESS"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2),
                                 _translate("MainWindow", "CONTRAST"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3),
                                 _translate("MainWindow", "SATURATION"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4),
                                 _translate("MainWindow", "BLUR"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  _translate("MainWindow", "ADJUST"))
        self.groupBox.setTitle(_translate("MainWindow", "BRUSH "))
        self.label_2.setText(_translate("MainWindow", "SIZE"))
        self.colourButton.setText(_translate("MainWindow", "COLOUR"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionSave_As.setShortcut(_translate("MainWindow",
                                                  "Ctrl+Shift+S"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
