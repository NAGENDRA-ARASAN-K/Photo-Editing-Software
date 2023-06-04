def insert(self):
        self.filename=QFileDialog.getOpenFileName(filter='Image (*.*)')[0]
        self.image=cv2.imread(self.filename)
        self.undo_stack.append(self.image)
        self.setPhoto(self.image)
