/*
 * Name: Riley Becker, adapted from https://www.youtube.com/watch?v=UeybhVFqoeg
 * Date: 5/18/25
 * Purpose: Uses Python to send test output into into an Elego Uno
*/
//Output pins
const int redPin = 3;
const int greenPin = 5;


void setup() {
  Serial.begin(9600);
  pinMode(greenPin, OUTPUT);
  pinMode(redPin, OUTPUT);
}

void loop() {
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

}
