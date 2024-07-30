class MovementScheme:
    """
    Схема движения на перекрестке, определяемая тем, какие светофоры должны гореть зеленым одновременно
    """
    def __init__(self, green_lights):
        self.green_lights = green_lights
        self.votes_counter = 0
        self.rating = 0
