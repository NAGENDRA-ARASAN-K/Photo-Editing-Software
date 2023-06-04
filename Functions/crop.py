def crop(self,image):
        def fit_image_to_window(image, window_size):
            height, width = image.shape[:2]
            window_width, window_height = window_size
            scale = min(window_width / width, window_height / height)
            resized_image = cv2.resize(image, (int(width * scale), int(height * scale)))
            return resized_image

        print('hi')
        window_size=800,600
        fit_imag=imutils.resize(image,height=1200,width=700)
        print(type(fit_imag))
        pygame.init()
        screen = pygame.display.set_mode((700, 600))
        fit_imag = pygame.surfarray.make_surface(fit_imag)
        crop_rect = pygame.Rect(0, 0, 0, 0)
        cropping=False
        running=True
        while running:
          for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
              if event.button==pygame.BUTTON_LEFT:
                cropping=True
                crop_rect.topleft = event.pos
                print(crop_rect.topleft)
            elif event.type==pygame.MOUSEBUTTONUP:
              if event.button == pygame.BUTTON_LEFT:

                print(crop_rect.width,crop_rect.height)
                cropping = False
                running=False
          if cropping:
            crop_rect.width = pygame.mouse.get_pos()[0] - crop_rect.x
            crop_rect.height = pygame.mouse.get_pos()[1] - crop_rect.y
          screen.fill((0,0,0))
          
          screen.blit(fit_imag,(0,0))
          pygame.draw.rect(screen, (255, 0, 0), crop_rect, 2)
          pygame.display.flip()
        cropped_image = pygame.Surface((crop_rect.width, crop_rect.height))
        cropped_image.blit(fit_imag, (0, 0), crop_rect)
        cropped_screen = pygame.display.set_mode((crop_rect.width, crop_rect.height))
        cropped_screen.blit(cropped_image, (0, 0))
        pygame.display.flip()
        pygame.quit()
        return cropped_image
