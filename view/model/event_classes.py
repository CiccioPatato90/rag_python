from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from enum import Enum
from typing import List, Dict, Optional, Union

class State:
    """
    Represents the state object containing the last query and response.
    """
    def __init__(self, last_query: Optional[str] = None, last_response: Optional[str] = None, connected: Optional[bool] = None):
        self.last_query = last_query
        self.last_response = last_response
        self.connected = connected

class EventType(Enum):
    """
    Enum representing different types of events (channels).
    """
    NEW_RESPONSE = "NEW_RESPONSE"
    NEW_QUERY = "NEW_QUERY"

class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass


class ConcreteSubject(Subject):
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """
    _state: State
    _observers: Dict[EventType, List[Observer]] = {
        event_type: [] for event_type in EventType
    }

    def __init__(self):
        self._state = State()

    def attach(self, event_type: EventType, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers[event_type].append(observer)

    def detach(self, event_type: EventType, observer: Observer) -> None:
        if observer in self._observers[event_type]:
            self._observers[event_type].remove(observer)

    def notify(self, event_type: EventType) -> None:
        """
        Trigger an update in each subscriber for the specified event type.
        """
        print(f"Subject: Notifying observers for {event_type}...")
        for observer in self._observers[event_type]:
            observer.update(self, event_type)

    def some_business_logic(self) -> None:
        """
        Example of a method that triggers notifications to observers.
        """
        print("\nSubject: I'm doing something important.")
        self._state = randrange(0, 10)

        print(f"Subject: My state has just changed to: {self._state}")
        # Notify different channels conditionally for demonstration
        # if self._state % 2 == 0:
        #     self.notify(EventType.TYPE_A)
        # else:
        #     self.notify(EventType.TYPE_B)
            
    def get_state(self) -> State:
        return self._state


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: Subject, event_type: EventType) -> None:
        """
        Receive an update from the subject for a specific event type.
        """
        pass


# Example implementation of a concrete observer:
class ConcreteObserver(Observer):
    def update(self, subject: Subject, event_type: EventType) -> None:
        print(f"Observer: Reacted to {event_type}. State: {subject._state}")