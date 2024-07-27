import copy
from random import randint
import asyncio
from abc import abstractmethod


class Event:
    """
    События, которыми обмениваются светофоры
    """

    def __init__(self, target_id, sender_id, sender_camera_queue, sender_state, sender_message):
        self.target_id = target_id
        self.sender_id = sender_id
        self.sender_camera_queue = sender_camera_queue
        self.sender_state = sender_state
        self.message = sender_message


class MovementScheme:
    """
    Схема движения на перекрестке, определяемая тем, какие светофоры должны гореть зеленым одновременно
    """

    def __init__(self, green_lights):
        self.green_lights = green_lights
        self.votes_counter = 0
        self.rating = 0


class Crossroad:
    """
    Абстракция среды, которая передает данные между светоформаи, расставляет их и симулирует трафик
    """
    traffic_lights = []

    def __init__(self):
        pass

    def pass_event(self, event):
        for light in self.traffic_lights:
            if light.id == event.target_id or event.target_id == "*":
                light.receive_event(event)

    def pass_state(self, target_id):
        for light in self.traffic_lights:
            if light.id == target_id:
                return light.get_state()

    async def move_on_green(self):
        while True:
            for traffic_light in self.traffic_lights:
                if traffic_light.current_state == "green" or traffic_light.current_state == "yellow":
                    traffic_light.camera_queue = 0
            await asyncio.sleep(0.5)

    async def simulate(self, mode="all traffic"):
        # генерация свеотофоров
        auto_top = AutoTrafficLight(0, self)
        self.traffic_lights.append(auto_top)
        auto_right = AutoTrafficLight(1, self)
        self.traffic_lights.append(auto_right)
        auto_bottom = AutoTrafficLight(2, self)
        self.traffic_lights.append(auto_bottom)
        auto_left = AutoTrafficLight(3, self)
        self.traffic_lights.append(auto_left)

        pedestrian_top_right_to_left = PedestrianTrafficLight(4, self)
        self.traffic_lights.append(pedestrian_top_right_to_left)
        pedestrian_top_right_to_bottom = PedestrianTrafficLight(5, self)
        self.traffic_lights.append(pedestrian_top_right_to_bottom)

        pedestrian_bottom_right_to_top = PedestrianTrafficLight(6, self)
        self.traffic_lights.append(pedestrian_bottom_right_to_top)
        pedestrian_bottom_right_to_left = PedestrianTrafficLight(7, self)
        self.traffic_lights.append(pedestrian_bottom_right_to_left)

        pedestrian_bottom_left_to_right = PedestrianTrafficLight(8, self)
        self.traffic_lights.append(pedestrian_bottom_left_to_right)
        pedestrian_bottom_left_to_top = PedestrianTrafficLight(9, self)
        self.traffic_lights.append(pedestrian_bottom_left_to_top)

        pedestrian_top_left_to_bottom = PedestrianTrafficLight(10, self)
        self.traffic_lights.append(pedestrian_top_left_to_bottom)
        pedestrian_top_left_to_right = PedestrianTrafficLight(11, self)
        self.traffic_lights.append(pedestrian_top_left_to_right)

        # Создание схем движения
        movement_schemes = [MovementScheme(
            green_lights=[
                auto_top.id,
                auto_bottom.id
            ]
        ), MovementScheme(
            green_lights=[
                auto_left.id,
                auto_right.id
            ]
        ), MovementScheme(
            green_lights=[
                pedestrian_top_right_to_left.id,
                pedestrian_top_right_to_bottom.id,
                pedestrian_bottom_right_to_top.id,
                pedestrian_bottom_right_to_left.id,
                pedestrian_bottom_left_to_right.id,
                pedestrian_bottom_left_to_top.id,
                pedestrian_top_left_to_bottom.id,
                pedestrian_top_left_to_right.id,
            ]
        ), MovementScheme(
            green_lights=[
                auto_bottom.id,
                pedestrian_top_left_to_bottom.id,
                pedestrian_bottom_left_to_top.id,
            ]
        ), MovementScheme(
            green_lights=[
                auto_top.id,
                pedestrian_top_right_to_bottom.id,
                pedestrian_bottom_right_to_top.id,
            ]
        ), MovementScheme(
            green_lights=[
                auto_right.id,
                pedestrian_bottom_left_to_right.id,
                pedestrian_bottom_right_to_left.id,
            ]
        ), MovementScheme(
            green_lights=[
                auto_left.id,
                pedestrian_top_right_to_left.id,
                pedestrian_top_left_to_right.id,
            ]
        )]
        # Запуск светофоров
        for traffic_light in self.traffic_lights:
            traffic_light.movement_schemes = copy.deepcopy(movement_schemes)
            asyncio.create_task(traffic_light.run())

        # Запуск движения транспорта на зеленый
        asyncio.create_task(self.move_on_green())

        # Запуск генерации трафика и мониторинга перекрестка
        count = 0
        while True:
            count += 1
            print(f"Шаг {count}\nГенерация трафика")
            for traffic_light in self.traffic_lights:
                if mode == "no pedestrians" and len(traffic_light.states) == 2: continue  # отключает генерацию пешеходов
                if mode == "no cars" and len(traffic_light.states) == 3: continue #отключает генерацию авто
                traffic_light.camera_queue += randint(0, 5)

            def print_crossroad():
                print(
                    f"""
                    \t{pedestrian_top_left_to_right.print()}\t\t\t{pedestrian_top_right_to_left.print()}
                    {pedestrian_top_left_to_bottom.print()}\t\t\t\t\t{pedestrian_top_right_to_bottom.print()}
                    \t\t\t{auto_top.print()}
                    \t\t{auto_left.print()}\t{auto_right.print()}
                    \t\t\t{auto_bottom.print()}
                    {pedestrian_bottom_left_to_top.print()}\t\t\t\t\t{pedestrian_bottom_right_to_top.print()}
                    \t{pedestrian_bottom_left_to_right.print()}\t\t\t{pedestrian_bottom_right_to_left.print()}
                    """
                )

            print("Перекресток с добавленным трафиком")
            print_crossroad()
            await asyncio.sleep(5)
            print("Перекресток через 5 секунд")
            print_crossroad()


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


mode = "all traffic"
# mode = "no pedestrians"
# mode = "no cars"
crossroad = Crossroad()
asyncio.run(crossroad.simulate(mode))
