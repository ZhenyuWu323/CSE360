#include "SensorSuite.h"

// SensorSuite::SensorSuite() {}

// SensorSuite::~SensorSuite() {
//     // Clean-up code if needed, e.g., delete sensor instances if owned
// }

void SensorSuite::startup() {
    // bnoSensor = new BNO85();
    // barometer = new Barometer();
    // batterySensor = new WeightedBatterySensor();
    SensorSuite::getPreferences();
    bnoSensor.startup();
    barometer.startup();
    batterySensor.startup();
    for (int i = 0; i < 15; i++) {
        sensorValues[i] = 0;
    }
}


bool SensorSuite::update() {
    bool updated = false;
    int tempCount = 0, offset = 0;

    // Update and read values from barometer, if updated
    if (barometer.update()) {
        float* baroValues = barometer.readValues(tempCount);
        for(int i = 1; i < tempCount-1; ++i) {
            sensorValues[offset + i -1] = baroValues[i];
        }
        offset += tempCount;
        updated = true;
        sensorValues[2] = sensorValues[2] * 0.9 + baroValues[3] * 0.1;
    }
    offset = 3;
    // Repeat the pattern for bnoSensor and batterySensor
    if (!updated) {// prevent both baro and bno update on same tick.
        if (bnoSensor.update()) {
            float* bnoValues = bnoSensor.readValues(tempCount);
            for(int i = 0; i < tempCount; ++i) {
                sensorValues[offset + i] = bnoValues[i];
            }
            offset += tempCount;
            updated = true;
        }
    }
    offset = 10;
    if (batterySensor.update()) {
        float* batteryValues = batterySensor.readValues(tempCount);
        for(int i = 0; i < tempCount; ++i) {
            sensorValues[offset + i] = batteryValues[i];
        }
        offset += tempCount;
        updated = true;
    }

    valueCount = offset; // Update the total number of valid sensor values stored
    return updated;
}

float* SensorSuite::readValues(int& count) {
    count = valueCount; // Return the count of valid sensor values
    return sensorValues; // Return the array of sensor values
}



void SensorSuite::getPreferences() {
    bnoSensor.getPreferences();
    barometer.getPreferences();
    batterySensor.getPreferences();
    return;

}