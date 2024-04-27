import unittest
from unittest.mock import MagicMock, patch, call
import logging
from ..common.decorators import *

class TestLogFunctionCall(unittest.TestCase):
    def test_log_function_call(self):
        # Create a mock object for the logger
        mock_logger = MagicMock()

        class TestClass:
            def __init__(self):
                self.logger = mock_logger

            @log_function_call
            def test_method(self, arg):
                return arg * 2

        instance = TestClass()
        result = instance.test_method(5)

        self.assertEqual(result, 10)
        # Check if the debug method was called with the expected calls
        expected_calls = [
            call(f"Entering test_method"),
            call(f"Exiting test_method with result 10")
        ]
        mock_logger.debug.assert_has_calls(expected_calls, any_order=False)


class TestMeasurePerformance(unittest.TestCase):
    @patch('logging.debug')
    def test_measure_performance(self, mock_debug):
        @measure_performance
        def some_function():
            return "result"

        result = some_function()
        self.assertEqual(result, "result")
        self.assertTrue(mock_debug.called)


class TestNotifyObservers(unittest.TestCase):
    def test_notify_observers(self):
        mock_observer = MagicMock()

        class Subject:
            def __init__(self):
                self.observer = mock_observer

            @notify_observers(['event1', 'event2'])
            def perform_action(self):
                return "done"

        subject = Subject()
        result = subject.perform_action()

        self.assertEqual(result, "done")
        calls = [call('event1'), call('event2')]
        mock_observer.notify.assert_has_calls(calls, any_order=True)


