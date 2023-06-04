def hsv(self,image):
        image = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        return image
