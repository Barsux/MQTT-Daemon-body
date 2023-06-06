import time
import datetime

#Глобальные списки очередей и модулей
queues = []
modules = []

#Флаги выполнения модулей 
module_flags = {
    "NOT_EVALUATE":0,
    "EVALUATE_ONCE":1,
    "EVALUATE_EVERY_CYCLE":2
}

#Функция разметки готовых к выполнению модулей согласно флагам
def enum_ready_modules() -> tuple:
    global modules
    ready_modules = []
    for module in modules:
        if module.flag:
            if module.flag == module_flags["EVALUATE_ONCE"]:
                module.flag = module_flags["NOT_EVALUATE"]
            ready_modules.append(module)
    return tuple(ready_modules)


#Класс модуля, наследуется для каждого из них
class Module:
    queue = None
    class Queue:
        Listeners = []
        next_clock = 0
        timer = False
        ready = False
        value = None



        def __init__(self, broadcaster):
            queues.append(self)
            self.Listeners.append(broadcaster)
            self.next_clock = time.time_ns()

        def put(self, value):
            self.value = value

        def get(self):
            value = self.value
            self.value = None
            return value

        def enable_wait(self, listener):
            self.Listeners.append(listener)

        def disable_wait(self, listener):
            self.Listeners.remove(listener)

        def start_timer(self, nsec_interval):
            self.nsec_interval = nsec_interval
            self.next_clock = time.time_ns() + nsec_interval
            self.timer = True

        def evaluate(self):
            if (self.timer):
                if time.time_ns() >= self.next_clock:
                    self.setReady()
                    self.next_clock = time.time_ns() + self.nsec_interval

        def setReady(self):
            self.ready = True

        def clear(self):
            self.ready = False

    debug_name = ""
    debug = False

    def __init__(self, flag, name, debug = False):
        self.flag = flag
        self.debug_name = name
        self.debug = debug
        modules.append(self)

    def attach_queue(self):
        raise NotImplementedError

    def printf(self, *args):
        ts = datetime.datetime.today().strftime("%d/%m/%y : %T %us")
        if not self.debug:
            out = f"({ts}) :"
        else:
            out = f"({ts}) [{self.debug_name}]:"
        print(out, *args)

    def enum_ready_queues(self) -> tuple:
        global queues
        return tuple(filter(lambda queue: self in queue.Listeners and queue.ready, queues))


    def evaluate(self):
        raise NotImplementedError