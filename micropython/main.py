from machine import Pin, PWM
import time

r_servo = PWM(Pin(2))
l_servo = PWM(Pin(3))

r_servo.freq(50)
l_servo.freq(50)

#function to set the angle of the servos
def set_angle(servo, angle):
    angle = max(0,min(180, angle))
    duty = int (1638 + (angle/180) * (8192-1638))
    servo.duty_u16(duty)

#The actual speed function will be controlled using an html/js page hosted on the wifi so that the pico can access it
#But for the time being, I will just code a basic speed function
def speed_dps(speed):
    return 5+(speed-1)*15

#Takes the current angle and then moves it to the target angle and returns the target angle as the new current angle
#Moves based on the calculated step from the sleep time and the speed from speed_dps()
def move(current, target, servo, dps):
    sleep_time = 0.02
    step = dps * sleep_time
    while abs(current-target)> step:
        if current < target:
            current+=step
        else:
            current-=step
        set_angle(servo, current)
        time.sleep(sleep_time)
    set_angle(servo,target)
    return target

curr_r = 0
curr_l = 180
speed = int(input("Enter a speed from 1-10"))
dps = speed_dps(speed)

while True:
    #servo horns will be in their respective positions that will allow one to go 
    #from 0 degrees to 90 degrees and one from 90 degrees to 180 degrees
    curr_r = move(curr_r,0, r_servo, dps)
    curr_l = move(curr_l,180, l_servo, dps)

    time.sleep(0.3)

    curr_r = move(curr_r,180, r_servo, dps)
    curr_l = move(curr_l,0, l_servo, dps)

    time.sleep(0.3)