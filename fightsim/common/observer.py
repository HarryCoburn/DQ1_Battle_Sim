import logging


class Observer:
    """ Observer Class for MVC model"""
    def __init__(self, name):
        self._observers = {}
        self._name = name
        logging.basicConfig(level=logging.DEBUG)

    def __repr__(self):
        return f"{self._name} contains observers {self._observers}"

    def attach(self, observer, property_name):
        """ Attach an observer to a specific property"""
        if observer is None or property_name is None:
            logging.error("Attempted to attach None observer or property")
            return
        if property_name not in self._observers:
            self._observers[property_name] = []
        self._observers[property_name].append(observer)
        logging.debug(f"Observer attached to {property_name}")

    def notify(self, property_name, data=None):
        """ Notify all the observers about a change to a specific property"""
        if property_name not in self._observers:
            logging.warning(f"No observers for {property_name}")
            return
        for observer in self._observers.get(property_name, []):
            observer.update(property_name, self, data)
        logging.debug(f"Observers notified for {property_name} with data: {data}")

    def detach(self, observer, property_name=None):
        """Detaches an observer"""
        if observer is None:
            logging.error("Attempted to detach None observer")
            return
        if property_name:
            if observer in self._observers.get(property_name, []):
                self._observers[property_name].remove(observer)
                logging.debug(f"Observer detached from {property_name}")
            else:
                for key in list(self._observers):
                    if observer in self._observers[key]:
                        self._observers[key].remove(observer)
                        logging.debug(f"Observer detached from {key}")

    def list_observers(self, property_name=None):
        """List all observers or observes for a specific property"""
        if property_name:
            return self._observers.get(property_name, [])
        return self._observers
