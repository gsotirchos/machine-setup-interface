#define LENGTH(array) ( sizeof(array)/sizeof(array[0]) )

#define HOME(steppers) { \
    waitForSerial(); \
    shiftArr(LENGTH(steppers), steppers, -1); \
    homeSteppers(LENGTH(steppers), steppers); \
    shiftArr(LENGTH(steppers), steppers, +1); \
}

#define MOVE(steppers) { \
    waitForSerial(); \
    Serial.print("\n-- Insert steps: "); \
    totalSteps = readFromSerial(); \
    Serial.println(totalSteps); \
    shiftArr(LENGTH(steppers), steppers, -1); \
    moveSteppers(LENGTH(steppers), steppers, totalSteps); \
    shiftArr(LENGTH(steppers), steppers, +1); \
}

// steppers
int VERT_BAR_STEPPERS[]   = {1, 2};
int VERT_STOP_STEPPERS[] = {3};

const int STEPS_PER_REVOLUTION = 200;

// pins numbers
const int PUL_PIN[] = {3, 6, 11};
const int DIR_PIN[] = {2, 7, 12};
const int  EN_PIN[] = {4, 8, 13};
const int  SW_PIN[] = {5, 9, 10};

// motion parameters
int   totalSteps = 0;
float rot_speed  = 10; // rpm
float interval   = 1000.0*60.0/(rot_speed*STEPS_PER_REVOLUTION)/2.0;

void initializePins() {
    for (int i = 0; i < LENGTH(PUL_PIN); i++) {
        // set and initialize the pins
        pinMode(PUL_PIN[i], OUTPUT);
        pinMode(DIR_PIN[i], OUTPUT);
        pinMode( EN_PIN[i], OUTPUT);
        pinMode( SW_PIN[i], INPUT_PULLUP);
        
        digitalWrite(DIR_PIN[i], HIGH); // forward rotation
    }
}

void waitForSerial() {
    Serial.println("\n[Press Return key to continue]");
    while (Serial.available()) { Serial.read(); }
    while (!Serial.available()) {}
    //Serial.println(Serial.read()); // print read value
    Serial.println("[Continuing]");
}

void shiftArr(int arrayLength, int array[], int value) {
    for (int i = 0; i < arrayLength; i++) {
        array[i] += value;
    }
}

void SerialPrintSteppers(int stepperCount, int steppers[]) {
    Serial.print("[");
    Serial.print(steppers[0] + 1);

    for (int i = 1; i < stepperCount; i++) {
        Serial.print(", ");
        Serial.print(steppers[i] + 1);
    }

    Serial.print("]");
}

void homeSteppers(int stepperCount, int steppers[]) {
    Serial.print("\n== Homing motor(s) ");
    SerialPrintSteppers(stepperCount, steppers);
    Serial.println(".");

    int finished = 0;

    // reverse rotation for return to home position
    for (int i = 0; i < stepperCount; i++) {
        digitalWrite(DIR_PIN[steppers[i]], HIGH);
    }

    while(1) {
        for (int i = 0; i < stepperCount; i++) {
            if (digitalRead(SW_PIN[steppers[i]]) == HIGH) {
                // limit switch not pressed, keep moving
                moveSteppers(1, &steppers[i], 1);
            } else {
                // change to forward rotation
                Serial.print(" ----- Limit switch on pin ");
                Serial.print(SW_PIN[steppers[i]]);
                Serial.println(" closed.");
            }
        }

        finished = 1;
        for (int i = 0; i < stepperCount; i++) {
            if (digitalRead(SW_PIN[steppers[i]]) == HIGH) {
                finished = 0;
            }
        }

        if (finished == 1) {
            for (int i = 0; i < stepperCount; i++) {
                digitalWrite(DIR_PIN[steppers[i]], LOW);
            }
            break;
        }

        delay(interval);
    }

    Serial.println("\n== Homing finished.");
}

void moveSteppers(int stepperCount, int steppers[], int totalSteps) {
    String sign;
    if (digitalRead(DIR_PIN[steppers[0]]) == LOW) {
        sign = "-";
    } else {
        sign = "+";
    }

    Serial.print("\n-- Rotating motor(s) ");
    SerialPrintSteppers(stepperCount, steppers);
    Serial.print(" by ");
    Serial.print(sign);
    Serial.print(totalSteps);
    Serial.println(" step(s).");

    for (int step = 0; step < totalSteps; step++) {
        for (int i = 0; i < stepperCount; i++) {
            digitalWrite(PUL_PIN[steppers[i]], HIGH);
        }
        delay(interval);

        for (int i = 0; i < stepperCount; i++) {
            digitalWrite(PUL_PIN[steppers[i]], LOW);
        }
        delay(interval);

        // show progress
        Serial.println(
            "step: " + sign + (step + 1) + "/" + sign + totalSteps
        );
    }

    Serial.println("-- Rotating finished.");
}

int readFromSerial() {
    Serial.flush();
    String inputString = "";

    // Read integer value from serial input:
    Serial.read();
    while (1) {
        while (!Serial.available()) {}
        inputString = Serial.readStringUntil('\n');

        if (inputString.toInt() > 0) {
            // convert the incoming byte to a char
            // and add it to the string
            return inputString.toInt();
        } else {
            Serial.println("Please insert a positive integer.");
        }
    }
}

void setup() {
    // start the serial
    Serial.begin(9600);

    // itialize pins
    initializePins();
}

void loop() {
    Serial.flush();

    // show info
    Serial.println("----------------------------------------");
    Serial.println("---------------- START -----------------");
    Serial.println("----------------------------------------");
    Serial.print("Rotational speed = ");
    Serial.print(rot_speed);
    Serial.println(" rpm");
    Serial.print("Interval = ");
    Serial.print(interval);
    Serial.println(" ms");

    // home and move vertical bar's stepper pair
    //HOME(VERT_BAR_STEPPERS);
    //MOVE(VERT_BAR_STEPPERS);

    // home and move horizontal panel stop's stepper pair
    HOME(VERT_STOP_STEPPERS);
    MOVE(VERT_STOP_STEPPERS);

    Serial.println("----------------------------------------");
    Serial.println("---------------- FINISH ----------------");
    Serial.println("----------------------------------------");

    // wait for keypress
    waitForSerial();
}

