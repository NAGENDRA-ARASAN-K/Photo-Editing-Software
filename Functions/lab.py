def lab(self,image):
    image = cv2.cvtColor(self.image, cv2.COLOR_BGR2LAB)
    return image
