# safe-serve-robot
AI-powered multipurpose robot for restaurant delivery and autonomous fire safety using navigation, obstacle avoidance, and cloud monitoring.
#SAFE-SERVE: A Multipurpose Restaurant Robot & Autonomous Fire Extinguisher

**SAFE-SERVE** is a smart, multipurpose autonomous robot designed for **restaurant automation and fire safety**. It combines **AI/ML-based fire detection**, **autonomous navigation**, **obstacle avoidance**, and **cloud-based data logging** to perform dual functions: **delivering orders** in restaurant settings and **detecting/extinguishing fire hazards** in real-time.

---

## Key Features

- **AI-powered Fire Detection** using computer vision and machine learning
- **Autonomous Fire Extinguishing System** triggered on detection
- **Smart Delivery Bot** that navigates through tables to deliver orders
- **Real-time Obstacle Avoidance** using ultrasonic or LiDAR sensors
- **Cloud-based Monitoring** and logging for performance and alerts
- Battery-efficient route optimization and power management

---

## Technologies Used

| Category              | Tools & Technologies                        |
|-----------------------|---------------------------------------------|
| Hardware              | Raspberry Pi / Arduino / ESP32              |
| Fire Detection        | OpenCV, TensorFlow / YOLO                   |
| Navigation            | Ultrasonic / IR Sensors, Servo motors       |
| Obstacle Avoidance    | Ultrasonic sensors, PID control             |
| Cloud Integration     | Firebase / AWS IoT / Google Cloud           |
| Data Logging & Alerts | MQTT, Firebase Realtime DB, Push Notifications |
| Power Management      | Battery pack, Voltage regulators            |
| Programming           | Python, C/C++, Arduino IDE                  |

---

---

## System Architecture

- Fire detection using live video feed
- If fire is detected:
  - Fire is localized
  - Robot navigates toward the source
  - Extinguisher module activates
  - Event is logged in the cloud
- If delivery mode:
  - Robot scans QR or receives input
  - Navigates to target table
  - Avoids obstacles en route
  - Returns to dock or standby

---

## Use Cases

- **Restaurants**: Contactless delivery and floor navigation
- **Fire-Prone Areas**: Automated emergency response before manual aid
- **Hospitals/Senior Care**: Secure item transport with emergency detection

---

## Future Enhancements

- Add voice interaction with NLP (e.g., order confirmation)
- Integrate GPS and SLAM for larger areas
- Add multi-robot coordination
- Solar-powered charging dock

## Project video link--https://youtu.be/O1jqvkd26KI?si=qTwXCOAdeS3ppcaT


