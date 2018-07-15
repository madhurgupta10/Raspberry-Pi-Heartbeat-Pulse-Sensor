from pulsesensor import Pulsesensor
import time
from helium_client import Helium

# Sensor Object
p = Pulsesensor()
p.startAsyncBPM()

helium = Helium("YOUR SERIAL PORT HERE")
helium.connect()

channel = helium.create_channel("YOUR CHANNEL NAME HERE")

# Access an instance of Configuration
config = channel.config()

active = True

try:
    while True:
        if active == True:
            bpm = p.BPM
            if bpm > 0:
                print("BPM: %d" % bpm)
                # Get the channel setting for interval_ms
                interval = config.get("channel.interval_ms")
                interval = config.get("channel.active")
                # Report the device having set interval_ms
                config.set("channel.interval_ms", interval)
                config.set("channel.active", active)
                channel.send(str(bpm))
                time.sleep(interval)
            else:
                print("No Heartbeat found")
                channel.send("Idle")
                time.sleep(5)
                interval = config.get("channel.active")
                config.set("channel.active", active)
except:
    p.stopAsyncBPM()
