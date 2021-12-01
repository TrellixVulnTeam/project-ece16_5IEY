/*
 * Global variables
 */
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;
const int BUTTON_PIN = 14;
const int MOTOR_PIN = 18;
const int FIRE_1 = 12;
const int FIRE_2 = 13;
int ax_arr[100], ay_arr[100], az_arr[100];
int ax_sum, ay_sum, az_sum;
int ax_avg, ay_avg, az_avg;
int buttonState = 1;
unsigned long int lastMoved = 0;
int moveSpeed = 1;
int sensitivity = 1;
unsigned long int buttonSampleTime = 0;
unsigned long int startQuitTime = 0;
bool startedTiming = false;
bool timeUp = 0;
int gameplay = 0;
unsigned long int buzzStart = 0;

/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  sending = false;
  writeDisplay("Calibrating...",1,true);
  writeDisplay("HOLD STILL",2,false);
  int i;
  for(i = 0; i < 100; i++) {
    readAccelSensor();
    ax_arr[i] = ax;
    ay_arr[i] = ay;
    az_arr[i] = az;
    delay(50);
  }
  for(i = 0; i < 100; i++) {
    ax_sum += ax_arr[i];
    ay_sum += ay_arr[i];
  }
  ax_avg = (int)(ax_sum/100);
  ay_avg = (int)(ay_sum/100);
  az_avg = (int)(az_sum/100);
  
  writeDisplay("Ready...", 1, true);
  writeDisplay("Set...", 2, false);
  writeDisplay("Play!", 3, false);
  pinMode(BUTTON_PIN, INPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(FIRE_1,OUTPUT);
  pinMode(FIRE_2,OUTPUT);
}

/*
 * The main processing loop
 */
void loop() {
  // Parse command coming from Python (either "stop" or "start")
  if(ppg != 0) {
    if((ppg < 10000) && (startedTiming == false)) {
      startedTiming = true;
      startQuitTime = millis();
    }
    if((ppg >= 10000) && (startedTiming == true)) {
      startedTiming = false;
      if(millis() - startQuitTime > 3000) {
       gameplay = 2;
      }
      else if(millis() - startQuitTime > 500) {
        gameplay = 1;
      }
      else {
        gameplay = 0;
      }
    }
  }

  if(buttonState == 0) {
    sensitivity++;
     if(sensitivity == 5) {
      sensitivity = 1;
     }
    }

  if((getOrientation() == 1) && (millis() - timeUp > 1000)) {
    moveSpeed++;
    timeUp = millis();
     if(moveSpeed == 5) {
      moveSpeed = 1;
     }
  }
  
  String command = receiveMessage();
  readAccelSensor();
  if(command == "stop") {
    sending = false;
    writeDisplay("Controller: Off", 0, true);
  }
  else if(command == "start") {
    sending = true;
    writeDisplay("Controller: On", 0, true);
  }
  else if(command == "shot") {
    buzzStart = millis();
    digitalWrite(MOTOR_PIN, HIGH);
  }

  if(millis() - buzzStart > 1000) {
    digitalWrite(MOTOR_PIN, LOW);
  }

  // Send the orientation of the board
  if (millis() - lastMoved > (-25*moveSpeed + 125)) {
  if(sending && sampleSensors()) {
    sendMessage(String(getOrientation())+","+String(gameplay));
    lastMoved = millis();
  }
  }
}
