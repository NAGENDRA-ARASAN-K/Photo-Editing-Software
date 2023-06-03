 def setPhoto(self,image,s=False):
        self.tmp=image
        image=imutils.resize(image,height=1200,width=700)
        frame=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image=QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
        self.undo_stack.append(self.image)
        if s:
            self.undo_stack.append(self.tmp)
