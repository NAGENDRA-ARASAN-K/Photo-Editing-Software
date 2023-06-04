def show_color_palette(self):
        pygame.init()
        palette_width = 240
        palette_height = 240
        color_box_size = 20
        rows = 12
        columns = 12
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),  # Red, Green, Blue
            (255, 255, 0), (255, 0, 255), (0, 255, 255),  # Yellow, Magenta, Cyan
            (128, 0, 0), (0, 128, 0), (0, 0, 128),  # Maroon, Green, Navy
            (128, 128, 0), (128, 0, 128), (0, 128, 128),  # Olive, Purple, Teal
            (255, 255, 255), (0, 0, 0), (128, 128, 128),  # White, Black, Gray
            (255, 128, 0), (255, 192, 203), (255, 99, 71),  # Orange, Pink, Tomato
            (210, 105, 30), (128, 0, 128)  # Chocolate, Purple
        ]

        for r in range(5):
            for g in range(5):
                for b in range(5):
                  if (r, g, b) not in colors:
                    colors.append((r * 51, g * 51, b * 51))
        colors.sort()

        palette_surface = pygame.Surface((palette_width, palette_height))
        palette_surface.fill((255, 255, 255))

        screen = pygame.display.set_mode((palette_width, palette_height))
        pygame.display.set_caption('Color Palette')

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        column = mouse_pos[0] // color_box_size
                        row = mouse_pos[1] // color_box_size
                        index = row * columns + column


            for i, color in enumerate(colors):
                x = (i % columns) * color_box_size
                y = (i // columns) * color_box_size
                pygame.draw.rect(palette_surface, color, (x, y, color_box_size, color_box_size))
                    
            screen.blit(palette_surface, (0, 0))
            pygame.display.flip()
        print(colors[index])

        pygame.quit()
        print('hi')
        self.draw_on_image(self.brush,colors[index])
        print('hi')




    def draw_on_image(self,brush_size,brush_colour):
        self.image=self.tmp
        drawing = False
        last_x, last_y = -1, -1

        def draw_circle(event, x, y, flags, param):
      
            nonlocal drawing, last_x, last_y

            if event == cv2.EVENT_LBUTTONDOWN:
                drawing = True
                last_x, last_y = x, y
            elif event == cv2.EVENT_LBUTTONUP:
                drawing = False
            elif event == cv2.EVENT_MOUSEMOVE:
                if drawing:
                    cv2.circle(self.image, (x, y), brush_size,(brush_colour[2],brush_colour[1],brush_colour[0]), -1)
                    cv2.line(self.image, (last_x, last_y), (x, y), (brush_colour[2],brush_colour[1],brush_colour[0]), brush_size)
                    last_x, last_y = x, y


        cv2.namedWindow('Image')
        cv2.setMouseCallback('Image', draw_circle)

        while True:
            window_size=800,600
            cv2.imshow('Image', self.image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.setPhoto(self.image)
                cv2.destroyAllWindows()
                break
