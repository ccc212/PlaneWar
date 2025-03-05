import pygame,random,main

block_size = 30
board_edge_x = 10
board_edge_y = 10
board_width = 10
board_height = 20
block_offset = 2    #方块间隔

red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (255, 0, 255)
cyan_blue = (0, 255, 255)
gray = (100, 100, 100)

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.arr = [[None for i in range(4)] for j in range(4)]
        self.TetrominoType = random.randint(0, 6)
        match self.TetrominoType:
            case 0:
                self.arr[1][1] = Block(red)  # 0000
                self.arr[2][1] = Block(red)  # 0##0
                self.arr[2][2] = Block(red)  # 00##
                self.arr[3][2] = Block(red)  # 0000
            case 1:
                self.arr[2][1] = Block(green)  # 0000
                self.arr[3][1] = Block(green)  # 00##
                self.arr[1][2] = Block(green)  # 0##0
                self.arr[2][2] = Block(green)  # 0000
            case 2:
                self.arr[2][0] = Block(blue)  # 00#0
                self.arr[2][1] = Block(blue)  # 00#0
                self.arr[2][2] = Block(blue)  # 0##0
                self.arr[1][2] = Block(blue)  # 0000
            case 3:
                self.arr[1][1] = Block(yellow)  # 0000
                self.arr[1][2] = Block(yellow)  # 0##0
                self.arr[2][1] = Block(yellow)  # 0##0
                self.arr[2][2] = Block(yellow)  # 0000
            case 4:
                self.arr[1][0] = Block(white)  # 0#00
                self.arr[1][1] = Block(white)  # 0#00
                self.arr[1][2] = Block(white)  # 0##0
                self.arr[2][2] = Block(white)  # 0000
            case 5:
                self.arr[1][1] = Block(purple)  # 0000
                self.arr[0][2] = Block(purple)  # 0#00
                self.arr[1][2] = Block(purple)  # ###0
                self.arr[2][2] = Block(purple)  # 0000
            case 6:
                self.arr[0][1] = Block(cyan_blue)  # 0000
                self.arr[1][1] = Block(cyan_blue)  # ####
                self.arr[2][1] = Block(cyan_blue)  # 0000
                self.arr[3][1] = Block(cyan_blue)  # 0000

    def _get_rotated_array(self):
        _rotated = [[None for i in range(4)] for j in range(4)]
        for x in range(4):
            for y in range(4):
                _rotated[x][3- y] = self.arr[y][x]
        return _rotated

    def rotate(self):
        self.arr = self._get_rotated_array()

    #检查旋转后的俄罗斯方块是否与边界或已有方块重叠
    def checkangle(self, arr):
        if self.TetrominoType == 3:
            return False
        _rotated = self._get_rotated_array()
        for i in range(4):
            for j in range(4):
                if _rotated[j][i] is not None:
                    if self.y + i >= board_height or j + self.x < 0 or j + self.x >= board_width:
                        return False
                    else:
                        if arr[j + self.x][i + self.y] is not None:
                            return False
        return True

    def move(self, x, y):
        self.x += x
        self.y += y

    # 检查移动后的俄罗斯方块是否与边界或已有方块重叠
    # -1到达底部和重合，0不能移动，1是正常的
    def check_move(self, x, y, arr):
        for i in range(4):
            for j in range(4):
                if self.arr[j][i] is not None:
                    if self.y + i + y >= board_height:
                        return -1
                    else:
                        if arr[j + self.x][i + self.y + y] is not None:
                            return -1

                    if j + x + self.x < 0 or j + x + self.x >= board_width:
                        return 0
                    else:
                        if arr[j + self.x + x][i + self.y] is not None:
                            return 0
        return 1

    def render(self, display):
        for x in range(4):
            for y in range(4):
                if self.arr[x][y] is not None:
                    self.arr[x][y].x = self.x + x
                    self.arr[x][y].y = self.y + y
                    self.arr[x][y].render(display, block_size)


