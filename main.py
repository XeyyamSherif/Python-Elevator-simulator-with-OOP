from distutils.command.build import build
from re import T
from shutil import move
import time
import random
import sys
from numpy import floor, negative

'''

    Class starts from here

'''


class Elevator():
    def __init__(self, last_floor_to_go, direction, passenger, max_floor_of_building, current_floor=1):
        self.current_floor = current_floor
        self.floors_to_go = last_floor_to_go
        self.direction = direction
        self.passenger = passenger
        self.max_floor = max_floor_of_building
        self.last_floor_to_go = last_floor_to_go

    def move(self):
        difference = self.last_floor_to_go-self.current_floor
        if difference > 0:
            self.direction = 'up'
        elif difference < 0:
            self.direction = 'down'

        if self.current_floor == 1:
            self.direction = "up"
        elif self.current_floor == self.max_floor:
            self.direction = 'down'
        if self.direction == 'up':
            self.current_floor += 1
        elif self.direction == 'down':
            self.current_floor -= 1
        time.sleep(0.5)

    def define_floor_to_go(self):
        if self.direction == 'up':
            max_floor_of_passengers_inside_elevator = max(
                [item.moving_to for item in self.passenger], default=self.max_floor)
            self.last_floor_to_go = max_floor_of_passengers_inside_elevator
        else:
            min_floor_of_passengers_inside_elevator = min(
                [item.moving_to for item in self.passenger], default=1)
            self.last_floor_to_go = min_floor_of_passengers_inside_elevator


class floor_of_the_building():
    def __init__(self, th, Passenger):
        self.th = th
        self.passenger = Passenger


class Building():
    def __init__(self, elevator, floors):
        self.elevator = elevator
        self.floors = floors


class Passenger():
    def __init__(self,  cur_floor, moving_to_floor, direction, max_floor):
        self.cur_floor = cur_floor
        self.moving_to = moving_to_floor
        self.direction = direction
        self.max_floor = max_floor

    def define_direction(self):
        difference = self.moving_to - self.cur_floor
        if difference == 0:
            while True:
                difference = self.moving_to - self.cur_floor
                if difference == 0:
                    self.moving_to = random.randint(1, self.max_floor)
                else:
                    break
        if difference > 0:
            self.direction = 'up'
        elif difference < 0:
            self.direction = 'down'

    def change_moving_to(self):
        self.moving_to = random.randint(1, self.max_floor)
        self.define_direction()


'''

    Main functions starts from here

'''


def create_building():
    '''
    this functions creates building and other classes
    '''

    # next 6 line create Building and elevator
    elevator_x = Elevator(1, "up", [], 5)
    floors = []
    for i in range(1, random.randint(5, 6)):
        floor_i = floor_of_the_building(i, [])
        floors.append(floor_i)
    bulding_x = Building(elevator_x, floors)

    # define max_floor_of the building for future use
    elevator_x.max_floor = len(bulding_x.floors)
    # next 8 line code create passengers for every floor
    for item in bulding_x.floors:
        item_passengers = []
        for i in range(1, random.randint(5, 10)):
            passenger_1 = Passenger(
                item.th, random.randint(1, elevator_x.max_floor), '', elevator_x.max_floor)
            passenger_1.change_moving_to()
            item_passengers.append(passenger_1)

        item.passenger = item_passengers

    return elevator_x, bulding_x


def passeger_transfer(elevator, building):
    '''
        this functions transfers passenger when levator reach to floor
    '''

    floor_elevator_now = building.floors[elevator.current_floor-1].passenger
    traveler_get_off = 0
    traveler_get_in = 0

    # in next 10 code traveler get off from elevator
    if len(elevator.passenger) == 0:
        # print('nobody in Elevator')
        pass
    else:
        for traveler_inside_elevator in list(elevator.passenger):
            if traveler_inside_elevator.moving_to == elevator.current_floor:
                traveler_inside_elevator.change_moving_to()
                traveler_inside_elevator.cur_floor = elevator.current_floor
                floor_elevator_now.append(traveler_inside_elevator)
                elevator.passenger.remove(traveler_inside_elevator)
                traveler_get_off += 1
        print(traveler_get_off, ' passengers is getting off')

    # in next 6 code traveler get in  elevator
    for traveler in list(floor_elevator_now):
        if traveler.direction == elevator.direction:
            if len(elevator.passenger) < 5 and len(floor_elevator_now) > 0:
                elevator.passenger.append(traveler)
                floor_elevator_now.remove(traveler)
                traveler_get_in += 1
    print(traveler_get_in, ' passengers is getting in')


def main():
    object = create_building()
    elevator_x = object[0]
    bulding_x = object[1]

    while True:
        print('elevator current floor:{}'.format(elevator_x.current_floor))
        passeger_transfer(elevator_x, bulding_x)
        elevator_x.define_floor_to_go()

        elevator_x.move()
        time.sleep(0.05)


main()
