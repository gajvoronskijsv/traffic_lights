import asyncio
from traffic_lights.lights import AutoTrafficLight, PedestrianTrafficLight
from traffic_lights.movement_schemes import MovementScheme
from random import randint
from copy import deepcopy


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

    async def simulate(self, args):
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
            traffic_light.movement_schemes = deepcopy(movement_schemes)
            asyncio.create_task(traffic_light.run())

        # Запуск движения транспорта на зеленый
        asyncio.create_task(self.move_on_green())

        def generate_traffic():
            auto_top.camera_queue += randint(0, int(args.cars_top))
            auto_left.camera_queue += randint(0, int(args.cars_left))
            auto_right.camera_queue += randint(0, int(args.cars_right))
            auto_bottom.camera_queue += randint(0, int(args.cars_bottom))

            pedestrian_top_right_to_left.camera_queue += randint(0, int(args.pedestrians_top))
            pedestrian_top_left_to_right.camera_queue = randint(0, int(args.pedestrians_top))

            pedestrian_top_right_to_bottom.camera_queue = randint(0, int(args.pedestrians_right))
            pedestrian_bottom_right_to_top.camera_queue = randint(0, int(args.pedestrians_right))

            pedestrian_bottom_right_to_left.camera_queue = randint(0, int(args.pedestrians_bottom))
            pedestrian_bottom_left_to_right.camera_queue = randint(0, int(args.pedestrians_bottom))

            pedestrian_bottom_left_to_top.camera_queue = randint(0, int(args.pedestrians_left))
            pedestrian_top_left_to_bottom.camera_queue = randint(0, int(args.pedestrians_left))

        def print_crossroad():
            print(
                f"""
                \t{pedestrian_top_left_to_right.print()}\t\t\t\t{pedestrian_top_right_to_left.print()}
                {pedestrian_top_left_to_bottom.print()}\t\t\t\t\t\t{pedestrian_top_right_to_bottom.print()}
                \t\t\t{auto_top.print()}
                \t\t{auto_left.print()}\t\t{auto_right.print()}
                \t\t\t{auto_bottom.print()}
                {pedestrian_bottom_left_to_top.print()}\t\t\t\t\t\t{pedestrian_bottom_right_to_top.print()}
                \t{pedestrian_bottom_left_to_right.print()}\t\t\t\t{pedestrian_bottom_right_to_left.print()}
                """
            )

        # Запуск генерации трафика и мониторинга перекрестка
        count = 0
        while True:
            count += 1
            print(f"Шаг {count}\nГенерация трафика")
            generate_traffic()
            print("Перекресток с добавленным трафиком")
            print_crossroad()
            await asyncio.sleep(5)
            print("Перекресток через 5 секунд")
            print_crossroad()
