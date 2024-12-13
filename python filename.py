import RPi.GPIO as GPIO

# Set the GPIO pins for the motor
motor_pin_1 = 18
motor_pin_2 = 22

# Set the PWM frequency
pwm_frequency = 50

# Initialize the PWM pins
pwm_1 = GPIO.PWM(motor_pin_1, pwm_frequency)
pwm_2 = GPIO.PWM(motor_pin_2, pwm_frequency)

# Start the PWM signals
pwm_1.start(0)
pwm_2.start(0)

# Set the motor speed
motor_speed = 50

# Set the PWM duty cycles
pwm_1.ChangeDutyCycle(motor_speed)
pwm_2.ChangeDutyCycle(100 - motor_speed)

# Wait for 1 second
time.sleep(1)

# Stop the PWM signals
pwm_1.stop()
pwm_2.stop()

# Clean up the GPIO
GPIO.cleanup()
