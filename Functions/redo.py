def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack.pop())
            self.image = self.undo_stack[-1]
            self.setPhoto(self.image)
            self.undo_stack.pop()
