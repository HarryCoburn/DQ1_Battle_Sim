# DQ1 Battle Simulator - App


from fightsim.views.view import View
from fightsim.controllers.controller import Controller
from fightsim.models.model import Model


def main():
    view = View()
    model = Model()
    controller = Controller(model, view)
    view.set_controller(controller)
    controller.initial_update()
    controller.view.mainloop()


if __name__ == "__main__":
    main()
