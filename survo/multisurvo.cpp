#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <mcp23017.h>
#include <sys/time.h>
#include <cstdlib>
#include <sys/time.h>
#include <unistd.h>

using namespace std;

#define BUTTON1 0       // MCP23017 GPA0
#define BUTTON2 1       // MCP23017 GPA1
#define LED1    2       // MCP23017 GPA2
#define LED2    3       // MCP23017 GPA3
#define PINBASE 100

int main(int argc, char **argv) {
    int i;

    if (mcp23017Setup(PINBASE,0x40) == -1){
        printf("Setup Fail\n");
        exit(1);
    }

	pinMode(PINBASE+BUTTON1, PWM_OUTPUT);
	pwmSetMode(PWM_MODE_MS);
	pwmSetClock(400);
	pwmSetRange(1024);

  while (true) {
	pwmWrite(PINBASE+BUTTON1, 28);
	usleep(300000);
	pwmWrite(PINBASE+BUTTON1, 25);
	usleep(300000);
  }

/*
    for(i=0;i<20;i++) {
        if(digitalRead(PINBASE+BUTTON1)) {
            digitalWrite(PINBASE+LED1,1);
        }
        delay(500);
    }
    digitalWrite(PINBASE+LED1,0);
    digitalWrite(PINBASE+LED2,0);
*/

}