class Board:
    def __init__(self):
        self.arr = [[None for i in range(board_height)] for j in range(board_width)]
        self._current_piece = None
        self._next_piece = None
        self._points = 0
        self._font = pygame.font.SysFont('fangsong', 36,True)
        self._point_text = self._font.render('分数', True, white)
        self._tetris = False    #是否消除
        self.lost = False   #是否结束
        self._frame_block = Block()     #边框方块

    def render(self, display):
        # 绘制游戏元素
        for x in range(board_width):
            for y in range(board_height):
                # 绘制方块
                if self.arr[x][y] is not None:
                    self.arr[x][y].render(display, block_size)

        # 绘制下一个方块和当前方块
        self._next_piece.render(display)
        self._current_piece.render(display)

        for i in range(board_width):
            # 绘制上边框
            self._frame_block.y = -1
            self._frame_block.x = i
            self._frame_block.render(display, block_size)
            # 绘制下边框
            self._frame_block.y = board_height
            self._frame_block.render(display, block_size)

        for i in range(-1, board_height + 1):
            # 绘制左边框
            self._frame_block.x = -1
            self._frame_block.y = i
            self._frame_block.render(display, block_size)
            # 绘制右边框
            self._frame_block.x = board_width
            self._frame_block.render(display, block_size)

        # 绘制得分信息
        display.blit(self._point_text, (440, 300))
        points = self._font.render(str(self._points), True, white)
        display.blit(points, (460, 350))

    def _move_blocks_down(self, y, arr):
        for i in range(y):
            for x in range(board_width):
                if arr[x][i] is not None:
                    self._move(0, 1, arr[x][i])

    def _move(self, x, y, block):
        self.arr[block.x + x][block.y + y] = block
        self.arr[block.x][block.y] = None
        block.x += x
        block.y += y

    def _delete_whole_lines(self):
        _deleted_lines = 0  #计算删除的行数
        for y in range(board_height):
            _full_line = True
            for x in range(board_width):
                if self.arr[x][y] is None:
                    _full_line = False
                    break
            if _full_line:
                _deleted_lines += 1
                for x in range(board_width):
                    self.arr[x][y] = None
                self._move_blocks_down(y, self.arr)
        self._points += _deleted_lines * 100
        if _deleted_lines == 4:
            self._points += 400
            if self._tetris:
                self._points += 400
            else:
                self._tetris = True
        else:
            self._tetris = False

    #将指定的方块插入到游戏板的指定位置
    def _insert(self, x, y, piece):
        self._current_piece = piece
        self._current_piece.y = y
        self._current_piece.x = x

    def start_game(self):
        self._next_piece = Tetromino(12, 2)
        self._create_new_piece()

    #创建新的当前方块并更新下一个方块
    def _create_new_piece(self):
        self._next_piece.x = int(board_width / 2)
        self._next_piece.y = 0
        if self._next_piece.check_move(0, 0, self.arr) == -1:
            self.lost = True
        else:
            self._delete_whole_lines()
            self._insert(int(board_width / 2), 0, self._next_piece)
            self._next_piece = Tetromino(12, 2)

    #将当前方块写入游戏板
    def _write_down_current_piece(self, arr, y_diff=0):
        for x in range(4):
            for y in range(4):
                if self._current_piece.arr[x][y] is not None:
                    if self._current_piece.y + y + y_diff >= board_height:
                        print(3)
                    arr[self._current_piece.x + x][self._current_piece.y + y + y_diff] = self._current_piece.arr[x][y]
                    arr[self._current_piece.x + x][self._current_piece.y + y + y_diff].x = self._current_piece.x + x
                    arr[self._current_piece.x + x][self._current_piece.y + y + y_diff].y = self._current_piece.y + y

    #用于移动当前方块
    def move_current_piece(self, x, y):
        match self._current_piece.check_move(x, y, self.arr):
            case 1:
                self._current_piece.move(x, y)
            case -1:
                self._write_down_current_piece(self.arr)
                self._create_new_piece()
            case 0:
                pass

    def rotate_current_piece(self):
        if self._current_piece.checkangle(self.arr):
            self._current_piece.rotate()

    def restart(self):
        self.lost = False
        self.arr = [[None for i in range(board_height)] for j in range(board_width)]
        self._points = 0
        self.start_game()


