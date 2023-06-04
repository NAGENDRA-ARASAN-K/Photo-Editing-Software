def saturate(self,image,si):
        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)
        s = cv2.multiply(s, (self.si)*0.1)
        s = np.clip(s, 0, 255)
        hsv_image = cv2.merge((h, s, v))
        saturated_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        saturated_image = cv2.convertScaleAbs(saturated_image)
        return saturated_image
