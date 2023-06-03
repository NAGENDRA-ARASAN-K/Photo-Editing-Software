def clockrotate(self,image):
        image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        return image