class Block:
    def __init__(self, color=gray):
        self.x = 0
        self.y = 0
        self.color = color

    def render(self, display, offset=0):
        pygame.draw.rect(display,
                         self.color,
                         pygame.Rect(
                             board_edge_x + self.x * (block_size + block_offset) + offset,
                             board_edge_y + self.y * (block_size + block_offset) + offset,
                             block_size,
                             block_size))


class Button:
    def __init__(self, text, x, y):
        self.x = x
        self.y = y
        self._font = pygame.font.SysFont('fangsong', 48,True)
        self._text = self._font.render(text, True, white)
        self._size = self._text.get_size()
        self._surface = pygame.Surface(self._size)
        self._surface.fill(black)
        self._surface.blit(self._text, (0, 0))
        self._rect = pygame.Rect(self.x, self.y, self._size[0], self._size[1])

    def render(self, display):
        display.blit(self._surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:   #检测是否按下左键
            if self._rect.collidepoint(x, y):   #检测鼠标位置是否在按钮范围内
                return True
        return False


class App:
    def __init__(self):
        self._font = None
        self._menu_button = None
        self._board = None
        self._running = True
        self._display_surf = None
        self._size = self._width, self._height = 560, 720
        self._FPS = pygame.time.Clock()
        self._time = 0
        self._controls_up = False
        self._controls_down = False
        self._controls_left = False
        self._controls_right = False
        self._time_to_move_down = 10
        self._menu = True

    def _on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self._size)#####
        self._running = True
        self._board = Board()
        self._menu_button = Button("开始", self._width / 2 - 40, int(self._height / 3))
        self._board.start_game()
        self.restart= main.Main()

    def _on_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            self.restart.start_interface()
            self._running = False
            print('游戏已结束')
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self._menu_button.click(event) and self._menu:
                self._board.restart()
                self._menu = False

        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w | pygame.K_UP:
                    # self._controls_up = True
                    self._board.rotate_current_piece()
                case pygame.K_a | pygame.K_LEFT:
                    self._controls_left = True
                case pygame.K_s | pygame.K_DOWN:
                    self._controls_down = True
                case pygame.K_d | pygame.K_RIGHT:
                    self._controls_right = True
                case pygame.K_RETURN | pygame.K_r:
                    self._board.restart()
                    self._menu = False
                case pygame.K_ESCAPE:
                    print('游戏已结束')
                    pygame.quit()
                    self.restart.start_interface()
                    self._running = False
        elif event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_w | pygame.K_UP:
                    self._controls_up = False
                case pygame.K_a | pygame.K_LEFT:
                    self._controls_left = False
                case pygame.K_s | pygame.K_DOWN:
                    self._controls_down = False
                case pygame.K_d | pygame.K_RIGHT:
                    self._controls_right = False

    def _on_loop(self):
        if self._board.lost:
            self._menu = True
        else:
            if self._time == self._time_to_move_down:
                self._board.move_current_piece(0, 1)
                self._time = 0
            else:
                self._time += 1

            if self._controls_right:
                self._board.move_current_piece(1, 0)
            elif self._controls_left:
                self._board.move_current_piece(-1, 0)
            # elif self._controls_up:
            #     self._board.rotate_current_piece()
            elif self._controls_down:
                self._board.move_current_piece(0, 1)

    def _on_render(self):
        self._display_surf.fill((0,0,0))
        if self._menu:
            self._menu_button.render(self._display_surf)
        else:
            self._board.render(self._display_surf)
        pygame.display.flip()
        self._FPS.tick(20)

    def on_execute(self):
        self._on_init()
        while self._running:
            for event in pygame.event.get():
                self._on_event(event)
            self._on_loop()
            self._on_render()
        exit()

if __name__ == '__main__':
    new = App()
    new.on_execute()