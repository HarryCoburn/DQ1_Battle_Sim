import unittest
from unittest.mock import MagicMock
import logging
from ..common.eventmanager import EventManager


class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManager("TestManager")

    def test_initialization(self):
        self.assertEqual(self.event_manager._name, "TestManager")
        self.assertDictEqual(self.event_manager._observers, {})
        self.assertIsInstance(self.event_manager.logger, logging.Logger)

    def test_attach(self):
        observer = MagicMock()
        self.event_manager.attach(observer, 'event1')
        self.assertIn('event1', self.event_manager._observers)
        self.assertIn(observer, self.event_manager._observers['event1'])

    def test_notify(self):
        observer = MagicMock()
        self.event_manager.attach(observer, 'event1')
        self.event_manager.notify('event1', 'data')
        observer.update.assert_called_once_with('event1', 'data')

    def test_detach_from_event_type(self):
        observer = MagicMock()
        self.event_manager.attach(observer, 'event1')
        self.event_manager.detach(observer, 'event1')
        self.assertNotIn(observer, self.event_manager._observers.get('event1', []))

    def test_detach_from_all_events(self):
        observer = MagicMock()
        self.event_manager.attach(observer, 'event1')
        self.event_manager.attach(observer, 'event2')
        self.event_manager.detach(observer)
        self.assertNotIn(observer, self.event_manager._observers.get('event1', []))
        self.assertNotIn(observer, self.event_manager._observers.get('event2', []))

    def test_notify_no_observers(self):
        with self.assertLogs(self.event_manager.logger, level='WARNING') as log:
            self.event_manager.notify('event1', 'data')
            self.assertIn('No observers registered for event1', log.output[0])

    def test_attach_none_parameters(self):
        with self.assertLogs(self.event_manager.logger, level='ERROR') as log:
            self.event_manager.attach(None, 'event1')
            self.assertIn('Attempted to attach an observer or subscribe to a None event type', log.output[0])

    def test_detach_none_observer(self):
        with self.assertLogs(self.event_manager.logger, level='ERROR') as log:
            self.event_manager.detach(None, 'event1')
            self.assertIn('Attempted to detach a None observer.', log.output[0])


if __name__ == '__main__':
    unittest.main()
