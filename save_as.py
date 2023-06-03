def save(self):
    cv2.imwrite(self.filename,self.tmp)

def save_as(self):
    self.newfilename=asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
    cv2.imwrite(self.newfilename, self.tmp)
