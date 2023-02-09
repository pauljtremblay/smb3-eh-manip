Retrospy/Arduino Configuration
==============================

The hardware retrospy usually uses is an arduino, a neat microcontroller
we will use to listen to inputs. We will connect to it via a serial connection,
so henceforth I will just refer to "arduino" as the hardware and "serial"
as the connection.

Assuming you have retrospy working, we will flash a new firmware that
communicates with our tool and tweak some configuration variables
to disable video and enable serial.

Arduino firmware
----------------

1. Download+install arduino IDE here: [arduino.cc downloads](https://www.arduino.cc/en/software)
2. Open `firmware.ino` in the data/arduino directory
3. In the upper left press the "Verify" button. It should say "Done Compiling" in the green status bar.
4. Next to verify, click the "Upload" button. This will flash the special code to your arduino.
5. You are done configuring the arduino :)

Tool configuration
------------------

1. Open up config.ini
2. Add a line for `auto_detect_lag_frames_serial = true`

Using ONLY serial and not video for starting and autoresets
-----------------------------------------------------------

1. Add a line for `enable_serial_autoreset = true`. You need to use the original cart and hold the reset button for >2 seconds for this to work.
2. Add a line for `enable_opencv = false`