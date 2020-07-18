class State:
    ready_to_fire = False
    fired = False
    stopped = True

    def set_ready_to_fire(self):
        self.ready_to_fire = True
        self.fired = False
        self.stopped = True

    def set_fired(self):
        self.ready_to_fire = False
        self.fired = True
        self.stopped = False

    def set_stopped(self):
        self.ready_to_fire = False
        self.fired = False
        self.stopped = True
