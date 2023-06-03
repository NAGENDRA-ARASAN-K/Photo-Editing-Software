def rgb(self,image):
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        return image
