"""
Dissemination and Prevention Epidemic Simulator (DPES) v 1.0.0
SIRD (Susceptible Infected Recovered Deceased) Model with Control Measures (Mask Application, Social Distancing,
Quarantine, Vaccination, and Lockdown)
"""
import pygame
import pymunk
import random
from collections import deque
import pandas
import matplotlib.pyplot as plt

# Initialize
WIDTH, HEIGHT = 1000, 710  # screen resolution
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SIRD Epidemic Simulation with Control Measures")
pygame.init()
SPACE = pymunk.Space()
FONT = pygame.font.SysFont('Consolas', 20, False, False)

# Colours
BLACK = (0, 0, 0)  # Screen Background
WHITE = (255, 255, 255)  # Susceptible and Social Distancing Ring's
RED = (255, 0, 0)  # Infected
BLUE = (0, 0, 255)  # Recovered
GREEN = (0, 255, 0)  # Deceased
PURPLE = (128, 0, 128)  # Vaccinated
YELLOW = (255, 255, 0)  # Quarantined Ring's

# Data Captured
INFECTED_COUNT = []
RECOVERED_COUNT = []
SUSCEPTIBLE_COUNT = []
DECEASED_COUNT = []
VACCINATED_COUNT = []
QUARANTINE_COUNT = []
SOCIAL_DISTANCING_COUNT = []
LOCKDOWN_COUNT = []
MASK_COUNT = []
DAY_COUNT = []

# Elements
FPS = 60
A_DAY = 1  # 1 day == A_DAY seconds, used for tracking the disease elements
s = deque([], maxlen=(FPS * A_DAY))  # for tracking time for it to do control measures, don't change this
DAY = FPS * A_DAY  # day in-simulation/game, don't change this
BORDER_WIDTH = 2  # pxl, 1 to 10 is preferable
SHOW_AS_PLOT = True  # if True data will be shown as graph
SHOW_AS_DATA = False  # if True data will be printed to the screen
SMOOTH_PLOT = False  # if True graph will be smoother, but smoother means the time/days is raw and not divided by FPS, need's SHOW_AS_PLOT as True
DATA_TO_EXCEL = False  # if True data will be printed in xlsx file, need's SHOW_AS_DATA as True

# Epidemic's Elements
'''Use integer'''
POPULATION = 300  # must not 0
SIZE = 10  # must not 0
PERSON_SPEED = 10  # pxl, how fast everything move in simulation
TRANSMISSION_CHANCE = 100  # 0 to 100%, to get infected
MORTALITY_RATE = 3  # 0 to 100%, more people will die
RECOVERY_TIME = 14  # how long for the person to be recovered in day's, must not 0

# Control Measures
''' Use integer'''
"""
DAY_START_MASK -> start use mask when this day happen
MASK_APPLICATION -> 0 to 100%, less to get infected
DAY_MASK_END -> how long mask application last because people get tired after the given time

DAY_START_DISTANCING -> start doing social distancing when this day happen
SOCIAL_DISTANCING_RATE -> 0 to 100%, more people will doing social distancing
DAY_SOCIAL_DISTANCING_END -> how long social distancing last because people get tired after the given time

DAY_START_QUARANTINE -> start doing quarantine when this day happen
DAY_SCHEDULED_QUARANTINE -> quarantine happens periodically after the above day
QUARANTINE_RATE -> 0 to 100%, how many % infected people will be quarantined every period of time
QUARANTINE_CHANCE -> 0 to 100%, how may % of the chosen infected people will get quarantine if not this/these infected people is can be considered as asymptomatic

DAY_START_VACCINE -> start doing vaccination when this day happen
DAY_SCHEDULED_VACCINE -> vaccination happens periodically after the above day
VACCINATION_RATE -> 0 to 100%, how many % people from population will be vaccinated every period of time
VACCINATION_CHANCE -> 0 to 100%, how many % of the chosen people will successfully build immunity from vaccination if not this/these people just become susceptible again

DAY_START_LOCKDOWN -> start doing lockdown when this day happen
LOCKDOWN -> 0 to 100%, lockdown distance's point, 0% will be no lockdown while 100% is full lockdown
DAY_LOCKDOWN_END -> at what day the lockdown will end
"""

DAY_START_MASK = 0
MASK_APPLICATION = 0
DAY_MASK_END = 0

DAY_START_DISTANCING = 0
SOCIAL_DISTANCING_RATE = 0
DAY_SOCIAL_DISTANCING_END = 0

DAY_START_QUARANTINE = 0
DAY_SCHEDULED_QUARANTINE = 0
QUARANTINE_RATE = 0
QUARANTINE_CHANCE = 0

DAY_START_VACCINE = 0
DAY_SCHEDULED_VACCINE = 0
VACCINATION_RATE = 0
VACCINATION_CHANCE = 0

DAY_START_LOCKDOWN = 0
LOCKDOWN = 0
DAY_LOCKDOWN_END = 0


