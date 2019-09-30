#define LENGTH(array) ( sizeof(array)/sizeof(array[0]) )

#define MOVE(steppers) { \
    waitForSerial(); \
    shiftArr(LENGTH(steppers), steppers, -1); \
    moveSteppers(LENGTH(steppers), steppers, totalSteps[steppers[1]]); \
    shiftArr(LENGTH(steppers), steppers, +1); \
}

#define HOME(steppers) { \
    waitForSerial(); \
    shiftArr(3, steppers, -1); \
    homeSteppers(LENGTH(steppers), steppers); \
    shiftArr(3, steppers, +1); \
}


// steppers
const int VERT_BAR_STEPPERS[]   = {1, 2};
const int HORIZ_STOP_STEPPERS[] = {3};

const int STEPS_PER_REVOLUTION = 200;

// pins numbers
const int PUL_PIN[] = { 3,  5,  6};
const int DIR_PIN[] = { 2,  4,  7};
const int  EN_PIN[] = { 8, 12, 13};
const int  SW_PIN[] = {10, 10, 11};

// motion parameters
int   totalSteps[] = {10, 10, 5};
float rot_speed    = 1; // rpm
int   interval     = 1000.0*60.0/(rot_speed*STEPS_PER_REVOLUTION)/2.0;


void initializePins() {
    for (int i = 0; i < LENGTH(PUL_PIN); i++) {
        // set and initialize the pins
        pinMode(PUL_PIN[i], OUTPUT);
        pinMode(DIR_PIN[i], OUTPUT);
        pinMode( EN_PIN[i], OUTPUT);
        pinMode( SW_PIN[i], INPUT_PULLUP);
        
        digitalWrite(DIR_PIN[i], HIGH); // positive direction
    }
}

void waitForSerial() {
    Serial.println("\n[Press Return key to continue]");
    while (Serial.available()) { Serial.read(); }
    while (!Serial.available()) {}
    //Serial.println(Serial.read());
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

    // reverse rotation
    for (int i = 0; i < stepperCount; i++) {
        digitalWrite(DIR_PIN[steppers[i]], LOW);
    }

    while(digitalRead(DIR_PIN[steppers[0]]) == LOW) {
        if (digitalRead(SW_PIN[steppers[0]]) == HIGH) {
            // limit switch not pressed, keep moving
            moveSteppers(stepperCount, steppers, 1);
        } else {
            // forward rotation
            for (int i = 0; i < stepperCount; i++) {
                digitalWrite(DIR_PIN[steppers[i]], HIGH);
            }
            delay(interval);

        }
    }

    Serial.println("\n== Homing finished.");
}

void moveSteppers(int stepperCount, int steppers[], int totalSteps) {
    char sign;
    if (digitalRead(DIR_PIN[steppers[0]]) == LOW) {
        sign = '-';
    } else {
        sign = '+';
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
        Serial.print('\r');
        Serial.print("step: ");
        Serial.print(sign);
        Serial.print(step + 1);
        Serial.print("/");
        Serial.print(sign);
        Serial.println(totalSteps);
    }

    Serial.println("-- Rotating finished.");
}

void setup() {
    // start the serial
    Serial.begin(9600);

    // itialize pins
    initializePins();
}

void loop() {
    Serial.flush();

    while(1) {
        // show info
        Serial.println("----------------------------------------");
        Serial.println("---------------- START -----------------");
        Serial.println("----------------------------------------");
        Serial.print("Rotational speed = ");
        Serial.print(rot_speed);
        Serial.println(" rpm");

        // home and move vertical bar's stepper pair
        HOME(VERT_BAR_STEPPERS);
        MOVE(VERT_BAR_STEPPERS);

        // home and move horizontal panel stop's stepper pair
        HOME(HORIZ_STOP_STEPPERS);
        MOVE(HORIZ_STOP_STEPPERS);

        Serial.println("----------------------------------------");
        Serial.println("---------------- FINISH ----------------");
        Serial.println("----------------------------------------");

        // wait for keypress
        waitForSerial();

    }
}

