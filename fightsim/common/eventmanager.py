import logging
from typing import Any, Callable, Dict, List, Optional


class EventManager:
    """ Observer Class for MVC model"""
    def __init__(self, name):
        self._observers: Dict[str, List[Callable]] = {}
        self._name: str = name
        self.logger = logging.getLogger(__name__)  # Get a module-level logger

    def __repr__(self):
        return f"{self._name} manages observers for these properties {list(self._observers.keys())}"

    def attach(self, observer: Callable, event_type: str):
        """ Attach an observer to a specific property"""
        if observer is None or event_type is None:
            self.logger.error("Attempted to attach an observer or subscribe to a None event type")
            return
        if event_type not in self._observers:
            self._observers[event_type] = []
        self._observers[event_type].append(observer)
        self.logger.debug(f"Observer attached to {event_type}")

    def notify(self, event_type, data=None):
        """ Notify all the observers about a change to a specific property"""
        observers = self._observers.get(event_type, [])
        if not observers:
            self.logger.warning(f"No observers registered for {event_type}")
            return
        for observer in observers:
            observer.update(event_type, data)
        self.logger.debug(f"Notified {len(observers)} observers for {event_type} with data: {data}")

    def detach(self, observer: Callable, event_type: Optional[str] = None) -> None:
        if observer is None:
            self.logger.error("Attempted to detach a None observer.")
            return
        if event_type:
            self._remove_observer_from_type(observer, event_type)
        else:
            self._remove_observer_from_all_types(observer)

    def _remove_observer_from_type(self, observer: Callable, event_type: str) -> None:
        if observer in self._observers.get(event_type, []):
            self._observers[event_type].remove(observer)
            self.logger.debug(f"Detached observer from {event_type}.")

    def _remove_observer_from_all_types(self, observer: Callable) -> None:
        for event_type, observers in list(self._observers.items()):
            if observer in observers:
                observers.remove(observer)
                self.logger.debug(f"Detached observer from {event_type}.")

    def list_observers(self, event_type=None):
        """List all observers or observes for a specific property"""
        if event_type:
            return self._observers.get(event_type, [])
        return self._observers
