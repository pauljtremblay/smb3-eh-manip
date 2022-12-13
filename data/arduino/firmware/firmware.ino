///////////////////////////////////////////////////////////////////////////////
// RetroSpy Firmware for Arduino Uno & Teensy 3.5
// v4.4
// RetroSpy written by zoggins of RetroSpy Technologies
// NintendoSpy originally written by jaburns

#include "common.h"

void setup()
{
    // for MODE_DETECT
#if defined(__arm__) && defined(CORE_TEENSY)
    for (int i = 33; i < 40; ++i)
        pinMode(i, INPUT_PULLUP);
#else
    PORTC = 0xFF; // Set the pull-ups on the port we use to check operation mode.
    DDRC = 0x00;
#endif

    Serial.begin(115200);
    common_pin_setup();

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-value"
    T_DELAY(5000);
    A_DELAY(200);
#pragma GCC diagnostic pop
}

void waitForInputPoll()
{
    unsigned char bits = NES_BITCOUNT;
    WAIT_LEADING_EDGE(NES_LATCH);

    do
    {
        WAIT_FALLING_EDGE(NES_CLOCK);
    } while (--bits > 0);
}

void loop()
{
    waitForInputPoll();
    sendTimeDiff();
    T_DELAY(5);
}
