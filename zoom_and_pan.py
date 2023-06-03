def zoom_and_pan(self,image):
        def zoom(scale_factor,screen_width,screen_height,a,b):
          new_width = int(a * scale_factor)
          new_height = int(b * scale_factor)
          scaled_image = pygame.transform.scale(image, (new_width, new_height))
          image_x = (screen_width - new_width) // 2
          image_y = (screen_height - new_height) // 2
          

        def pan_image():
            pygame.init()

            screen_width, screen_height = 800, 600
            screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("Pan")
            image = pygame.surfarray.make_surface(self.image)
            width, height = image.get_size()

            # Create a new surface with transposed dimensions
            #transposed_surface = pygame.Surface((height, width))

            # Transpose the surface by blitting pixels onto the new surface with transposed coordinates
            '''for x in range(width):
                for y in range(height):
                    pixel = surface.get_at((x, y))  # Get the pixel color from the original surface
                    transposed_surface.set_at((y, x), pixel)'''
            scale_factor = 1.0
            #image =transposed_surface
            image_rect = image.get_rect()
            image_x, image_y = 0, 0

            is_panning = False
            start_x, start_y = 0, 0

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button
                            is_panning = True
                            start_x, start_y = event.pos
                        elif event.button == 4:  # Mouse wheel scroll up
                            scale_factor *= 1.1
                            
                        elif event.button == 5:  # Mouse wheel scroll down
                            scale_factor *= 0.9
                            
                        

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:  # Left mouse button
                            is_panning = False

                    elif event.type == pygame.MOUSEMOTION:
                        if is_panning:
                            dx = event.pos[0] - start_x
                            dy = event.pos[1] - start_y
                            start_x, start_y = event.pos

                            image_x += dx
                            image_y += dy
                
                screen.fill((0,0,0,0))
                new_width = int(image_rect.width * scale_factor)
                new_height = int(image_rect.height * scale_factor)
                scaled_image = pygame.transform.scale(image, (new_width, new_height))

                # Calculate the position to center the image on the screen
                pan_x = (screen_width - new_width) // 2 + image_x
                pan_y = (screen_height - new_height) // 2 + image_y

                screen.blit(scaled_image, (pan_x, pan_y))
                pygame.display.flip()
        pan_image()
