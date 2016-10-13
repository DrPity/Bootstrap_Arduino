void checkSerial() {
  if (Serial.available() > 0){
    inByte = Serial.readStringUntil(lf);
    inByte.trim();

    if(inByte.indexOf('#') == 0){
      Serial.print("Serial works");   // check serial
      Serial.println();
    }
  }
}
