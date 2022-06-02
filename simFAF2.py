import logging
import threading
import time

consumption = []
generation = []
game_finish = False

blueprints = [
    {
        'Type': 'Engineer',
        'Tier' : 1,
        'BuildRate ' : 5,
        'Health ' : 100
    }
]

unitList = [
    {
        'Type': 'Engineer',
        'Tier': 1,
        'Dead': False,
        'Active' : False
    }
]

def create_consumption_unit(unit):
    global consumption
    consumption.append(unit)

def game_run(name):
    global game_finish
    print("Starting Game")
    time.sleep(30)
    game_finish = True
    print("Finishing Game")


def economy_thread(name):
    global game_finish
    while game_finish == False:
        print(next((x for x in blueprints if x["Type"] == "Engineer"), None))
        time.sleep(0.50)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=economy_thread, args=(1,))
    y = threading.Thread(target=game_run, args=(1,))
    logging.info("Main    : before running thread")
    x.start()
    y.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()
    logging.info("Main    : all done")