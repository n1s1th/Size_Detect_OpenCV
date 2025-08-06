/*
  Arduino Uno code for receiving two string coordinates from Python over serial,
  controlling robot/slider, then responding with "done" or "fail",
  and finally receiving the sort result ("small" or "large") for further sorting.
*/

String coord1 = "";
String coord2 = "";
String sortResult = "";

void setup() {
  Serial.begin(9600);
  while (!Serial) { ; } // Wait for serial port to connect
}

void loop() {
  coord1 = "";
  coord2 = "";

  // Wait for first coordinate
  while (coord1 == "") {
    if (Serial.available()) {
      coord1 = Serial.readStringUntil('\n');
      coord1.trim();
    }
  }

  // Wait for second coordinate
  while (coord2 == "") {
    if (Serial.available()) {
      coord2 = Serial.readStringUntil('\n');
      coord2.trim();
    }
  }

  // Control robot/slider here using coord1 and coord2
  bool operationSuccess = controlRobotAndSlider(coord1, coord2);

  if (operationSuccess) {
    Serial.println("done");
  } else {
    Serial.println("fail");
    delay(500); // Give Python time to process
    return; // Restart loop, wait for new inputs
  }

  // Wait for sorting result ("small" or "large")
  sortResult = "";
  unsigned long sortTimeout = millis() + 10000; // 10s timeout
  while (sortResult == "" && millis() < sortTimeout) {
    if (Serial.available()) {
      sortResult = Serial.readStringUntil('\n');
      sortResult.trim();
      if (sortResult.length() > 0) {
        break;
      }
    }
  }

  if (sortResult.length() > 0) {
    // Call function to sort object, based on sortResult
    sortObject(sortResult);
  }

  // Loop again for next command
}

// Placeholder for robot/slider control logic
bool controlRobotAndSlider(String c1, String c2) {
  // Add your control code here.
  // Return true if operation succeeded; false otherwise.
  return true;
}

// Placeholder for sorting logic
void sortObject(String result) {
  // Add your sorting code here.
  // result will be "small" or "large"
}
