import pygame
import math
import os
from settings import PATH, FPS,PATH2


pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))
#宣告一全域變數
generate_times=0

class Enemy:
    def __init__(self):
        global generate_times
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        self.path_pos = 0
        self.move_count = 0
        self.stride = 1
        #設定不同路徑,並依產生次數決定路徑
        if generate_times>0 and generate_times%2==1:
            self.path=PATH2
        else:
            self.path=PATH
        self.x, self.y = self.path[0]

    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """
        pygame.draw.rect(win, (255, 0, 0), [self.x - self.width // 2, self.y - self.height // 2, self.width, 5])
        pygame.draw.rect(win, (127, 255, 0), [self.x - self.width // 2, self.y - self.height // 2,
                                              (self.health / self.max_health) * self.width, 5])

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """

        ax, ay = self.path[self.path_pos]
        bx, by = self.path[self.path_pos + 1]
        distance_A_B = math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
        max_count = int(distance_A_B / self.stride)  # total footsteps that needed from A to B

        if self.move_count < max_count:
            unit_vector_x = (bx - ax) / distance_A_B
            unit_vector_y = (by - ay) / distance_A_B
            delta_x = unit_vector_x * self.stride
            delta_y = unit_vector_y * self.stride

            # update the coordinate and the counter
            self.x += delta_x
            self.y += delta_y
            self.move_count += 1

        else:
            self.move_count = 0
            self.path_pos += 1



class EnemyGroup:
    def __init__(self):
        # self.generate_times=0
        self.gen_count = 0
        self.gen_period = 120  # (unit: frame)
        self.reserved_members = []
        self.expedition = [Enemy()]  # don't change this line until you do the EX.3

    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """

        if self.gen_count >= self.gen_period and self.reserved_members:
            self.expedition.append(self.reserved_members.pop())
            self.gen_count = 0
        else:
            self.gen_count += 1

    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        self.reserved_members = [Enemy() for i in range(num)]
        #每產生一次,全域變數加1
        global generate_times
        generate_times+=1

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)





