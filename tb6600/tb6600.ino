// define pins numbers
const int TOTAL_STEPPERS = 3;
const int STEPS_PER_REVOLUTION = 200;

const int PUL_PIN[] = { 3,  5,  6};
const int DIR_PIN[] = { 2,  4,  7};
const int  EN_PIN[] = { 8, 12, 13};
const int  SW_PIN[] = {10, 10, 11};

int   totalPulses[] = {10, 5, 3};
float rot_speed     = 10; // rpm
int   interval      = (1000.0*60.0/(rot_speed*STEPS_PER_REVOLUTION))/2.0;


void initializePins(steppers[]) {
    for (int i = 0; i < sizeof(steppers); i++) {
        // set and initialize the pins
        pinMode(PUL_PIN[steppers[i]], OUTPUT);
        pinMode(DIR_PIN[steppers[i]], OUTPUT);
        pinMode( EN_PIN[steppers[i]], OUTPUT);
    }
}

void waitForSerial() {
    Serial.println("[Press Return key to continue]");
    while (Serial.available()) { Serial.read(); }
    while (!Serial.available()) {}
    //Serial.println(Serial.read());
    Serial.println("[Continuing]");
}

void homeStepper(int steppers, int swNumber) {
    Serial.println("\n-- Homing motor(s).");

    // reverse rotation
    for (int i = 0; i < sizeof(steppers); i++) {
        digitalWrite(DIR_PIN[steppers[i]], LOW);
    }

    while(digitalRead(DIR_PIN[steppers[0]]) == LOW) {
        if (digitalRead(SW_PIN[swNumber]) == LOW) {
            // keep moving
            moveSteppers(steppers, 1);
        } else {
            // normal rotation
            for (int i = 0; i < sizeof(steppers); i++) {
                digitalWrite(DIR_PIN[steppers[i]], HIGH);
            }
            delay(interval);

            Serial.print("Motor(s) homed.")
        }
    }
}


void moveSteppers(int steppers[], int totalSteps) {
    if (digitalRead(DIR_PIN[steppers[0]]) == LOW) {
        char sign[] = "-";
    } else {
        char sign[] = "+";
    }

    Serial.print("\n-- Rotating motor(s) ");
    Serial.print(", by ");
    Serial.print(sign);
    Serial.print(totalSteps);
    Serial.println(" steps.");

    // wait for keypress
    waitForSerial();

    for (int step = 0; step < totalSteps; step++) {
        for (int i = 0; i < sizeof(steppers); i++) {
            digitalWrite(DIR_PIN[steppers[i]], HIGH);

            digitalWrite(PUL_PIN[steppers[i]], HIGH);
            delay(interval);

            digitalWrite(PUL_PIN[steppers[i]], LOW);
            delay(interval);

        }

        // show progress
        Serial.print('\r');
        Serial.print("step: ");
        Serial.print(sign);
        Serial.print(step + 1);
        Serial.print("/");
        Serial.print(sign);
        Serial.println(totalSteps);
    }
}

void setup() {
    // start the serial
    Serial.begin(9600);

    // select steppers
    int steppers[3] = {0, 1, 2}

    initializePins(steppers[]);
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
        // TODO
        for (int i = 0; i < sizeof(steppers); i++) {
            moveSteppers(stepper, totalPulses[steppers[i]]);
        }

        Serial.println("----------------------------------------");
        Serial.println("---------------- FINISH ----------------");
        Serial.println("----------------------------------------");
    }
}


