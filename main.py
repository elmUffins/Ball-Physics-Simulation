import pygame

pygame.init()
pygame.mixer.init()
pygame.font.init()

pygame.display.set_caption("Ball Physics Simulation")
screen = pygame.display.set_mode((800, 600))
running = True

#Attributes for the ball
circle_pos = pygame.Vector2(400, 300)
circle_vel = pygame.Vector2(2, 5)
circle_acc = pygame.Vector2(0, 0.5)
vel_decay = 0.005
circle_radius = 20
bounce_sound = pygame.mixer.Sound("Bounce.wav")

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock() #Allows to control the frame rate

#Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    circle_vel += circle_acc
    circle_vel *= 1 - vel_decay
    circle_pos += circle_vel

    #Logic for wall collision
    if circle_pos.x - circle_radius < 0 or circle_pos.x + circle_radius > 800:
        if circle_vel.x > 0.15:
            circle_vel.x += -0.1
        circle_vel.x *= -1
        bounce_sound.play()
    if circle_pos.y - circle_radius < 0 or circle_pos.y + circle_radius > 600:
        circle_vel.y *= -1
        if circle_vel.y > 0.5 or circle_vel.y < -0.5:
            bounce_sound.play()
        if circle_pos.y - circle_radius < 0:
            circle_pos.y = circle_radius
        else:
            circle_pos.y = 600 - circle_radius
    if circle_vel.y < 0.026 and circle_vel.x < 0.01 and circle_vel.x > 0: # If the ball is almost stopped - It's not as smooth as desired, but works
        circle_vel.y = 0

    #Logic for booster collision
    if circle_pos.x + circle_radius >= 770 and circle_pos.y + circle_radius >= 590:
        if circle_vel.x > 0:
            circle_vel.x += 4
        else:
            circle_vel.x += -4
        circle_vel.y += -10
    if circle_pos.x - circle_radius <= 30 and circle_pos.y + circle_radius >= 590:
        if circle_vel.x > 0:
            circle_vel.x += 4
        else:
            circle_vel.x += -4
        circle_vel.y += -10

    #Logic for clicking
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    if mouse_click == (1, 0, 0):
        circle_vel.y = -10
        if circle_vel.x > 0:
            circle_vel.x += 1
        else:
            circle_vel.x += -1

    screen.fill((0, 0, 0))

    pSurface = font.render(f"Position: {circle_pos}", True, (255, 255, 255))
    vSurface = font.render(f"Velocity: {circle_vel}", True, (255, 255, 255))
    screen.blit(pSurface, (10, 10))
    screen.blit(vSurface, (10, 46))
    pygame.draw.circle(screen, (255, 0, 0), circle_pos, circle_radius)
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 800, 600.5), 1)
    boosterR = pygame.draw.rect(screen, (0, 255, 255), (770, 590, 25, 10))
    boosterL = pygame.draw.rect(screen, (0, 255, 255), (5, 590, 25, 10))

    pygame.display.flip()
    clock.tick(60) #Frame rate