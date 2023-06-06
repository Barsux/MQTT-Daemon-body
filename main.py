import json
from core import Kernel
from base import enum_ready_modules, time, module_flags
from mqtt import MQTT

FILENAME = "userdata.json"

#Парсим json потом перенесу в отдельный модуль
def parseJson(filename):
    try:
        with open('userdata.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл конфигурации {FILENAME} не найден.")
        exit(0)


if __name__ == "__main__":
    json = parseJson(FILENAME)


    main_core = Kernel(module_flags["EVALUATE_EVERY_CYCLE"], "CORE", True)
    mqtt = MQTT(module_flags["EVALUATE_EVERY_CYCLE"], "MQTT", True, json)
    main_core.attach_queue(mqtt.tx, mqtt.rx)


    while True:
        for module in enum_ready_modules():
            module.evaluate()



