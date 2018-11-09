float tempe;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
   tempe = analogRead(0)*5/1024.0;
   tempe = tempe - 0.5;
   tempe = tempe / 0.01;
   tempe = tempe - 32;
   tempe = tempe * 5/9;
   Serial.println(tempe);
   delay(500);
}
