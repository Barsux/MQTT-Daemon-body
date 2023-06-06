from base import Module

class Kernel(Module):
    init = False
    step = 0

    def __init__(self, flag, name, debug = True):
        super().__init__(flag, name, debug)
        self.queue = self.Core_queue(self)
        self.printf("Скрипт запустился штатно!")
    
    def attach_queue(self, mqtt_tx, mqtt_rx):
        self.mqtt_tx = mqtt_tx
        self.mqtt_rx = mqtt_rx


    def evaluate(self):
        for queue in self.enum_ready_queues():
            if queue == self.mqtt_tx:
                msg = self.mqtt_tx.get()
                self.printf(f"Получено сообщение: {msg}")
                self.mqtt_tx.clear()
            

    class Core_queue(Module.Queue):
        def __init__(self, instance):
            super().__init__(instance)
            self.instance = instance