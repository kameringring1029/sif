#include <iostream>
#include <wiringPi.h>
#include <sys/time.h>
#include <cstdlib>
#include <sys/time.h>
#include <unistd.h>
#include "pca9685.h"

using namespace std;
int main()
{
  if (wiringPiSetupGpio() == -1) {
      std::cout << "cannot setup gpio." << std::endl;
      return 1;
    }

  pinMode(18, PWM_OUTPUT);
  pwmSetMode(PWM_MODE_MS);
  pwmSetClock(400);
  pwmSetRange(1024);

  while (true) {
      int num;
//      std::cin >> num;

 //     if (num == -1) {
//	        break;
//	   }


		
	    pwmWrite(18, 28);
		usleep(300000);
	    pwmWrite(18, 25);
		usleep(300000);
  }

  return 0;
}

