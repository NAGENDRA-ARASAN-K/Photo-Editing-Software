def bac(self,image,ci,bri):
        adjusted_image = cv2.convertScaleAbs(self.image, alpha=(self.bri)*0.1,beta=self.ci)
        return adjusted_image
