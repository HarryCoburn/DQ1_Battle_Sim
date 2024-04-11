'''
DQ1 Battle Simulator - App
'''

from view import View
from controller import Controller
from model import Model


if __name__ == "__main__":
    view = View()
    model = Model()
    controller = Controller(model, view)

    view.set_controller(controller)

    controller.initial_update()

    controller.view.mainloop()
