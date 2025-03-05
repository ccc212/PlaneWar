import pygame, sys, time

pygame.init()

FPS = 300
BulletNum = 15

color1 = (0, 0, 0)
color2 = (255, 255, 255)
color3 = (60, 60, 60)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_rect = screen.get_rect()

Plane = pygame.image.load('飞机大战/飞机.png')
plane = pygame.transform.rotozoom(Plane, 0, 0.5)
plane_rect = plane.get_rect()
plane_rect.midbottom = screen_rect.midbottom
plane_speed = 2
mleft, mright, mup, mdown = False, False, False, False

bullets = pygame.sprite.Group()

font = pygame.font.SysFont('fangsong', 40, True)
text = font.render('分数:', True, color3)
text_rect = text.get_rect()

enemies = pygame.sprite.Group()
enemy_1 = pygame.sprite.Sprite()
Enemy_1 = pygame.image.load('飞机大战/敌人1.png')
enemy_1.image = pygame.transform.rotozoom(Enemy_1, 180, 0.5)
enemy_1.rect = enemy_1.image.get_rect()
enemy_1.rect.top = text_rect.bottom
enemy_1_speed = 1
el, er = False, True
enemies.add(enemy_1)

clock = pygame.time.Clock()
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w | pygame.K_UP:
                    mup = True
                case pygame.K_a | pygame.K_LEFT:
                    mleft = True
                case pygame.K_s | pygame.K_DOWN:
                    mdown = True
                case pygame.K_d | pygame.K_RIGHT:
                    mright = True
                case pygame.K_SPACE:
                    if len(bullets) < BulletNum:
                        bullet = pygame.sprite.Sprite()
                        bullet.rect = pygame.Rect(0, 0, 10, 25)
                        bullet.rect.midbottom = plane_rect.midtop
                        bullets.add(bullet)
                case pygame.K_ESCAPE:
                    exit()
        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_w | pygame.K_UP:
                    mup = False
                case pygame.K_a | pygame.K_LEFT:
                    mleft = False
                case pygame.K_s | pygame.K_DOWN:
                    mdown = False
                case pygame.K_d | pygame.K_RIGHT:
                    mright = False

    if mleft and plane_rect.left > 0:
        plane_rect.x -= plane_speed
    if mright and plane_rect.right < screen_rect.right:
        plane_rect.x += plane_speed
    if mup and plane_rect.top > 0:
        plane_rect.y -= plane_speed
    if mdown and plane_rect.bottom < screen_rect.bottom:
        plane_rect.y += plane_speed

    screen.fill(color2)
    screen.blit(plane, plane_rect)
    screen.blit(text, text_rect)

    for bullet in bullets:
        pygame.draw.rect(screen, color1, bullet.rect)
        bullet.rect.y -= 1
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    if enemy_1.rect.right == screen_rect.right:
        el, er = True, False
    elif enemy_1.rect.left == 0:
        el, er = False, True
    if enemy_1.rect.left > 0 and el:
        enemy_1.rect.x -= enemy_1_speed
    if enemy_1.rect.right < screen_rect.right and er:
        enemy_1.rect.x += enemy_1_speed
    enemies.draw(screen)

    pygame.sprite.groupcollide(bullets, enemies, True, True)

    if not enemies:
        enemy_1 = pygame.sprite.Sprite()
        Enemy_1 = pygame.image.load('飞机大战/敌人1.png')
        enemy_1.image = pygame.transform.rotozoom(Enemy_1, 180, 0.5)
        enemy_1.rect = enemy_1.image.get_rect()
        enemy_1.rect.top = text_rect.bottom
        enemies.add(enemy_1)

    # if pygame.sprite.spritecollideany(plane,enemies):
    #     plane_rect.midbottom = screen_rect.midbottom
    #     time.sleep(0.5)

    pygame.display.update()