class Person:
    """
    Creating person with every aspects given
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body = pymunk.Body()
        self.body.position = x, y
        self.speed_x = -PERSON_SPEED / A_DAY
        self.speed_y = PERSON_SPEED / A_DAY
        self.body.velocity = random.uniform(self.speed_x, self.speed_y), random.uniform(self.speed_x, self.speed_y)
        self.shape = pymunk.Circle(self.body, SIZE)
        self.shape.density = 1
        self.shape.elasticity = 1
        self.shape.collision_type = POPULATION
        self.shape_sd = pymunk.Circle(self.body, SIZE + SIZE / 2)
        self.shape_sd.density = 1
        self.shape_sd.elasticity = 1
        self.shape_sd_c = 0
        self.infected_time = 0
        self.recovered_time = 0
        self.deceased_time = 0
        self.social_distancing_time = 0
        self.susceptible_time = 0
        self.deceased = False
        self.recovered = False
        self.infected = False
        self.susceptible = True
        self.social_distancing = False
        self.quarantine = False
        self.vaccinate = False
        SPACE.add(self.shape, self.body)

    # passing time for every individual
    def day_time(self):
        if self.infected or self.quarantine:
            self.infected_time += 1
        if self.social_distancing:
            self.social_distancing_time += 1

    @staticmethod
    def recovered_or_deceased(person):
        if random.randint(1, 100) <= MORTALITY_RATE:
            person.died()
        else:
            person.recover()

    @staticmethod
    def decide_to_distance(person):
        if random.randint(1, 100) <= SOCIAL_DISTANCING_RATE:
            person.distancing()
        else:
            person.normal()

    @staticmethod
    def get_vaccinated(person):
        if random.randint(1, 100) <= VACCINATION_RATE:
            person.vaccine()
        else:
            person.normal()

    @staticmethod
    def get_quarantined(person):
        if random.randint(1, 100) <= QUARANTINE_RATE:
            person.quarantined()
        else:
            pass

    # person start social distancing by chance given
    def distancing(self, arbiter=0, space=0, data=0):
        if self.deceased or self.quarantine:
            pass
        elif self.susceptible_time == 0:
            self.social_distancing = True
            if DAY_START_DISTANCING > 0:
                if self.shape_sd_c == 0:
                    SPACE.add(self.shape_sd)

    # person that are not social distancing
    def normal(self, arbiter=0, space=0, data=0):
        self.susceptible_time += 1

    # person stop social distancing
    def distancing_end(self, arbiter=0, space=0, data=0):
        if self.social_distancing_time >= DAY * DAY_SOCIAL_DISTANCING_END:
            self.social_distancing = False
            if DAY_START_DISTANCING > 0:
                if self.shape_sd_c == 0:
                    self.shape_sd_c += 1
                    SPACE.remove(self.shape_sd)

    # deceased person
    def died(self):
        if self.infected_time >= DAY * RECOVERY_TIME:
            self.infected = False
            self.recovered = False
            self.susceptible = False
            self.quarantine = False
            self.deceased = True
            self.deceased_time += 1
            self.body.velocity = 0, 0
            self.shape.density = 10000
            self.shape.collision_type = POPULATION + 2

    # recovered person
    def recover(self):
        if self.infected_time >= DAY * RECOVERY_TIME:
            self.infected = False
            self.deceased = False
            self.susceptible = False
            self.quarantine = False
            self.recovered = True
            self.recovered_time += 1
            self.shape.density = 1
            self.shape.collision_type = POPULATION + 3

    # infected person transmission chance controller
    def infect(self, space=0, arbiter=0, data=0):
        if 0 <= max(DAY_COUNT) < DAY_START_MASK:
            if random.randint(1, 100) <= TRANSMISSION_CHANCE:
                self.infected = True
                self.susceptible = False
                self.shape.collision_type = POPULATION + 1
            else:
                self.infected = False
        elif DAY_START_MASK <= max(DAY_COUNT) < DAY_MASK_END:
            if random.randint(1, 100) <= TRANSMISSION_CHANCE - (MASK_APPLICATION / 100 * TRANSMISSION_CHANCE):
                self.infected = True
                self.susceptible = False
                self.shape.collision_type = POPULATION + 1
            else:
                self.infected = False
        elif DAY_MASK_END <= max(DAY_COUNT):
            if random.randint(1, 100) <= TRANSMISSION_CHANCE:
                self.infected = True
                self.susceptible = False
                self.shape.collision_type = POPULATION + 1
            else:
                self.infected = False

    # for n person infected in the beginning of simulation
    def n_infect(self, space=0, arbiter=0, data=0):
        self.infected = True
        self.susceptible = False
        self.shape.collision_type = POPULATION + 1

    # person get vaccinated
    def vaccine(self, arbiter=0, space=0, data=0):
        if self.deceased or self.recovered or self.infected or self.quarantine:
            pass
        elif random.randint(1, 100) <= VACCINATION_CHANCE:
            self.susceptible = False
            self.vaccinate = True
            self.shape.collision_type = POPULATION + 4
            self.shape.density = 1

    # infected person get quarantined
    def quarantined(self, arbiter=0, space=0, data=0):
        if self.infected and random.randint(1, 100) <= QUARANTINE_CHANCE:
            self.quarantine = True
            self.body.velocity = 0, 0
            self.shape.collision_type = POPULATION + 5
            self.shape.density = 10000

    # drawing person
    def draw_person(self):
        x, y = self.body.position
        if self.social_distancing and self.infected:
            pygame.draw.circle(WIN, RED, (int(x), int(y)), SIZE)
            pygame.draw.circle(WIN, WHITE, (int(x), int(y)), SIZE * 2, 1)
        if self.social_distancing and self.recovered:
            pygame.draw.circle(WIN, BLUE, (int(x), int(y)), SIZE)
            pygame.draw.circle(WIN, WHITE, (int(x), int(y)), SIZE * 2, 1)
        elif self.social_distancing and self.vaccinate:
            pygame.draw.circle(WIN, PURPLE, (int(x), int(y)), SIZE)
            pygame.draw.circle(WIN, WHITE, (int(x), int(y)), SIZE * 2, 1)
        elif self.social_distancing and self.susceptible:
            pygame.draw.circle(WIN, WHITE, (int(x), int(y)), SIZE)
            pygame.draw.circle(WIN, WHITE, (int(x), int(y)), SIZE * 2, 1)
        elif self.quarantine and self.infected:
            pygame.draw.circle(WIN, RED, (int(x), int(y)), SIZE)
            pygame.draw.circle(WIN, YELLOW, (int(x), int(y)), SIZE + 2, 2)
        elif self.infected:
            pygame.draw.circle(WIN, RED, (int(x), int(y)), SIZE)
        elif self.recovered:
            pygame.draw.circle(WIN, BLUE, (int(x), int(y)), SIZE)
        elif self.deceased:
            pygame.draw.circle(WIN, GREEN, (int(x), int(y)), SIZE)
        elif self.vaccinate:
            pygame.draw.circle(WIN, PURPLE, (int(x), int(y)), SIZE)
        elif self.susceptible:
            pygame.draw.circle(WIN, WHITE, (int(x), int(y)), SIZE)


class City(object):
    """
    Creating city by creating border all around the screen to contain people
    """

    def __init__(self, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, BORDER_WIDTH * 2)
        self.shape.elasticity = 1
        SPACE.add(self.body, self.shape)

    # drawing the city's border
    def draw(self):
        pygame.draw.line(WIN, WHITE, self.shape.a, self.shape.b, BORDER_WIDTH * 2)

    @staticmethod
    def city_border():
        border_right = City((WIDTH - 10 - BORDER_WIDTH / 2, 10), (WIDTH - 10 - BORDER_WIDTH / 2, HEIGHT - 10))
        border_left = City((9 + BORDER_WIDTH / 2, 10), (9 + BORDER_WIDTH / 2, HEIGHT - 10))
        border_top = City((10, 9 + BORDER_WIDTH / 2), (WIDTH - 10, 9 + BORDER_WIDTH / 2))
        border_bottom = City((10 + BORDER_WIDTH / 2, HEIGHT - 10 - BORDER_WIDTH / 2),
                             (WIDTH - 10 - BORDER_WIDTH / 2, HEIGHT - 10 - BORDER_WIDTH / 2))
        return border_right, border_left, border_top, border_bottom


class GateRight(object):
    """
    The city is divide into four areas: top-right, top-left, bottom-right, bottom-left
    right gate divide top-right area with bottom-right area
    """

    def __init__(self, x, y, c1, c2):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, y
        self.shape = pymunk.Segment(self.body, c1, c2, BORDER_WIDTH)
        self.shape.elasticity = 1
        self.shape.collision_type = POPULATION + 50
        self.lck_c = LOCKDOWN / 2
        self.lck_a = 50 + self.lck_c
        self.lck_b = 50 - self.lck_c
        self.ad_c = 0
        self.speed_x = -PERSON_SPEED / A_DAY
        self.speed_y = PERSON_SPEED / A_DAY

    # create adding function to create gate in the middle of simulation
    def add_right(self, gate_right):
        if self.ad_c == 0:
            SPACE.add(self.body, self.shape)
            self.ad_c += 1

    # drawing the gate
    def draw(self):
        p1 = self.body.local_to_world(self.shape.a)
        p2 = self.body.local_to_world(self.shape.b)
        pygame.draw.line(WIN, WHITE, p1, p2, BORDER_WIDTH)

    # moving the gate
    def open_right(self, open=True):
        if open and (self.body.local_to_world(self.shape.a)[0]) >= (WIDTH / 2 + 5) + \
                (self.lck_b / 100 * (WIDTH / 2 + 5)):
            self.body.velocity = self.speed_x, 0
        else:
            self.body.velocity = self.speed_y, 0

    @staticmethod
    def gate_right_return(gate_right):
        gate_right.open_right(False)


class GateLeft(GateRight):
    """
    Left gate divide top-left area with bottom-left area
    """

    def add_left(self, gate_left):
        if self.ad_c == 0:
            SPACE.add(self.body, self.shape)
            self.ad_c += 1

    def open_left(self, open=True):
        if open and self.body.local_to_world(self.shape.a)[0] <= self.lck_a / 100 * (WIDTH / 2 + 5):
            self.body.velocity = self.speed_y, 0
        else:
            self.body.velocity = self.speed_x, 0

    @staticmethod
    def gate_left_return(gate_left):
        gate_left.open_left(False)


class GateTop(GateRight):
    """
    Top gate divide top-right area with top-left area
    """

    def add_top(self, gate_top):
        if self.ad_c == 0:
            SPACE.add(self.body, self.shape)
            self.ad_c += 1

    def open_top(self, open=True):
        if open and self.body.local_to_world(self.shape.a)[1] <= self.lck_a / 100 * (HEIGHT / 2):
            self.body.velocity = 0, self.speed_y
        else:
            self.body.velocity = 0, self.speed_x

    @staticmethod
    def gate_top_return(gate_top):
        gate_top.open_top(False)


class GateBottom(GateRight):
    """
    Bottom gate divide bottom-right area with bottom-left area
    """

    def add_bottom(self, gate_bottom):
        if self.ad_c == 0:
            SPACE.add(self.body, self.shape)
            self.ad_c += 1

    def open_bottom(self, open=True):
        if open and self.body.local_to_world(self.shape.a)[1] >= (HEIGHT / 2) + (self.lck_b / 100 * (HEIGHT / 2)):
            self.body.velocity = 0, self.speed_x
        else:
            self.body.velocity = 0, self.speed_y

    @staticmethod
    def gate_bottom_return(gate_bottom):
        gate_bottom.open_bottom(False)


class DataCollection:
    """
    Manipulating data from the simulation; collecting, plotting, printing, showing
    """

    # storing data in these list
    @staticmethod
    def active_count(recovered_ctf, infected_ctf, susceptible_ctf, deceased_ctf, vaccinated_ctf, quarantined_ctf,
                     social_distancing_ctf, lockdown_ctf, mask_ctf, day_pass):
        RECOVERED_COUNT.append(recovered_ctf)
        INFECTED_COUNT.append(infected_ctf)
        SUSCEPTIBLE_COUNT.append(susceptible_ctf)
        DECEASED_COUNT.append(deceased_ctf)
        VACCINATED_COUNT.append(vaccinated_ctf)
        QUARANTINE_COUNT.append(quarantined_ctf)
        SOCIAL_DISTANCING_COUNT.append(social_distancing_ctf)
        LOCKDOWN_COUNT.append(lockdown_ctf)
        MASK_COUNT.append(mask_ctf)
        DAY_COUNT.append(day_pass)

    # plotting data
    @staticmethod
    def plotting():
        fig = plt.figure(facecolor='w')
        ax = fig.add_subplot(111, facecolor='#dddddd', axisbelow=True)
        if SMOOTH_PLOT:
            ax.plot(SUSCEPTIBLE_COUNT, 'black', label='Susceptible')
            ax.plot(INFECTED_COUNT, 'red', label='Infected')
            ax.plot(RECOVERED_COUNT, 'blue', label='Recovered')
            ax.plot(DECEASED_COUNT, 'green', label='Deceased')
            if DAY_START_VACCINE == 0:
                pass
            else:
                ax.plot(VACCINATED_COUNT, label='Vaccinated')
            if DAY_START_QUARANTINE == 0:
                pass
            else:
                ax.plot(QUARANTINE_COUNT, label='Quarantined')
            if DAY_START_DISTANCING == 0:
                pass
            else:
                ax.plot(SOCIAL_DISTANCING_COUNT, label='Social Distancing')
            if DAY_START_LOCKDOWN == 0:
                pass
            else:
                ax.plot(LOCKDOWN_COUNT, label='Lockdown Period')
            if DAY_START_MASK == 0:
                pass
            else:
                ax.plot(MASK_COUNT, label='Masking Period')
            ax.set_xlabel('Raw Time or Days')
        else:
            ax.plot(DAY_COUNT, SUSCEPTIBLE_COUNT, label='Susceptible')
            ax.plot(DAY_COUNT, INFECTED_COUNT, label='Infected')
            ax.plot(DAY_COUNT, RECOVERED_COUNT, label='Recovered')
            ax.plot(DAY_COUNT, DECEASED_COUNT, label='Deceased')
            if DAY_START_VACCINE == 0:
                pass
            else:
                ax.plot(DAY_COUNT, VACCINATED_COUNT, label='Vaccinated')
            if DAY_START_QUARANTINE == 0:
                pass
            else:
                ax.plot(DAY_COUNT, QUARANTINE_COUNT, label='Quarantined')
            if DAY_START_DISTANCING == 0:
                pass
            else:
                ax.plot(DAY_COUNT, SOCIAL_DISTANCING_COUNT, label='Social Distancing')
            if DAY_START_LOCKDOWN == 0:
                pass
            else:
                ax.plot(DAY_COUNT, LOCKDOWN_COUNT, label='Lockdown Period')
            if DAY_START_MASK == 0:
                pass
            else:
                ax.plot(MASK_COUNT, label='Masking Period')
            ax.set_xlabel('Time or Days')
        ax.set_ylabel('Population')
        plt.legend()
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)
        plt.show()

    # printing data to the screen or into xlsx file
    @staticmethod
    def printing(file_name):
        df = pandas.DataFrame({
            'Susceptible': SUSCEPTIBLE_COUNT, 'Infected': INFECTED_COUNT,
            'Recovered': RECOVERED_COUNT, 'Deceased': DECEASED_COUNT,
            'Quarantine': QUARANTINE_COUNT, 'Vaccinated': VACCINATED_COUNT,
            'Social Distancing': SOCIAL_DISTANCING_COUNT, 'Lockdown Period': LOCKDOWN_COUNT,
            'Masking Period': MASK_COUNT, 'Day': DAY_COUNT
        })
        if DATA_TO_EXCEL:
            df.to_excel(str(file_name) + ".xlsx", sheet_name=str(file_name))
            print("Data has been collected in " + str(file_name) + ".xlsx sheet's name " + str(file_name))
        else:
            print(df)

    # now data to the screen
    @staticmethod
    def data_screen(text, x, y):
        print_text = FONT.render(text, True, BLACK)
        WIN.blit(print_text, (x, y))


vac_count_helper = [DAY_START_VACCINE]
qua_count_helper = [DAY_START_QUARANTINE]
class Timer:
    """
    Create and tracking time for time related functions
    """

    @staticmethod
    def a_day(time_tracking):
        day_pass = time_tracking / (FPS * A_DAY)
        return int(day_pass)

    # social distancing happen only once in the whole epidemic
    @staticmethod
    def distancing_day(day_pass):
        if day_pass == 0:
            pass
        else:
            if DAY_START_DISTANCING == 0:
                pass
            elif s[0] == DAY_START_DISTANCING and s[-1] == DAY_START_DISTANCING:
                return True
            else:
                pass

    # vaccination happens multiple times
    @staticmethod
    def vaccinate_day(day_pass):
        if day_pass == 0:
            pass
        else:
            if DAY_START_VACCINE == 0 or DAY_SCHEDULED_VACCINE == 0:
                pass
            elif DAY_START_VACCINE == vac_count_helper[-1] and s[0] / DAY_START_VACCINE == 1 \
                    and s[-1] / DAY_START_VACCINE == 1:
                return True
            elif s[0] % (vac_count_helper[-1] + DAY_SCHEDULED_VACCINE) == 0 \
                    and s[-1] % (vac_count_helper[-1] + DAY_SCHEDULED_VACCINE) == 0:
                vac_count_helper.append(s[-1])
                return True
            else:
                pass

    # quarantine happens multiple times
    @staticmethod
    def quarantine_day(day_pass):
        if day_pass == 0:
            pass
        else:
            if DAY_START_QUARANTINE == 0 or DAY_SCHEDULED_QUARANTINE == 0:
                pass
            elif DAY_START_QUARANTINE == qua_count_helper[-1] and s[0] / DAY_START_QUARANTINE == 1 \
                    and s[-1] / DAY_START_QUARANTINE == 1:
                return True
            elif s[0] % (qua_count_helper[-1] + DAY_SCHEDULED_QUARANTINE) == 0 \
                    and s[-1] % (qua_count_helper[-1] + DAY_SCHEDULED_QUARANTINE) == 0:
                qua_count_helper.append(s[-1])
                return True
            else:
                pass

    # a day loop, a function that's return True value every seconds which is a day in simulation
    @staticmethod
    def day_loop(day_pass):
        if day_pass == 0:
            pass
        else:
            if A_DAY == 0:
                pass
            elif s[0] == s[-1]:
                return True
            else:
                pass


class Simulation:
    # main game/simulation loop
    @staticmethod
    def main(file_name='DPES'):
        # spawn person
        susceptible = [Person(random.randint(20, WIDTH - 20), random.randint(20, HEIGHT - 20))
                       for _ in range(POPULATION)]

        # create collision handler
        for i in range(1, POPULATION + 1):
            susceptible[i - 1].shape.collision_type = i
            handler = SPACE.add_collision_handler(i, POPULATION + 1)
            handler.separate = susceptible[i - 1].infect

        # infect 1 people (n) to start the epidemic
        random.choice(susceptible).n_infect()

        # create border around the city/screen
        border_right, border_left, border_top, border_bottom = City.city_border()

        # create gate as separation between areas inside the city/screen
        gate_right = GateRight((WIDTH / 2 + 5 - BORDER_WIDTH / 2) +
                               ((WIDTH / 2 + 5 - BORDER_WIDTH / 2) * abs(LOCKDOWN - 100) / 100),
                               HEIGHT / 2 - BORDER_WIDTH / 2, (0, 0), (WIDTH / 2 - 13 - BORDER_WIDTH / 2, 0))
        gate_left = GateLeft(10 + BORDER_WIDTH / 2, HEIGHT / 2 - BORDER_WIDTH / 2, (0, 0),
                             ((WIDTH / 2 - 5 - (BORDER_WIDTH / 2)) -
                              ((WIDTH / 2 - 5 - (BORDER_WIDTH / 2)) * abs(LOCKDOWN - 100) / 100), 0))
        gate_top = GateTop(WIDTH / 2 - 5 - BORDER_WIDTH / 2, 10, (10, 0),
                           (10, ((HEIGHT / 2 - 10) - ((HEIGHT / 2 - 10) * abs(LOCKDOWN - 100) / 100))))
        gate_bottom = GateBottom(WIDTH / 2 + 5 - BORDER_WIDTH / 2,
                                 ((HEIGHT / 2 - BORDER_WIDTH / 2) +
                                  ((HEIGHT / 2 - BORDER_WIDTH / 2) * abs(LOCKDOWN - 100) / 100)),
                                 (0, 0), (0, HEIGHT / 2 - 10 - BORDER_WIDTH / 2))

        time_tracking = 0
        clock = pygame.time.Clock()
        run = True
        pause = False
        data_sn = False
        while run:
            clock.tick(FPS)
            # quitting simulation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            # pausing simulation
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_SPACE]:
                pause = True
            elif key_pressed[pygame.K_c]:
                pause = False

            if not pause:
                # called function block
                time_tracking += 1
                day_pass = Timer.a_day(time_tracking)
                s.append(day_pass)
                day_start_distancing = Timer.distancing_day(day_pass)
                if DAY_SCHEDULED_VACCINE == 1:
                    day_scheduled_vaccinate = Timer.day_loop(day_pass)
                else:
                    day_scheduled_vaccinate = Timer.vaccinate_day(day_pass)
                if DAY_SCHEDULED_QUARANTINE == 1:
                    day_scheduled_quarantine = Timer.day_loop(day_pass)
                else:
                    day_scheduled_quarantine = Timer.quarantine_day(day_pass)
                susceptible_ctf = POPULATION
                infected_ctf = 0
                recovered_ctf = 0
                deceased_ctf = 0
                vaccinated_ctf = 0
                social_distancing_ctf = 0
                quarantined_ctf = 0
                lockdown_ctf = 0
                mask_ctf = 0

                # drawing block
                WIN.fill(BLACK)
                border_right.draw()
                border_left.draw()
                border_top.draw()
                border_bottom.draw()

                # lockdown control measure
                if DAY_LOCKDOWN_END == 0 or DAY_START_LOCKDOWN == 0:
                    pass
                else:
                    if DAY_LOCKDOWN_END > day_pass >= DAY_START_LOCKDOWN:
                        lockdown_ctf = POPULATION
                        gate_right.add_right(gate_right)
                        gate_left.add_left(gate_left)
                        gate_top.add_top(gate_top)
                        gate_bottom.add_bottom(gate_bottom)
                        gate_right.draw()
                        gate_left.draw()
                        gate_top.draw()
                        gate_bottom.draw()
                    elif (DAY_LOCKDOWN_END + (abs(WIDTH / PERSON_SPEED))) >= day_pass >= DAY_LOCKDOWN_END:
                        lockdown_ctf = 0
                        GateRight.gate_right_return(gate_right)
                        GateLeft.gate_left_return(gate_left)
                        GateTop.gate_top_return(gate_top)
                        GateBottom.gate_bottom_return(gate_bottom)
                        gate_right.draw()
                        gate_left.draw()
                        gate_top.draw()
                        gate_bottom.draw()

                if DAY_START_MASK == 0 or DAY_MASK_END == 0:
                    pass
                else:
                    if 0 <= day_pass < DAY_START_MASK:
                        mask_ctf = 0
                    elif DAY_START_MASK <= day_pass < DAY_MASK_END:
                        mask_ctf = POPULATION
                    elif DAY_MASK_END <= day_pass:
                        mask_ctf = 0

                # spawning block
                for person in susceptible:
                    person.draw_person()
                    person.day_time()
                    person.distancing_end()

                    # data capture
                    if person.infected:
                        infected_ctf += 1
                        susceptible_ctf -= 1
                    if person.recovered:
                        recovered_ctf += 1
                        susceptible_ctf -= 1
                    if person.deceased:
                        deceased_ctf += 1
                        susceptible_ctf -= 1
                    if person.vaccinate:
                        vaccinated_ctf += 1
                        susceptible_ctf -= 1
                    if person.social_distancing:
                        social_distancing_ctf += 1
                    if person.quarantine:
                        quarantined_ctf += 1

                    # quarantine control measures
                    if day_pass >= DAY_START_QUARANTINE and day_scheduled_quarantine:
                        person.get_quarantined(person)

                    # vaccination control measures
                    if day_pass >= DAY_START_VACCINE and day_scheduled_vaccinate:
                        person.get_vaccinated(person)

                    # social distancing control measure
                    if day_start_distancing:
                        person.decide_to_distance(person)

                    # infected person end time
                    if person.recovered_time >= 1 or person.deceased_time >= 1:
                        continue
                    else:
                        person.recovered_or_deceased(person)

                # collecting data
                DataCollection.active_count(recovered_ctf, infected_ctf, susceptible_ctf, deceased_ctf, vaccinated_ctf,
                                            quarantined_ctf, social_distancing_ctf, lockdown_ctf, mask_ctf, day_pass)
                SPACE.step(1 / FPS)

            # showing now data
            if key_pressed[pygame.K_d]:
                data_sn = True
            elif key_pressed[pygame.K_f]:
                data_sn = False

            # printing now data
            if data_sn:
                stats = pygame.Surface((340, 320))
                stats.fill(WHITE)
                stats.set_alpha(200)
                stats_pos = (10, 10)
                WIN.blit(stats, stats_pos)
                fps = str(int(clock.get_fps()))
                DataCollection.data_screen(f"FPS = {fps}", 20, 20)
                DataCollection.data_screen(f"Day = {str(DAY_COUNT[-1])} days", 20, 40)
                DataCollection.data_screen(f"Population = {str(POPULATION - DECEASED_COUNT[-1])} people", 20, 60)
                DataCollection.data_screen(f"Transmission Chance = {str(TRANSMISSION_CHANCE)} %", 20, 80)
                DataCollection.data_screen(f"Mortality Rate = {str(MORTALITY_RATE)} %", 20, 100)
                DataCollection.data_screen(f"Recovery Time = {str(RECOVERY_TIME)} day", 20, 120)
                DataCollection.data_screen(f"Susceptible = {str(SUSCEPTIBLE_COUNT[-1])} people", 20, 140)
                DataCollection.data_screen(f"Infected = {str(INFECTED_COUNT[-1])} people", 20, 160)
                DataCollection.data_screen(f"Recovered = {str(RECOVERED_COUNT[-1])} people", 20, 180)
                DataCollection.data_screen(f"Deceased = {str(DECEASED_COUNT[-1])} people", 20, 200)
                DataCollection.data_screen(f"Social Distancing = {str(SOCIAL_DISTANCING_COUNT[-1])} people", 20, 220)
                DataCollection.data_screen(f"Quarantine = {str(QUARANTINE_COUNT[-1])} people", 20, 240)
                DataCollection.data_screen(f"Vaccinated = {str(VACCINATED_COUNT[-1])} people", 20, 260)
                if LOCKDOWN_COUNT[-1] == POPULATION:
                    DataCollection.data_screen(f"Lockdown = Yes " + str(LOCKDOWN) + "%", 20, 280)
                else:
                    DataCollection.data_screen(f"Lockdown = No", 20, 280)
                if MASK_COUNT[-1] == POPULATION:
                    DataCollection.data_screen(f"Face Mask = Yes " + str(MASK_APPLICATION) + "%",
                                               20, 300)
                else:
                    DataCollection.data_screen(f"Face Mask = No", 20, 300)

            # quit simulation when there is no infected people left
            if min(INFECTED_COUNT) == 0:
                run = False

            pygame.display.update()
        pygame.quit()

        # plotting or printing the captured data or both
        if SHOW_AS_PLOT and SHOW_AS_DATA:
            DataCollection.printing(file_name)
            DataCollection.plotting()
        elif SHOW_AS_PLOT:
            DataCollection.plotting()
        elif SHOW_AS_DATA:
            DataCollection.printing(file_name)

    # testing
    @staticmethod
    def test():
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.set_mode((200, 200)).fill(BLACK)
            pygame.draw.circle(WIN, PURPLE, (200 / 2, 200 / 2), 10)
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    """ The file name where the data is stored and written in xlsx by default is 'DPES' you can change it by entering a 
    new file name in the main() function parameter as in the example below: """
    Simulation.main()
    # Simulation.main('action_10')

# How to Operate the Simulation
"""
1. You need to set some parameters in global variable first
2. To see the overall data from the simulation you need to set value of SHOW_AS_PLOT or SHOW_AS_DATA to True, 
    the captured data will be shown after the simulation is complete
