def blur(self,image,bi):
    kernel=(self.bi,self.bi)
    image = cv2.blur(self.image,kernel)
    return image
