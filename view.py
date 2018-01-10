import pygame
from point3d import Point3d

WIDTH  = 800
HEIGHT = 600

RED = pygame.Color(255,0,0)
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)

BACKGROUND = pygame.Color('black')
POINT_COLOR = pygame.Color(200,200,200,255)
EDGE_COLOR  = pygame.Color(100,150,255,255)
POINT_RADIUS = 3
EDGE_WIDTH = 1

ORIGIN = Point3d()
CENTER = Point3d(WIDTH/2., HEIGHT/2., 0)

CAM_MOVE_RATE   = 0.2
CAM_ROTATE_RATE = 0.01

TEST_POINTS = [
    Point3d(-100,-100,-100),Point3d(100,-100,-100),Point3d(100,100,-100),Point3d(-100,100,-100),
    Point3d(-100,-100,100),Point3d(100,-100,100),Point3d(100,100,100),Point3d(-100,100,100)
]



class View:
    def __init__(self):
        self.width  = WIDTH
        self.height = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.axis_x = Point3d(100, 0, 0)
        self.axis_y = Point3d(0, 100, 0)
        self.axis_z = Point3d(0, 0, 100)
        self.cam_center = Point3d(CENTER)
        self.cam_pitch  = 0.0
        self.cam_yaw = 0.0

    def run(self):
        while self.running:
            key_pressed = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    # print event.key
                    pass 

            if key_pressed[pygame.K_ESCAPE]:
                self.running = False
            if key_pressed[pygame.K_UP]:
                self.cam_center.y += CAM_MOVE_RATE
            if key_pressed[pygame.K_DOWN]:
                self.cam_center.y -= CAM_MOVE_RATE
            if key_pressed[pygame.K_RIGHT]:
                self.cam_center.x -= CAM_MOVE_RATE
            if key_pressed[pygame.K_LEFT]:
                self.cam_center.x += CAM_MOVE_RATE
            if key_pressed[pygame.K_w]:
                self.cam_pitch += CAM_ROTATE_RATE
            if key_pressed[pygame.K_s]:
                self.cam_pitch -= CAM_ROTATE_RATE
            if key_pressed[pygame.K_a]:
                self.cam_yaw += CAM_ROTATE_RATE
            if key_pressed[pygame.K_d]:
                self.cam_yaw -= CAM_ROTATE_RATE

            self.screen.fill(BACKGROUND)
            self.display()
            pygame.display.flip()

    def convert(self, point):
        """Gets a 3d point in the space and converts to a 2d point in the screen"""
        # print "-----------"
        # print "converting", point
        new_point = Point3d(point)
        # print "rotating in", self.cam_pitch
        new_point.rotateX(self.cam_pitch)
        # print "got", new_point
        new_point.rotateY(self.cam_yaw)

        # print "inverting y"
        new_point.y *= -1
        # print "got", new_point
        # print "now translating in", self.cam_center
        new_point += self.cam_center
        # print "got", new_point
        return (int(new_point.x), int(new_point.y))

    def display(self):
        # display X axis
        pygame.draw.aaline(
            self.screen, RED,
            self.convert(ORIGIN),
            self.convert(self.axis_x), EDGE_WIDTH)
        # display Y axis
        pygame.draw.aaline(
            self.screen, GREEN,
            self.convert(ORIGIN),
            self.convert(self.axis_y), EDGE_WIDTH)
        # display Z axis
        pygame.draw.aaline(
            self.screen, BLUE,
            self.convert(ORIGIN),
            self.convert(self.axis_z), EDGE_WIDTH)
        # testing cube
        for p in TEST_POINTS:
            pygame.draw.circle(self.screen,BLUE, self.convert(p),5)
        for i in range(3):
            pygame.draw.aaline(
                self.screen, pygame.Color('grey'),
                self.convert(TEST_POINTS[i]),
                self.convert(TEST_POINTS[i+1]), EDGE_WIDTH)
        pygame.draw.aaline(
                self.screen, pygame.Color('grey'),
                self.convert(TEST_POINTS[3]),
                self.convert(TEST_POINTS[0]), EDGE_WIDTH)
        for i in range(4,7):
            pygame.draw.aaline(
                self.screen, pygame.Color('grey'),
                self.convert(TEST_POINTS[i]),
                self.convert(TEST_POINTS[i+1]), EDGE_WIDTH)
        pygame.draw.aaline(
                self.screen, pygame.Color('grey'),
                self.convert(TEST_POINTS[-1]),
                self.convert(TEST_POINTS[4]), EDGE_WIDTH)
        for i in range(4):
            pygame.draw.aaline(
                self.screen, pygame.Color('grey'),
                self.convert(TEST_POINTS[i]),
                self.convert(TEST_POINTS[i+4]), EDGE_WIDTH)



if __name__ == '__main__':
    view = View()
    view.run()

