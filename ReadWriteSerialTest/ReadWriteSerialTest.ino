/*
 * Name: Riley Becker, adapted from https://www.youtube.com/watch?v=UeybhVFqoeg
 * and from https://www.youtube.com/watch?v=AHr94RtMj1A
 * Date: 5/18/25
 * Purpose: Uses a Python Virtual Environment to create a feedback loop between the Arduino and Python
*/
//Output pins
const int redPin = 3;
const int greenPin = 5;

//Pin numbers
const int VRY = A1;
const int VRX = A0;
const int SW = 7;

//Printing values (LR, UD)
int LR;
int UD;

void setup() {
  Serial.begin(9600);
  pinMode(greenPin, OUTPUT);
  pinMode(redPin, OUTPUT);
}

void loop() {

  //Print message from the 
  String msg;
  if(Serial.available() > 0) {
    msg = Serial.readString();

    if(msg == "ON") {
      digitalWrite(greenPin, HIGH);
    }
    else if(msg == "OFF") {
      digitalWrite(greenPin, LOW);
    }
    else {
      for(int i = 0; i < 5; i++) {
        digitalWrite(redPin, HIGH);
        delay(150);
        digitalWrite(redPin, LOW);
        delay(150);
      }
    }
  }

  //Read joystick analog values
  LR = analogRead(VRX);
  UD = analogRead(VRY);

  //Print joystick values
  Serial.print("LR: ");
  Serial.print(LR);
  Serial.print(" UD: ");
  Serial.println(UD);
  delay(1000);

}
