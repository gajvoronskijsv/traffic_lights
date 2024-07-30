from abc import abstractmethod
from traffic_lights.events import Event
import asyncio


class TrafficLight:
    """
    Абстрактный светофор
    """
    states = None

    def __init__(self,
                 id,
                 crossroad,
                 current_state="red",
                 camera_queue=0,
                 event_queue=[],
                 received_events=[],
                 movement_schemes=None):
        self.id = id
        self.crossroad = crossroad
        self.current_state = current_state
        self.camera_queue = camera_queue
        self.event_queue = event_queue
        self.movement_schemes = movement_schemes
        self.pass_next_vote = True
        self.received_events = received_events

    def print(self):
        return f"({self.current_state[0]})({self.camera_queue})"

    async def send_event(self, target_id, timer=0):
        await asyncio.sleep(timer)
        for scheme in self.movement_schemes:
            scheme.rating = 0
            scheme.votes_counter = 0
        if self.pass_next_vote:
            message = "pass"
        else:
            message = "vote"
        self.received_events = []
        event = Event(target_id=target_id,
                      sender_id=self.id,
                      sender_camera_queue=self.camera_queue,
                      sender_state=self.current_state,
                      sender_message=message)
        self.crossroad.pass_event(event)

    def receive_event(self, event):
        self.event_queue.append(event)

    def learn_state(self, target_id):
        return self.crossroad.pass_state(target_id)

    def get_state(self):
        return self.current_state

    async def run(self):
        await self.send_event("*", 0)
        while True:
            await asyncio.sleep(0)
            # Проверка ивентов в очереди и обновление голосов по схемам
            for event in list(self.event_queue):
                event_is_received = False
                for received_event in self.received_events:
                    if received_event.sender_id == event.sender_id:
                        event_is_received = True
                if event_is_received:
                    continue
                self.received_events.append(event)
                for scheme in self.movement_schemes:
                    scheme.votes_counter += 1
                    if event.message == "vote":
                        if event.sender_id in scheme.green_lights:
                            scheme.rating += event.sender_camera_queue
                        else:
                            scheme.rating -= event.sender_camera_queue
                self.event_queue.remove(event)
            # Проверка, получены ли все нужные сообщения
            all_schemes_voted = True
            for scheme in self.movement_schemes:
                if scheme.votes_counter != len(self.crossroad.traffic_lights):
                    all_schemes_voted = False
            # Если все сообщения получены, идет поиск самой лучшей схемы и переключается состояние светофора:
            if all_schemes_voted:
                # Если все светофоры отработали и уступают другим, то нужен сброс уступок
                pass_counter = 0
                for received_event in self.received_events:
                    if received_event.message == "pass":
                        pass_counter += 1
                if pass_counter == len(self.crossroad.traffic_lights):
                    if self.camera_queue != 0:
                        self.pass_next_vote = False
                    await self.send_event("*", 0)
                    continue
                # поиск самой лучшей схемы
                best_scheme = self.movement_schemes[0]
                for scheme in self.movement_schemes:
                    if scheme.rating > best_scheme.rating:
                        best_scheme = scheme
                best_scheme_index = 0
                while best_scheme is not self.movement_schemes[best_scheme_index]:
                    best_scheme_index += 1
                # переключение режима работы светофора и отправка сообщения с задержкой
                if self.id in best_scheme.green_lights:
                    await self.toggle_lights("green")
                    # так как светофор пропустит свой трафик, необходимо уступить другим светофорам
                    self.pass_next_vote = True
                else:
                    await self.toggle_lights("red")
                await self.send_event("*", 5)

    @abstractmethod
    async def toggle_lights(self, colour):
        pass


class PedestrianTrafficLight(TrafficLight):
    """
    Светофор для пешеходов
    """

    def __init__(self, *args):
        self.states = ["red", "green"]
        super().__init__(*args)

    async def toggle_lights(self, colour):
        if self.current_state == colour:
            return
        if self.current_state == "red":
            self.current_state = "green"
        elif self.current_state == "green":
            self.current_state = "red"


class AutoTrafficLight(TrafficLight):
    """
    Светофор для автомобилей
    """

    def __init__(self, *args):
        self.states = ["red", "yellow", "green"]
        super().__init__(*args)

    async def toggle_lights(self, colour):
        if self.current_state == colour:
            return
        if self.current_state == "red":
            self.current_state = "green"
        elif self.current_state == "yellow":
            self.current_state = "red"
        elif self.current_state == "green":
            self.current_state = "yellow"
            self.current_state = "red"
