import pygame, time, main, random
from os import path

FPS = 300
BulletNum = 30

color1 = (0, 0, 0)
color2 = (255, 255, 255)
color3 = (60, 60, 60)

character_speed = 5
enemy_1_speed = 1
enemy_2_speed = 2
enemy_3_speed = 3
enemy_4_speed = 1
enemy_5_speed = 1

enemies_total = 10

character_hp = 3

screen_width = 1920
screen_height = 1000

cha_bullet_speed_1 = 3
cha_bullet_speed_2 = 2
cha_bullet_speed_3 = 10
ene_bullet_speed = 5

highest_score_file = "PlaneWar/飞机大战/highest_score.txt"


class Screen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()


class Enemy(Screen):
    def __init__(self, path, rotation, scale):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.rotozoom(self.image, rotation, scale)
        self.rect = self.image.get_rect()
        self.live =True


class Enemy1(Enemy):
    def __init__(self):
        super().__init__('PlaneWar/飞机大战/敌人1.png', 180, 0.5)
        self.points = 10
        self.speed = enemy_1_speed
        self.rect.x = random.randint(0, screen_width - (int)(0.5 * 200))
        self.hp = 1

    def update(self):
        self.rect.y += self.speed


class Enemy2(Enemy):
    def __init__(self):
        super().__init__('PlaneWar/飞机大战/敌人2.png', 180, 0.75)
        self.points = 15
        self.speed = enemy_2_speed
        self.rect.x = random.randint(500, screen_width - 500 - 1 * 200)
        self.num = 0
        self.change = 1
        self.hp = 2

    def update(self):
        if not self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            if self.num % 3 == 0: self.rect.y += self.speed
            if self.num % 50 == 0: self.rect.y += self.speed
            if self.num % 25 == 0:
                self.rect.x += self.speed * self.num * self.change
                self.change *= -1
            if self.num == 500: self.num = 0
        else:
            self.rect.y += self.speed
        self.num += 1


class Enemy3(Enemy):
    def __init__(self):
        super().__init__('PlaneWar/飞机大战/敌人3.png', 180, 0.5)
        self.points = 15
        self.speed = enemy_3_speed
        self.rect.x = random.randint(0, screen_width - (int)(0.5 * 200))
        self.el, self.er = False, True
        self.hp = 2

    def update(self):
        if self.rect.right >= self.screen_rect.right:
            self.el, self.er = True, False
            self.rect.y += 400
        elif self.rect.left <= 0:
            self.el, self.er = False, True
            self.rect.y += 400
        if self.rect.left > 0 and self.el:
            self.rect.x -= self.speed
        if self.rect.right < self.screen_rect.right and self.er:
            self.rect.x += self.speed


class Enemy4(Enemy):
    def __init__(self):
        super().__init__('PlaneWar/飞机大战/敌人4.png', 180, 0.3)
        self.points = 15
        self.speed = enemy_4_speed
        self.rect.x = random.randint(0, screen_width - (int)(0.3 * 200))
        self.change = random.choice([1, -1])
        self.hp = 1

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.change
        if self.rect.right >= self.screen_rect.right:
            self.change *= -1
        elif self.rect.left <= 0:
            self.change *= -1


class Enemy5(Enemy):
    def __init__(self):
        super().__init__('PlaneWar/飞机大战/敌人5.png', 180, 1)
        self.points = 20
        self.speed = enemy_5_speed
        self.rect.x = random.randint(0, screen_width - (int)(1 * 200))
        self.num = 0
        self.bullets = pygame.sprite.Group()
        self.hp = 4

    def update(self):
        self.fire_switch = True
        self.rect.y += self.speed

class EnemyBoss(Enemy):
    def __init__(self):
        super().__init__('PlaneWar/飞机大战/敌人boss.png', 0, 1.5)
        self.points = 40
        self.speed = 1
        self.rect.midtop = self.screen_rect.midtop
        self.rect.y+=60
        self.hp = 20
        self.num=0
        self.el, self.er = False, True
        self.range=200

    def update(self):
        if self.rect.x+150 >= screen_width/2+self.range:
            self.el, self.er = True, False
        elif self.rect.x+150 <= screen_width/2-self.range:
            self.el, self.er = False, True
        if self.el:
            self.rect.x -= self.speed
        if self.er:
            self.rect.x += self.speed


