from datetime import datetime


class data_type:
    def __init__(self, inc_mostrada, inc_real, bateria, version_firmware, hold, abs, date):
        self.inc_mostrada = inc_mostrada
        self.inc_real = inc_real
        self.bateria = bateria
        self.firmware = version_firmware
        self.hold = hold
        self.abs = abs
        self.date = date
        self.timestamp = datetime.now()
    def __str__(self):
        return self.inc_mostrada + ", " + str(self.timestamp)
