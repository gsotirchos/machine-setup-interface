// define pins numbers
const int TOTAL_STEPPERS = 3;
const int STEPS_PER_REVOLUTION = 200;

const int PUL_PIN[] = {3,  5,  6};
const int DIR_PIN[] = {2,  4,  7};
const int  EN_PIN[] = {8, 12, 13};

int   totalPulses[] = {10, 5, 3};
float rot_speed     = 10; // rpm
int   interval      = (1000.0*60.0/(rot_speed*STEPS_PER_REVOLUTION))/2.0;


void initializePins() {
    for (int stepper = 0; stepper < TOTAL_STEPPERS; stepper++) {
        // set and initialize the pins
        pinMode(PUL_PIN[stepper], OUTPUT);
        pinMode(DIR_PIN[stepper], OUTPUT);
        pinMode( EN_PIN[stepper], OUTPUT);
    }
}

void waitForSerial() {
    Serial.println("[Press Return key to continue]");
    while (Serial.available()) { Serial.read(); }
    while (!Serial.available()) {}
    //Serial.println(Serial.read());
    Serial.println("[Continuing]");
}

void motorSteps(int stepper, int totalSteps) {
    Serial.print("\n-- Rotating motor ");
    Serial.print(stepper + 1);
    Serial.print(", by ");
    Serial.print(totalSteps);
    Serial.println(" steps.");

    // wait for keypress
    waitForSerial();

    for (int step = 0; step < totalSteps; step++) {
        digitalWrite(DIR_PIN[stepper], HIGH);

        digitalWrite(PUL_PIN[stepper], HIGH);
        delay(interval);

        digitalWrite(PUL_PIN[stepper], LOW);
        delay(interval);

        // show progress
        Serial.print('\r');
        Serial.print("step: ");
        Serial.print(step + 1);
        Serial.print("/");
        Serial.println(totalSteps);
    }
}

void setup() {
    // start the serial
    Serial.begin(9600);

    initializePins();
}

void loop() {
    Serial.flush();

    while(1) {
        // wait for keypress
        waitForSerial();

        // show info
        Serial.println("----------------------------------------");
        Serial.println("---------------- START -----------------");
        Serial.println("----------------------------------------");
        Serial.print("Rotational speed = ");
        Serial.print(rot_speed);
        Serial.println(" rpm");

        // Send steps to every stepper
        for (int stepper = 0; stepper < TOTAL_STEPPERS; stepper++) {
            motorSteps(stepper, totalPulses[stepper]);
        }

        Serial.println("----------------------------------------");
        Serial.println("---------------- FINISH ----------------");
        Serial.println("----------------------------------------");
    }
}


