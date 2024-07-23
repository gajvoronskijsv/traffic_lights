from time import sleep


class Event:
    def __init__(self, target_id, sender_id=None, sender_camera_queue=None, sender_state=None):
        self.target_id = target_id
        self.sender_id = sender_id
        self.sender_camera_queue = sender_camera_queue
        self.sender_state = sender_state


class Crossroad:
    traffic_lights = []

    def __init__(self):
        pass

    def pass_event(self, event):
        for light in self.traffic_lights:
            if light.id == event.target_id:
                light.receive_event(event)
                return

    def pass_state(self, target_id):
        for light in self.traffic_lights:
            if light.id == target_id:
                return light.get_state()


class TrafficLight:
    def __init__(self, id, crossroad, current_state, camera_queue, event_queue):
        self.id = id
        self.crossroad = crossroad
        self.current_state = current_state
        self.camera_queue = camera_queue
        self.event_queue = event_queue

    def send_event(self, target_id, timer=0):
        event = Event(target_id=target_id,
                      sender_id=self.id,
                      sender_camera_queue=self.camera_queue,
                      sender_state=self.current_state)
        sleep(timer)
        self.crossroad.pass_event(event)

    def receive_event(self, event):
        self.event_queue.append(event)

    def learn_state(self, target_id):
        return self.crossroad.pass_state(target_id)

    def get_state(self):
        return self.current_state


class PedestrianTrafficLight(TrafficLight):
    def __init__(self, id, crossroad, current_state=None, camera_queue=0, event_queue=[]):
        self.__init__(id, crossroad, current_state, camera_queue, event_queue)
        self.states = ["red", "green"]


class AutoTrafficLight(TrafficLight):
    def __init__(self, id, current_state=None, camera_queue=0, event_queue=[]):
        self.__init__(id, current_state, camera_queue, event_queue)
        self.states = ["red", "yellow", "green"]
