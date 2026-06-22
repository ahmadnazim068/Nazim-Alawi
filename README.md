# Smart Fun Run Central Dashboard System

## 1. Project Component & Overview
Component Name: Centralized IoT & OS Real-Time Race Dashboard

This system acts as the core orchestration backend and visual interface for the Smart Fun Run event. Built using a multithreaded Python Flask framework, the server concurrently handles multiple live tracking data feeds. It synchronizes online runner registrations directly from a live Google Sheet endpoint, listens for real-time runner checkpoint tags pulled from a Firebase Real-Time Database, and maintains synchronized state updates. To prevent race conditions and data corruption across these concurrent processing workers, the system implements robust OS Mutex synchronization mechanisms (`data_lock`), exposing data seamlessly to a dynamically updating Cyberpunk HUD web front-end.

## 2. Team Members & Roles
This repository represents the unified engineering efforts of our 9-member sub-group across both IoT and OS disciplines:

| Name | Matric Number | Core Project Role | Discipline |
| :--- | :--- | :--- | :--- |
| Name | Matric | OS Lead / IOT lead | COURSE |
| AHMAD NAZIM BIN ALAWI | CN230110 | DASHBOARD FLASK Developer | OS (BNF32303) & IOT (BNF44403) |
| DANESH A/L AJINTA KUMAR  | CN230193 | DASHBOARD FIREBASE Developer | IOT (BNF44403) |

other tema member as runner and media staff

## 3. Quick Start Guide
Follow these instructions to boot up and test the integrated system locally:

### Prerequisites
Ensure you have Python 3.x installed along with the required execution dependencies:
```bash
pip install flask pandas openpyxl requests
