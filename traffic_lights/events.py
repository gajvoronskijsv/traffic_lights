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