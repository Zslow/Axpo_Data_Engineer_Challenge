from subscriber import Subscriber
import threading

if __name__ == "__main__":

    subscriber = Subscriber()
    subscriber.connect_mqtt()
    subscriber.subscribe_mqtt()

    
    worker_thread = threading.Thread(target=subscriber.disk_writer_worker)
    worker_thread.start()
    subscriber.loop_forever()