class EnemyManager(Screen):
    def __init__(self):
        super().__init__()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies_count = 0
        self.born_time = 0
        self.born_gap = random.randint(80, 180)
        # self.enemy_list = [Enemy5]
        self.enemy_list = [Enemy1, Enemy2, Enemy3, Enemy4, Enemy5]
        self.enemy_type = random.choice(self.enemy_list)
        self.enemy = self.enemy_type
        self.num = 0
        self.boss_open=False

    def update(self):
        if not self.boss_open:
            if not self.enemies:
                self.enemy = self.enemy_type()
                self.enemies.add(self.enemy)
            if self.born_time >= self.born_gap and self.enemies_count < enemies_total:
                self.enemy_type = random.choice(self.enemy_list)
                self.enemy = self.enemy_type()
                self.enemies.add(self.enemy)
                self.born_time = 0
                self.enemies_count += 1
            if self.enemy.points == 20:
                self.enemy_bullet_update()
        else:
            self.boss_open=False
            if not self.enemies:
                self.enemy=EnemyBoss()
                self.enemies.add(self.enemy)
                self.enemies_count+=enemies_total
                if self.enemy.hp==0:
                    self.enemies.empty()
                    self.enemies_count=0

        self.born_time += 1
        self.enemies.update()

    def enemy_bullet_update(self):
        if self.num % 50 == 0:
            bullet = EnemyBullet(self.enemy)
            self.bullets.add(bullet)
            self.bullets.update()
            self.num = 0
        self.num += 1

    def restart(self):
        self.enemies_count = 0
        self.born_time = 0
        self.born_gap = random.randint(80, 180)
        self.enemy = self.enemy_type


class Character(Screen):
    def __init__(self, path, scale):
        super().__init__()
        self.image = pygame.image.load(path)
        self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.rect = self.image.get_rect()
        self.speed = character_speed
        self.mleft, self.mright, self.mup, self.mdown, self.fire = False, False, False, False, False
        self.HP = character_hp
        self.bullets = pygame.sprite.Group()
        self.num = 0
        self.fire_kind = 1
        self.live=True

    def update(self):
        if self.fire and len(self.bullets) < BulletNum:
            if self.fire_kind == 1 :
                if self.num % 50 == 0:
                    bullet1 = CharacterBullet1(self)
                    self.bullets.add(bullet1)
                if self.num % 120 == 0:
                    bullet2 = CharacterBullet2(self,1)
                    bullet3 = CharacterBullet2(self,-1)
                    self.bullets.add(bullet2,bullet3)
                    self.num = 0
            elif self.fire_kind == 2 and self.num % 3 == 0:
                bullet = CharacterBullet1(self)
                self.bullets.add(bullet)
                self.num = 0
            elif self.fire_kind == 3 and self.num % 50 == 0:
                bullet = CharacterBullet3(self)
                self.bullets.add(bullet)
                self.num = 0
        if self.mleft and self.rect.left > 0:
            self.rect.x -= character_speed
        if self.mright and self.rect.right < self.screen_rect.right:
            self.rect.x += character_speed
        if self.mup and self.rect.top > 0:
            self.rect.y -= character_speed
        if self.mdown and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += character_speed
        self.num += 1

class CharacterBullet(pygame.sprite.Sprite):
    def __init__(self, plane,x=10,y=10):
        super().__init__()
        self.rect = pygame.Rect(0, 0, x, y)
        self.rect.midbottom = plane.rect.midtop
        self.live = False

class CharacterBullet1(CharacterBullet):
    def __init__(self, plane):
        super().__init__(plane,10,25)
    def update(self):
        self.rect.y -= cha_bullet_speed_1

