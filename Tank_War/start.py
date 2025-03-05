import sys
import pygame
from  Tank_War import scene,My_Tank,Enemy_Tank,home
import main

# 变量设置
# 该关卡坦克总数量
EnemyTanks_Total = 8
# 场上可以存在的敌方坦克总数量
EnemyTanks_Now_Max = 4


# 结束界面显示
def show_end_interface(screen, width, height, is_win):
    # 返回主菜单
    restart = main.Main()
    bg_img = pygame.image.load("Tank_War/images/others/background.png")
    screen.blit(bg_img, (0, 0))
    if is_win:
        fail_img = pygame.image.load("Tank_War/images/others/youwin.png")
        rect = fail_img.get_rect()
        rect.midtop = (width / 2, height / 2)
        screen.blit(fail_img, rect)
    else:
        fail_img = pygame.image.load("Tank_War/images/others/gameover.png")
        rect = fail_img.get_rect()
        rect.midtop = (width / 2, height / 2)
        screen.blit(fail_img, rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                restart.start_interface()
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_ESCAPE]:
            pygame.quit()
            restart.start_interface()

# 主函数
def _main():
    # 初始化
    pygame.init()
    screen = pygame.display.set_mode((630, 630))
    # 设置窗口的标题
    pygame.display.set_caption('TankWar（按shift启动坦克）（wasd j 控制）')
    # 加载图片
    bg_img = pygame.image.load("Tank_War/images/others/background.png")
    # 关卡
    F_map = 0
    # 游戏是否结束
    is_gameover = False
    # 时钟
    clock = pygame.time.Clock()
    #返回主菜单
    restart = main.Main()
    # 主循环
    while not is_gameover:
        # 关卡
        F_map += 1
        if F_map != 1:
            break
        # 该关卡坦克总数量
        enemytanks_total = EnemyTanks_Total
        # 场上任何时刻存在的敌方坦克总数量
        enemytanks_now = 0
        # 场上可以存在的敌方坦克总数量
        enemytanks_now_max = EnemyTanks_Now_Max
        # 精灵组
        tanksGroup = pygame.sprite.Group()
        mytanksGroup = pygame.sprite.Group()
        enemytanksGroup = pygame.sprite.Group()
        enemybulletsGroup = pygame.sprite.Group()
        # 自定义事件
        #     -生成敌方坦克事件
        genEnemyEvent = pygame.constants.USEREVENT + 0
        pygame.time.set_timer(genEnemyEvent, 100)
        #     -敌方坦克静止恢复事件
        recoverEnemyEvent = pygame.constants.USEREVENT + 1
        pygame.time.set_timer(recoverEnemyEvent, 8000)
        # 关卡地图
        map_f = scene.Map(F_map)
        # 我方坦克
        tank_player = My_Tank.myTank()
        tanksGroup.add(tank_player)
        mytanksGroup.add(tank_player)
        is_switch_tank = True
        player_moving = False
        # 为了轮胎的动画效果
        time = 0
        # 敌方坦克
        for i in range(0, 3):
            if enemytanks_total > 0:
                enemytank = Enemy_Tank.enemyTank(i)
                tanksGroup.add(enemytank)
                enemytanksGroup.add(enemytank)
                enemytanks_now += 1
                enemytanks_total -= 1
        # 大本营
        myhome = home.Home()
        # 出场特效
        appearance_img = pygame.image.load("Tank_War/images/others/appear.png").convert_alpha()
        appearances = []
        appearances.append(appearance_img.subsurface((0, 0), (48, 48)))
        appearances.append(appearance_img.subsurface((48, 0), (48, 48)))
        appearances.append(appearance_img.subsurface((96, 0), (48, 48)))
        # 关卡主循环
        while True:
            if is_gameover is True:
                break
            if enemytanks_total < 1 and enemytanks_now < 1:
                is_gameover = False
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    restart.start_interface()
                if event.type == genEnemyEvent:
                    if enemytanks_total > 0:
                        if enemytanks_now < enemytanks_now_max:
                            enemytank = Enemy_Tank.enemyTank()
                            if not pygame.sprite.spritecollide(
                                    enemytank, tanksGroup, False, None):
                                tanksGroup.add(enemytank)
                                enemytanksGroup.add(enemytank)
                                enemytanks_now += 1
                                enemytanks_total -= 1
                if event.type == recoverEnemyEvent:
                    for each in enemytanksGroup:
                        each.can_move = True
            # 检查用户键盘操作
            key_pressed = pygame.key.get_pressed()
            # 玩家一
            if key_pressed[pygame.K_w]:
                tanksGroup.remove(tank_player)
                tank_player.move_up(tanksGroup, map_f.brickGroup, map_f.ironGroup, myhome)
                tanksGroup.add(tank_player)
                player_moving = True
            elif key_pressed[pygame.K_s]:
                tanksGroup.remove(tank_player)
                tank_player.move_down(tanksGroup, map_f.brickGroup, map_f.ironGroup, myhome)
                tanksGroup.add(tank_player)
                player_moving = True
            elif key_pressed[pygame.K_a]:
                tanksGroup.remove(tank_player)
                tank_player.move_left(tanksGroup, map_f.brickGroup, map_f.ironGroup, myhome)
                tanksGroup.add(tank_player)
                player_moving = True
            elif key_pressed[pygame.K_d]:
                tanksGroup.remove(tank_player)
                tank_player.move_right(tanksGroup, map_f.brickGroup, map_f.ironGroup, myhome)
                tanksGroup.add(tank_player)
                player_moving = True
            elif key_pressed[pygame.K_j]:
                if not tank_player.bullet.live:
                    tank_player.shoot()
            elif key_pressed[pygame.K_ESCAPE]:
                pygame.quit()
                restart.start_interface()

            # 背景
            screen.blit(bg_img, (0, 0))
            # 石头墙
            for each in map_f.brickGroup:
                screen.blit(each.brick, each.rect)
            # 钢墙
            for each in map_f.ironGroup:
                screen.blit(each.iron, each.rect)
            time += 1
            if time == 5:
                time = 0
                is_switch_tank = not is_switch_tank
            # 我方坦克
            if tank_player in mytanksGroup:
                if is_switch_tank and player_moving:
                    screen.blit(
                        tank_player.tank_0,
                        (tank_player.rect.left, tank_player.rect.top))
                    player_moving = False
                else:
                    screen.blit(
                        tank_player.tank_1,
                        (tank_player.rect.left, tank_player.rect.top))

            # 敌方坦克
            for each in enemytanksGroup:
                # 出生特效
                if each.born:
                    if each.times > 0:
                        each.times -= 1
                        if each.times <= 10:
                            screen.blit(appearances[2],
                                        (3 + each.x * 12 * 24, 3))
                        elif each.times <= 20:
                            screen.blit(appearances[1],
                                        (3 + each.x * 12 * 24, 3))
                        elif each.times <= 30:
                            screen.blit(appearances[0],
                                        (3 + each.x * 12 * 24, 3))
                        elif each.times <= 40:
                            screen.blit(appearances[2],
                                        (3 + each.x * 12 * 24, 3))
                        elif each.times <= 50:
                            screen.blit(appearances[1],
                                        (3 + each.x * 12 * 24, 3))
                        elif each.times <= 60:
                            screen.blit(appearances[0],
                                        (3 + each.x * 12 * 24, 3))
                        elif each.times <= 70:
                            screen.blit(appearances[2],
                                        (3 + each.x * 12 * 24, 3))
                        elif each.times <= 80:
                            screen.blit(appearances[1],
                                        (3 + each.x * 12 * 24, 3))
                        elif each.times <= 90:
                            screen.blit(appearances[0],
                                        (3 + each.x * 12 * 24, 3))
                    else:
                        each.born = False
                else:
                    if is_switch_tank:
                        screen.blit(each.tank_0,
                                    (each.rect.left, each.rect.top))
                    else:
                        screen.blit(each.tank_1,
                                    (each.rect.left, each.rect.top))
                    if each.can_move:
                        tanksGroup.remove(each)
                        each.move(tanksGroup, map_f.brickGroup,
                                  map_f.ironGroup, myhome)
                        tanksGroup.add(each)
            # 我方子弹
            for tank_player in mytanksGroup:
                if tank_player.bullet.live:
                    tank_player.bullet.move()
                    screen.blit(tank_player.bullet.bullet,
                                tank_player.bullet.rect)
                    # 子弹碰撞敌方子弹
                    for each in enemybulletsGroup:
                        if each.live:
                            if pygame.sprite.collide_rect(
                                    tank_player.bullet, each):
                                tank_player.bullet.live = False
                                each.live = False
                                enemybulletsGroup.remove(each)
                                break
                        else:
                            enemybulletsGroup.remove(each)
                    # 子弹碰撞敌方坦克
                    for each in enemytanksGroup:
                        if each.live:
                            if pygame.sprite.collide_rect(tank_player.bullet, each):
                                enemytanksGroup.remove(each)
                                tanksGroup.remove(each)
                                enemytanks_now -= 1
                                each.reload()
                                tank_player.bullet.live = False
                                break
                        else:
                            enemytanksGroup.remove(each)
                            tanksGroup.remove(each)
                    # 子弹碰撞石头墙
                    for each in map_f.brickGroup:
                        if pygame.sprite.collide_rect(tank_player.bullet, each):
                            tank_player.bullet.live = False
                            each.live = False
                            map_f.brickGroup.remove(each)
                            break

                    # 子弹碰钢墙
                    for each in map_f.ironGroup:
                        if pygame.sprite.collide_rect(tank_player.bullet, each):
                            tank_player.bullet.live = False

                    # 子弹碰大本营
                    if pygame.sprite.collide_rect(tank_player.bullet, myhome):
                        tank_player.bullet.live = False
                        myhome.set_dead()
                        is_gameover = True
            # 敌方子弹
            for each in enemytanksGroup:
                if each.live:
                    if each.can_move and not each.bullet.live:
                        enemybulletsGroup.remove(each.bullet)
                        each.shoot()
                        enemybulletsGroup.add(each.bullet)
                    if not each.born:
                        if each.bullet.live:
                            each.bullet.move()
                            screen.blit(each.bullet.bullet, each.bullet.rect)
                            # 子弹碰撞我方坦克
                            for tank_player in mytanksGroup:
                                if pygame.sprite.collide_rect(
                                        each.bullet, tank_player):
                                    tank_player.life -= 1
                                    if tank_player.life < 1:
                                        mytanksGroup.remove(tank_player)
                                        tanksGroup.remove(tank_player)
                                        if len(mytanksGroup) < 1:
                                            is_gameover = True
                                    else:
                                        tank_player.reset()
                                    each.bullet.live = False
                                    enemybulletsGroup.remove(each.bullet)
                                    break
                            # 子弹碰撞石头墙
                            if pygame.sprite.spritecollide(each.bullet, map_f.brickGroup, True, None):
                                each.bullet.live = False
                                enemybulletsGroup.remove(each.bullet)

                            # 子弹碰钢墙
                            if pygame.sprite.spritecollide(each.bullet, map_f.ironGroup, False, None):
                                each.bullet.live = False

                            # 子弹碰大本营
                            if pygame.sprite.collide_rect(each.bullet, myhome):
                                each.bullet.live = False
                                myhome.set_dead()
                                is_gameover = True
                else:
                    enemytanksGroup.remove(each)
                    tanksGroup.remove(each)
            # 家
            screen.blit(myhome.home, myhome.rect)
            # 时钟
            pygame.display.flip()
            clock.tick(60)
    if not is_gameover:
        show_end_interface(screen, 630, 630, True)
    else:
        show_end_interface(screen, 630, 630, False)

if __name__ == '__main__':
    main()