3. Run this code by executing in the terminal
4. While simulation run you can:
    a. Press Space key to pause
    b. Press C key to unpause
    c. Press D key to show now data from simulation
    d. Press F key to stop showing now data
5. To quit simulation you can just close the simulation window or wait until there is no infected person left inside the 
    simulation
"""

# How to Run Simulation with Various Scenarios as Examples
"""
 This scenarios are few examples that can be run in this program
 To run this scenarios you need to set several parameters in advance to enter the scenario that will happen in this 
epidemic and then executing the program files through the terminal. These following are the criteria in the parameters
for many scenarios, keep in mind that the value you can input must be an integer:
    0. Basic SIRD Epidemic
    You need to set this variables as a standard SIRD epidemic simulation
    Set this as stable variables if you want to test the control measures
        A_DAY = 1
        POPULATION = 300
        SIZE = 10
        PERSON_SPEED = 10
        TRANSMISSION_CHANCE = 75
        MORTALITY_RATE = 25 
        RECOVERY_TIME = 15
    
    1. Without precautions
    Set everything to 0 and simulation will run without control measures
        DAY_START_MASK = 0 
        MASK_APPLICATION = 0 
        DAY_MASK_END = 0  
        DAY_START_DISTANCING = 0  
        SOCIAL_DISTANCING_RATE = 0  
        DAY_SOCIAL_DISTANCING_END = 0  
        DAY_START_QUARANTINE = 0  
        DAY_SCHEDULED_QUARANTINE = 0  
        QUARANTINE_RATE = 0  
        QUARANTINE_CHANCE = 0  
        DAY_START_VACCINE = 0  
        DAY_SCHEDULED_VACCINE = 0  
        VACCINATION_RATE = 0  
        VACCINATION_CHANCE = 0 
        DAY_START_LOCKDOWN = 0  
        LOCKDOWN = 0  
        DAY_LOCKDOWN_END = 0  

    2. The effect of using a mask is 25% effective to prevent infection
    Set the value in mask control measures and set anything else to 0
        DAY_START_MASK = 15
        MASK_APPLICATION = 25 
        DAY_MASK_END = 100
        
    3. The effect of using a mask is 50% effective to prevent infection
    Set the value in mask control measures and set anything else to 0
        DAY_START_MASK = 15
        MASK_APPLICATION = 50 
        DAY_MASK_END = 100
        
    4. Effect 25% of the population conducts social distancing
    Set the value in social distancing control measures and set anything else to 0
        DAY_START_DISTANCING = 20
        SOCIAL_DISTANCING_RATE = 25  
        DAY_SOCIAL_DISTANCING_END = 100
        
    5. Effect 50% of the population conducts social distancing
    Set the value in social distancing control measures and set anything else to 0
        DAY_START_DISTANCING = 20
        SOCIAL_DISTANCING_RATE = 50  
        DAY_SOCIAL_DISTANCING_END = 100
        
    6. Effect 25% of the infected population are quarantined with 75% symptomatic
    Set the value in quarantine control measures and set anything else to 0
        DAY_START_QUARANTINE = 20
        DAY_SCHEDULED_QUARANTINE = 3  
        QUARANTINE_RATE = 25
        QUARANTINE_CHANCE = 75
        
    7. Effect 50% of the infected population are quarantined with 75% symptomatic
    Set the value in quarantine control measures and set anything else to 0
        DAY_START_QUARANTINE = 20
        DAY_SCHEDULED_QUARANTINE = 3  
        QUARANTINE_RATE = 50
        QUARANTINE_CHANCE = 75
        
    8. Effect 25% of the population is vaccinated with a 95% vaccine success rate 
    Set the value in vaccine control measures and set anything else to 0
        DAY_START_VACCINE = 30
        DAY_SCHEDULED_VACCINE = 2  
        VACCINATION_RATE = 25
        VACCINATION_CHANCE = 95
        
    9. Effect 50% of the population is vaccinated with a 95% vaccine success rate 
    Set the value in vaccine control measures and set anything else to 0
        DAY_START_VACCINE = 30
        DAY_SCHEDULED_VACCINE = 2  
        VACCINATION_RATE = 50
        VACCINATION_CHANCE = 95
        
    10. 90% lockdown
    Set the value in lockdown control measures and set anything else to 0
        DAY_START_LOCKDOWN = 15 
        LOCKDOWN = 90
        DAY_LOCKDOWN_END = 50
        
    11. 100% lockdown
    Set the value in lockdown control measures and set anything else to 0
        DAY_START_LOCKDOWN = 15 
        LOCKDOWN = 100
        DAY_LOCKDOWN_END = 50
        
    12. Combination from number 2, 4, 6, 8, and 10
        DAY_START_MASK = 15
        MASK_APPLICATION = 25 
        DAY_MASK_END = 100
        DAY_START_DISTANCING = 20
        SOCIAL_DISTANCING_RATE = 25  
        DAY_SOCIAL_DISTANCING_END = 100
        DAY_START_QUARANTINE = 20
        DAY_SCHEDULED_QUARANTINE = 3  
        QUARANTINE_RATE = 25
        QUARANTINE_CHANCE = 75
        DAY_START_VACCINE = 30
        DAY_SCHEDULED_VACCINE = 2  
        VACCINATION_RATE = 25
        VACCINATION_CHANCE = 95
        DAY_START_LOCKDOWN = 15 
        LOCKDOWN = 90
        DAY_LOCKDOWN_END = 50
        
    13. Combination from number 3, 5, 7, 9, and 11
        DAY_START_MASK = 15
        MASK_APPLICATION = 50 
        DAY_MASK_END = 100
        DAY_START_DISTANCING = 20
        SOCIAL_DISTANCING_RATE = 50  
        DAY_SOCIAL_DISTANCING_END = 100
        DAY_START_QUARANTINE = 20
        DAY_SCHEDULED_QUARANTINE = 3  
        QUARANTINE_RATE = 50
        QUARANTINE_CHANCE = 75
        DAY_START_VACCINE = 30
        DAY_SCHEDULED_VACCINE = 2  
        VACCINATION_RATE = 50
        VACCINATION_CHANCE = 95
        DAY_START_LOCKDOWN = 15 
        LOCKDOWN = 100
        DAY_LOCKDOWN_END = 50

Read README.txt for more detail to utilize this program!
        
"""
