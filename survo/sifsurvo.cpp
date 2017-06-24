#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <typeinfo>
#include <cstdlib>
#include <sys/time.h>
#include <future>
#include <unistd.h>

#include <wiringPi.h>
#include "pca9685.h"

using namespace std;

#define BTNSLP 70000
#define PIN_BASE 300
#define MAX_PWM 4096
#define HERTZ 50
//#define MILLIS_DEF 0.85
//#define MILLIS_TOUCH 0.55


static int BPM;
static int GPIO[10]={0,5,6,12,13,16,19,20,26,21};

/*文字列分割*/
vector<string> split(const string &str, char delim){
	istringstream iss(str); string tmp; vector<string> res;
	while(getline(iss, tmp, delim)) res.push_back(tmp);
	return res;
}


/**
 * Calculate the number of ticks the signal should be high for the required amount of time
 */
int calcTicks(float impulseMs, int hertz)
{
	float cycleMs = 1000.0f / hertz;
	return (int)(MAX_PWM * impulseMs / cycleMs + 0.5f);
}



/*演奏*/
void playMusic(string gakufu, int gpio, int tick_def, int tick_touch){

	const char* oto;
	oto = gakufu.c_str();


	float millis;
	int tick;

	int i = 0;
	double sleeptime = 0;
	int intsleeptime = 0;
	struct timeval start_timeval, end_timeval;
	double sec_timeofday;

	double tmpsleep = (double)15 / (double)BPM;

	gettimeofday( &start_timeval, NULL );
	while (i < gakufu.size()){

		if (oto[i] == '0'){			/*休符*/
			pwmWrite(PIN_BASE+gpio-1, tick_def);
		} else if (oto[i] == '1'){	/*短押し*/
			pwmWrite(PIN_BASE+gpio-1 , tick_touch);
			usleep(BTNSLP);
			pwmWrite(PIN_BASE+gpio-1 , tick_def);
		} else if (oto[i] == '2'){	/*長押し*/
			pwmWrite(PIN_BASE+gpio-1, tick_touch);
		}

		// calc sleep time
		gettimeofday( &end_timeval, NULL );
		sleeptime = (end_timeval.tv_sec - start_timeval.tv_sec)
					+ (end_timeval.tv_usec - start_timeval.tv_usec) / 1000000.0;
		sleeptime = tmpsleep*(i+1) - sleeptime;
		intsleeptime = (int)(sleeptime * 1000000);
		//cout << intsleeptime << endl;
		usleep(intsleeptime);
		
		i++;
	}

	// 終了処理
	digitalWrite(gpio, 0);

}

/* ボタン */
class button
{
	private:
		int gpio;
		string gakufu;
		int tick_def, tick_touch;
	public:
		void setGakufu(string line, int no);
		void play();
};

void button::setGakufu(string line, int no)
{
	gakufu = line;
	gpio = no;

	if(no <= 5) {
//	if(no <= 9) {
		tick_def = calcTicks(0.85, HERTZ);
		tick_touch = calcTicks(0.55, HERTZ);
	}else{
	//	tick_def = calcTicks(2.43, HERTZ);
	//	tick_touch = calcTicks(2.55, HERTZ);
		tick_def = calcTicks(0, HERTZ);
		tick_touch = calcTicks(0, HERTZ);
	}
}

void button::play()
{
	thread t(playMusic, gakufu, gpio, tick_def, tick_touch);
//	if(gpio==GPIO[9]){
	if(gpio==9){
		t.join();
	}else{
		t.detach();	
	}
}


/* ファイル読み込み */
string readFile (char *filename)
{
	ifstream ifs(filename);
	string file;
	ifs >> file;
	cout << file << endl;

	return file;
}


int main(int argc, char *argv[]){
	vector<string> line;

	button Buttons[10];
	
	// Initialize WiringPi
	if(wiringPiSetupGpio() == -1){
		cout << "GPIO Init error" << endl;
		return 0;
	}

	// Setup with pinbase 300 and i2c location 0x40
	int fd = pca9685Setup(PIN_BASE, 0x40, HERTZ);
	if (fd < 0)
	{
		printf("Error in setup\n");
		return fd;
	}

	// Reset all output
	pca9685PWMReset(fd);

	/* input and set gakufu */
	line = split(readFile(argv[1]), ',');
	BPM = atoi(line[0].c_str());
//	for(int i=1; i<=9; i++) Buttons[i].setGakufu(line[i], GPIO[i]);
	for(int i=1; i<=9; i++) Buttons[i].setGakufu(line[i], i);

	/* wait for start */
	cout << "Press Key to Start" << endl;
	getchar();

	/* play Music */
	for(int i=1; i<=9; i++) Buttons[i].play();

	/* End */
	cout << endl << "End." << endl;
	return 0;
}

