def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.image = self.undo_stack[-1]
            self.setPhoto(self.image)
            self.undo_stack.pop()
