import paho.mqtt.client as mqtt
import logging
from settings import get_settings
import queue
import datetime


class Subscriber(mqtt.Client):
    def __init__(self):
        super().__init__(mqtt.CallbackAPIVersion.VERSION2)
        self.settings = get_settings()
        logging.basicConfig(level=self.settings.logging_level)
        self.message_queue = queue.Queue()
        

    def on_connect(self,client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            logging.info("Connected to MQTT Broker!")
        else:
            logging.info(f"Failed to connect, return code {reason_code}")

    def on_message(self, client, userdata, msg):
        logging.info(f"Received `{msg.payload.decode()}` from '{msg.topic}' topic")
        self.message_queue.put(msg)

    def connect_mqtt(self):

        if self.settings.mqtt.username:
            self.mqtt_client.username_pw_set(
                self.settings.mqtt.username, self.settings.mqtt.password
            )

        self.connect(self.settings.mqtt.host, self.settings.mqtt.port)

    def subscribe_mqtt(self):

        self.subscribe(self.settings.mqtt.topic)

    def disk_writer_worker(self):
        logging.info("Starting Disk write Thread")
        retries = 0
        while True:
            try:
                dt = datetime.datetime.utcnow().strftime("%Y%m%d")
                # Write payload to disk in a daily file persisted in a volume
                # The file would be uploaded to a External Cold Storage in another Process
                with open(f"./data/{dt}.json", "a") as f:

                    msg = self.message_queue.get()
                    logging.debug(f"Writing to file: {msg.payload.decode()}")
                    f.write(f"{msg.payload.decode()}\n")  
                    self.message_queue.task_done()
                    retries = 0
            
            except Exception as e:
                logging.error(f"Error trying to write file: {e}")
                
                if retries < 3:
                    logging.info("Retrying file write.")
                    retries += 1
                    f.close()
                else:
                    raise e

