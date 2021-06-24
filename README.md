# DPES
Dissemination and Prevention Epidemic Simulator (DPES) v 1.0.0 with: SIRD (Susceptible Infected Recovered Deceased) Model with Control Measures (Mask Application, Social Distancing, Quarantine, Vaccination, and Lockdown)
Doc. 18:35 31/03/2021

    This program will simulate epidemic events using the SIRD model, a slightly modified model from the standard  SIR  model. This program also adds epidemic control activities as an effort to reduce the rate of infection, including: mask application, social distancing, quarantine, vaccination and lockdown.
    You can set the simulation run via global parameters. Following are the basic simulation elements you can change to adjust the simulation run:
    
    # Elements
    FPS = 60
        -> Frame per second, the higher the number the smoother the simulation will run, 60 is smooth enough 
    A_DAY = 1
        -> To set how long the days are in the simulation. By default 1 day is equal to 1 second. Value must be an integer and not 0.
    BORDER_WIDTH = 2
         -> To set the thickness of city's border, 1 to 10 pixel is preferable
    SHOW_AS_PLOT = False
        -> After the simulation is complete the recorded simulation data will be displayed. If you want to display data
            into graphic form, set this value to True and the data will be displayed in matplotlib format.
    SHOW_AS_DATA = False
        -> Data can also be displayed raw. Set this value to True then the data will be displayed on the screen in 
            tabular form. You can also set where this raw data is displayed using next parameters.
    SMOOTH_PLOT = True
        -> For a smoother graphic, set this value to True, then the data displayed by matplotlib will look smoother.
            Please note that the x axis on this graph is not based on per day as which have been determined so that for
            a more accurate x axis based on the time per day set this value to False, the data will be shown per day 
            (1 second).
    DATA_TO_EXCEL = False
        -> Set this value to True if you want to record simulation data into an xlsx file. Set this value to False if 
            you want to display data on the screen in tabular form.
        -> If you want to display data in graphical form and also want to view it in tabular form then set the
            SHOW_AS_PLOT and SHOW_AS_DATA value become True.

    # Epidemic's Elements
    POPULATION = 500
        -> The number of people in the simulation, does not increase and remains. Value must be an integer and not 0.
    SIZE = 5
        -> The size of the person in the simulation, in pixels. Value must be an integer and not 0.
    SPEED_x, SPEED_y = -100, 100
        -> In pixels. To change how fast it moves in the simulation. As a comparison of people with a size of 5 pixels 
            at least move up to a maximum speed of 10 pixels. Also used to move the area separation gate. Value must be 
            an integer.
    TRANSMISSION_CHANCE = 100
        -> How effectively can the disease be transmitted from infected to susceptible. Value must be an integer between
            0 up to 100 (in percent).
    MORTALITY_RATE = 50
        -> How effectively the disease can cause death for the infected person. Value must be an integer between 0 up to 100
            (in percent).
    RECOVERY_TIME = 21
        -> How long does it take for the disease to heal / disappear, in day's unit. Value must be an integer and not 0.
 
# How to Operate the Simulation
1. You need to set some parameters inside global variable first
2. Run this code by executing in the terminal
3. While simulation run you can:
    a. Press Space key to pause
    b. Press C key to unpause
    c. Press D key to show now data from simulation
    d. Press F key to stop showing now data
4. To quit simulation you can just close the simulation window or wait until there is no infected person left inside the simulation

# How to Run Simulation with Various Scenarios as Examples
This scenarios are few examples that can be run in this program
 To run this scenarios you need to set several parameters in advance to enter the scenario that will happen in this epidemic and then executing the program files through the terminal. These following are the criteria in the parameters for many scenarios, keep in mind that the value you can input must be an integer:
    0. Basic SIRD Epidemic
    You need to set this variables as a standard SIRD epidemic simulation
    Set this as stable variables if you want to test the control measures
        A_DAY = 1
        POPULATION = 300
        SIZE = 10
        SPEED_x, SPEED_y = -20, 20
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
