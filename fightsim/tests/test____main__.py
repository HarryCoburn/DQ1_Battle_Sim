import unittest
from unittest.mock import patch, MagicMock
import logging
from fightsim.__main__ import create_event_manager, create_view, create_model, create_controller, main


class TestMain(unittest.TestCase):

    @patch('fightsim.__main__.EventManager')
    def test_create_event_manager(self, MockEventManager):
        event_manager = create_event_manager()
        MockEventManager.assert_called_once_with("DQ1 Model Observer")
        self.assertTrue(MockEventManager.called)

    @patch('fightsim.__main__.View')
    def test_create_view(self, MockView):
        view = create_view()
        MockView.assert_called_once()
        self.assertTrue(MockView.called)

    @patch('fightsim.__main__.Model')
    @patch('fightsim.__main__.player_factory')
    @patch('fightsim.__main__.enemy_dummy_factory')
    def test_create_model(self, MockEnemyFactory, MockPlayerFactory, MockModel):
        mock_event_manager = MagicMock()
        model = create_model(mock_event_manager)
        MockModel.assert_called_once_with(player=MockPlayerFactory(), enemy=MockEnemyFactory(), observer=mock_event_manager)
        self.assertTrue(MockModel.called)

    @patch('fightsim.__main__.Controller')
    def test_create_controller(self, MockController):
        mock_model = MagicMock()
        mock_view = MagicMock()
        mock_event_manager = MagicMock()
        controller = create_controller(mock_model, mock_view, mock_event_manager)
        MockController.assert_called_once_with(mock_model, mock_view, mock_event_manager)
        self.assertTrue(MockController.called)

if __name__ == '__main__':
    unittest.main()