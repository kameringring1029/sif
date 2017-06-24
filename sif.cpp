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

using namespace std;


#define btnslp 70000

static int BPM;
static int GPIO[10]={0,5,6,12,13,16,19,20,26,21};

/*文字列分割*/
vector<string> split(const string &str, char delim){
	istringstream iss(str); string tmp; vector<string> res;
	while(getline(iss, tmp, delim)) res.push_back(tmp);
	return res;
}



/*演奏*/
void playMusic(string gakufu, int gpio){

	const char* oto;
	oto = gakufu.c_str();

	// Set GPIO pin to output mode
	pinMode(gpio, OUTPUT);


	int i = 0;
	double sleeptime = 0;
	int intsleeptime = 0;
	struct timeval start_timeval, end_timeval;
	double sec_timeofday;

	double tmpsleep = (double)15 / (double)BPM;

	gettimeofday( &start_timeval, NULL );
	while (i < gakufu.size()){

		if (oto[i] == '0'){			/*休符*/
			digitalWrite(gpio, 0);
		} else if (oto[i] == '1'){	/*短押し*/
			digitalWrite(gpio, 1);
			usleep(btnslp);
			digitalWrite(gpio, 0);
		} else if (oto[i] == '2'){	/*長押し*/
			digitalWrite(gpio, 1);
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
	public:
		void setGakufu(string line, int no);
		void play();
};

void button::setGakufu(string line, int no)
{
	gakufu = line;
	gpio = no;
}

void button::play()
{
	thread t(playMusic, gakufu, gpio);
	if(gpio==GPIO[9]){
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

	/* input and set gakufu */
	line = split(readFile(argv[1]), ',');
	BPM = atoi(line[0].c_str());
	for(int i=1; i<=9; i++) Buttons[i].setGakufu(line[i], GPIO[i]);

	/* wait for start */
	cout << "Press Key to Start" << endl;
	getchar();

	/* play Music */
	for(int i=1; i<=9; i++) Buttons[i].play();

	/* End */
	cout << endl << "End." << endl;
	return 0;
}

