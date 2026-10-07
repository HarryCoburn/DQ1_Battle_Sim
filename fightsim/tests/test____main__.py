import unittest
from random import Random
from unittest.mock import patch, MagicMock
from fightsim.__main__ import build_app, main


class TestBuildApp(unittest.TestCase):

    @patch('fightsim.__main__.Controller')
    @patch('fightsim.__main__.View')
    @patch('fightsim.__main__.Model')
    @patch('fightsim.__main__.player_factory')
    @patch('fightsim.__main__.enemy_dummy_factory')
    def test_build_app_wires_model_view_and_controller(self, MockEnemyFactory, MockPlayerFactory,
                                                       MockModel, MockView, MockController):
        controller = build_app()

        MockModel.assert_called_once_with(player=MockPlayerFactory.return_value,
                                          enemy=MockEnemyFactory.return_value)
        MockView.assert_called_once_with()

        model, view, rng = MockController.call_args.args
        self.assertIs(model, MockModel.return_value)
        self.assertIs(view, MockView.return_value)
        self.assertIsInstance(rng, Random)

        MockView.return_value.bind_actions.assert_called_once_with(MockController.return_value)
        MockController.return_value.initial_update.assert_called_once_with()
        self.assertIs(controller, MockController.return_value)


@patch('fightsim.__main__.logging.config.fileConfig')
class TestMain(unittest.TestCase):

    @patch('fightsim.__main__.build_app')
    def test_main_runs_app_and_returns_zero(self, MockBuildApp, _):
        self.assertEqual(main(), 0)
        MockBuildApp.return_value.run.assert_called_once_with()

    @patch('fightsim.__main__.build_app', side_effect=RuntimeError("no display"))
    def test_main_returns_one_when_startup_fails(self, MockBuildApp, _):
        with self.assertLogs('fightsim.main', level='ERROR'):
            self.assertEqual(main(), 1)


if __name__ == '__main__':
    unittest.main()