class CharacterBullet2(CharacterBullet):
    def __init__(self, plane,direction):
        super().__init__(plane)
        self.direction = direction
    def update(self):
        self.rect.y -= cha_bullet_speed_2
        self.rect.x -= cha_bullet_speed_2*self.direction

class CharacterBullet3(CharacterBullet):
    def __init__(self, plane):
        super().__init__(plane,130,10)
    def update(self):
        self.rect.y -= cha_bullet_speed_3

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 10, 25)
        self.rect.midtop = enemy.rect.midbottom

    def update(self):
        self.rect.y += ene_bullet_speed


class Info:
    def __init__(self, text):
        self.font = pygame.font.SysFont('fangsong', 40, True)
        self.str_image = self.font.render(text, True, color3)
        self.str_rect = self.str_image.get_rect()


class App(Screen):
    def __init__(self):
        super().__init__()
        pygame.init()
        pygame.init()

        self.score = 0
        self.highest_score = 0
        self.level = 1

        self.enemy_manager = EnemyManager()

        self.plane_group = pygame.sprite.Group()
        self.plane = Character('PlaneWar/飞机大战/飞机.png', 0.5)
        self.plane.rect.midbottom = self.screen_rect.midbottom
        self.plane_group.add(self.plane)

        self.play_font = pygame.font.SysFont('fangsong', 90, True)
        self.play_image = self.play_font.render('开始', True, color1)
        self.play_rect = self.play_image.get_rect()
        self.play_rect.center = self.screen_rect.center

        self.mouse_pos = None
        self.start = False

        self.clock = pygame.time.Clock()

        self.restart = main.Main()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('游戏已结束')
                pygame.quit()
                self.restart.start_interface()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = pygame.mouse.get_pos()
                if self.play_rect.collidepoint(self.mouse_pos):
                    self.start = True
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_w | pygame.K_UP:
                        self.plane.mup = True
                    case pygame.K_a | pygame.K_LEFT:
                        self.plane.mleft = True
                    case pygame.K_s | pygame.K_DOWN:
                        self.plane.mdown = True
                    case pygame.K_d | pygame.K_RIGHT:
                        self.plane.mright = True
                    case pygame.K_SPACE:
                        self.plane.fire = True
                    case pygame.K_RETURN:
                        self.start = True
                    case pygame.K_ESCAPE:
                        print('游戏已结束')
                        pygame.quit()
                        self.restart.start_interface()
                    case pygame.K_TAB:
                        if self.plane.fire_kind==1:
                            self.plane.fire_kind = 2
                        elif  self.plane.fire_kind==2:
                            self.plane.fire_kind = 3
                        elif  self.plane.fire_kind==3:
                            self.plane.fire_kind = 1

            elif event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_w | pygame.K_UP:
                        self.plane.mup = False
                    case pygame.K_a | pygame.K_LEFT:
                        self.plane.mleft = False
                    case pygame.K_s | pygame.K_DOWN:
                        self.plane.mdown = False
                    case pygame.K_d | pygame.K_RIGHT:
                        self.plane.mright = False
                    case pygame.K_SPACE:
                        self.plane.fire = False

    def plane_die(self):
        self.plane.HP -= 1
        self.plane.rect.midbottom = self.screen_rect.midbottom
        time.sleep(0.5)

    def plane_hp(self):
        plane_list = pygame.sprite.Group()
        if self.start == True:
            for num in range(1, self.plane.HP + 1):
                love = pygame.sprite.Sprite()
                love.image = pygame.image.load('PlaneWar/飞机大战/血.png')
                love.image = pygame.transform.rotozoom(love.image, 0, 0.25)
                love.rect = love.image.get_rect()
                love.rect.x = screen_width - num * 50 - 25

                love.rect.y = 25
                plane_list.add(love)
            plane_list.draw(self.screen)

    def restart_game3(self):
        self.plane.HP = 3
        self.plane.bullets.empty()
        self.enemy_manager.enemies.empty()
        self.start = False
        self.plane.fire_kind=1
        self.enemy_manager.bullets.empty()

    def collision(self):
        for each in self.enemy_manager.enemies:
            if each.live:
                co1 =pygame.sprite.groupcollide(self.plane.bullets,self.enemy_manager.enemies,True,False)
                if each.hp>0 and co1:
                    each.hp-=1
                    if each.hp == 0:
                        self.enemy_manager.enemies.remove(each)
                        for item in co1.values():
                            self.score += self.enemy_manager.enemy.points * len(item)

        if pygame.sprite.spritecollideany(self.plane, self.enemy_manager.enemies):
            self.plane_die()

        if pygame.sprite.groupcollide(self.plane_group, self.enemy_manager.bullets, False, True):
            self.plane.HP -= 1

        for enemy in self.enemy_manager.enemies:
            if enemy.rect.bottom >= self.screen_rect.bottom:
                self.restart_game3()

        if self.enemy_manager.enemies_count == enemies_total:
            if not self.enemy_manager.enemies:
                self.enemy_manager.restart()
                self.enemy_manager.update()
                self.enemy_manager.enemies.draw(self.screen)
                self.level += 1

    def update_score(self):
        self.highest_score_str = Info('最高分：' + str(self.highest_score))
        self.highest_score_str.str_rect = pygame.Rect(0, 0, 1800, 40)
        self.score_str = Info('分数：' + str(self.score))
        self.score_str.str_rect = pygame.Rect(0, 40, 1800, 40)
        self.level_str = Info('关卡：' + str(self.level))
        self.level_str.str_rect = pygame.Rect(0, 80, 1800, 40)
        self.tab_str = Info('按Tab更换攻击方式')
        self.tab_str.str_rect.midtop = self.screen_rect.midtop

        self.screen.blit(self.highest_score_str.str_image, self.highest_score_str.str_rect)
        self.screen.blit(self.score_str.str_image, self.score_str.str_rect)
        self.screen.blit(self.level_str.str_image, self.level_str.str_rect)
        self.screen.blit(self.tab_str.str_image, self.tab_str.str_rect)

    def update_bullets(self):
        for bullet in self.plane.bullets:
            pygame.draw.rect(self.screen, color1, bullet.rect)
            bullet.update()
            if bullet.rect.bottom < 0:
                self.plane.bullets.remove(bullet)
        for bullet in self.enemy_manager.bullets:
            pygame.draw.rect(self.screen, color1, bullet.rect)
            bullet.update()
            if bullet.rect.bottom > self.screen_rect.bottom:
                self.enemy_manager.bullets.remove(bullet)

    def update_enemies(self):
        self.enemy_manager.update()
        self.enemy_manager.enemies.draw(self.screen)

    def update_high_score(self):
        self.highest_score = self.get_high_score()
        if self.score > self.highest_score:
            with open(highest_score_file, "w") as file:
                file.write(str(self.score))

    def get_high_score(self):
        if path.exists(highest_score_file):
            with open(highest_score_file, "r") as file:
                high_score = int(file.read())
        return high_score

    def level_change(self):
        if self.level == 3:
            self.enemy_manager.boss_open=True
        else:
            self.enemy_manager.boss_open=False


    def run(self):
        while True:
            self.get_high_score()
            self.clock.tick(FPS)
            self.screen.fill(color2)
            self.events()

            if self.plane.HP > 0 and self.start:
                self.screen.blit(self.plane.image, self.plane.rect)
                self.level_change()
                self.plane.update()
                self.update_enemies()
                self.update_bullets()
                self.update_score()
                self.collision()
            else:
                self.screen.blit(self.play_image, self.play_rect)
                self.score = 0
                self.level = 1
                self.restart_game3()

            self.plane_hp()

            self.update_high_score()
            pygame.display.update()


if __name__ == '__main__':
    app = App()
    app.run()

# 某君新认识一网友。当问及年龄时，他的网友说：“我的年龄是个2位数，我比儿子大27岁,如果把我的年龄的两位数字交换位置，刚好就是我儿子的年龄”，请输出网友年龄所有的可能情况，每个年龄数字为一行，只输出年龄数字即可，输出结果
