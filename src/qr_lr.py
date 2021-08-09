# import the pygame module, so you can use it
import pygame
import numpy as np
import numpy.linalg as la
from numpy import pi

def draw_ellipse_angle(surface, color, rect, angle, width=0):
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle/pi*180)
    surface.blit(rotated_surf, rotated_surf.get_rect(center = target_rect.center))

def draw_line_angle(surface, color, start, end, angle, width=1):
    target_rect = pygame.Rect(0,0,WIDTH,HEIGHT)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.line(shape_surf, color, start, end, width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle/pi*180)
    surface.blit(rotated_surf, rotated_surf.get_rect(center = target_rect.center))

def render_multi_line(text, x, y, fsize):
        lines = text.splitlines()
        for i, l in enumerate(lines):
            screen.blit(myfont.render(l, 1, (255,0,0)), (x, y + fsize*i))

def rot(angle):
    return np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]])

# initialize the pygame module
pygame.init()

pygame.display.set_caption("draw LR algorithm")



WIDTH = 480
HEIGHT = 360
centrex = WIDTH // 2
centrey = HEIGHT // 2
semiaxis1 = 100
semiaxis2 = 50
angle = pi/4
# create a surface on screen that has the size of 240 x 180
screen = pygame.display.set_mode((WIDTH,HEIGHT))

# initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
myfont = pygame.font.SysFont("monospace", 15)

instruct_user = True

while instruct_user:
    render_multi_line("""LEFT ARROW rotates clockwise,
RIGHT ARROW rotates counterclockwise,
UP ARROW increases eccentricity,
DOWN ARROW decreases eccentricity.
Press any key to continue...""",
    10,10,20)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            instruct_user = False
        if event.type == pygame.QUIT:
            instruct_user = False
            running = False
            pygame.quit()

running = True

# main loop
while running:

    inputmatrix = rot(angle) @ np.diag((semiaxis1, semiaxis2)) @ rot(-angle)
    L = la.cholesky(inputmatrix)
    lroutputmatrix = L.T @ L
    Q, R = la.qr(inputmatrix)
    adjust_signs = np.diag(np.sign(np.diag(R)))
    Q = Q @ adjust_signs
    R = adjust_signs @ R
    qroutputmatrix = R @ Q
    (qroutsemiaxis1, qroutsemiaxis2), qroutrot = la.eig(qroutputmatrix)
    qroutangle = np.arctan2(qroutrot[1,0],qroutrot[0,0])

    (lroutsemiaxis1, lroutsemiaxis2), lroutrot = la.eig(lroutputmatrix)
    lroutangle = np.arctan2(lroutrot[1,0],lroutrot[0,0])

    screen.fill((255,255,255))
    draw_line_angle(screen,
                    (255,0,0),
                    (centrex, centrey - semiaxis2),
                    (centrex, centrey + semiaxis2),
                    angle,
                    width=2)
    draw_line_angle(screen,
                    (255,0,0),
                    (centrex - semiaxis1, centrey),
                    (centrex + semiaxis1, centrey),
                    angle,
                    width=2)

    draw_line_angle(screen,
                    (0,0,255),
                    (centrex, centrey - qroutsemiaxis2),
                    (centrex, centrey + qroutsemiaxis2),
                    qroutangle,
                    width=2)
    draw_line_angle(screen,
                    (0,0,255),
                    (centrex - qroutsemiaxis1, centrey),
                    (centrex + qroutsemiaxis1, centrey),
                    qroutangle,
                    width=2)

    draw_ellipse_angle(screen,
                       (255,0,0),
                       (centrex - semiaxis1, centrey - semiaxis2,
                        2*semiaxis1, 2*semiaxis2),
                        angle=angle,
                        width=2)
    draw_ellipse_angle(screen,
                       (0,0,255),
                       (centrex - qroutsemiaxis1, centrey - qroutsemiaxis2,
                        2*qroutsemiaxis1, 2*qroutsemiaxis2),
                        angle=qroutangle,
                        width=2)

    draw_line_angle(screen,
                    (0,255,0),
                    (centrex, centrey - lroutsemiaxis2),
                    (centrex, centrey + lroutsemiaxis2),
                    lroutangle,
                    width=2)
    draw_line_angle(screen,
                    (0,255,255),
                    (centrex - lroutsemiaxis1, centrey),
                    (centrex + lroutsemiaxis1, centrey),
                    lroutangle,
                    width=2)

    draw_ellipse_angle(screen,
                       (0,255,0),
                       (centrex - lroutsemiaxis1, centrey - lroutsemiaxis2,
                        2*lroutsemiaxis1, 2*lroutsemiaxis2),
                        angle=lroutangle,
                        width=2)


    label1 = myfont.render("In", 1, (255,0,0))
    screen.blit(label1, (WIDTH - 70, 30))
    label2 = myfont.render("Out QR", 1, (0,0,255))
    screen.blit(label2, (WIDTH - 70, 70))
    label2 = myfont.render("Out LR", 1, (0,255,0))
    screen.blit(label2, (WIDTH - 70, 110))

    pygame.draw.line(screen, (0,0,0), (0,centrey), (WIDTH,centrey))
    pygame.draw.line(screen, (0,0,0), (centrex,0), (centrex,HEIGHT))
    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle += 0.001
    if keys[pygame.K_RIGHT]:
        angle -= 0.001
    if keys[pygame.K_UP]:
        semiaxis2 += 0.01
    if keys[pygame.K_DOWN]:
        semiaxis2 -= 0.01


    # event handling, gets all event from the event queue
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False
            pygame.quit()
