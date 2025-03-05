from Tetris import tetris
from PlaneWar import plane_war
from UI import MenuMain
from Tank_War import start

# print(pygame.font.get_fonts())
class Main:
    def __init__(self):
        self.ui = None

    def start_interface(self):
        self.ui = MenuMain.main()
        if self.ui == 2:
            app = plane_war.App()
            app.run()
        elif self.ui == 3:
            start._main()
        elif self.ui == 4:
            app = tetris.App()
            app.on_execute()


if __name__ == '__main__':
    new = Main()
    new.start_interface()
