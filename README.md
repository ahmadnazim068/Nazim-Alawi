# Smart Fun Run Central Dashboard System

## 1. Project Component & Overview
Component Name: Centralized IoT & OS Real-Time Race Dashboard 

This system acts as the core orchestration backend and visual interface for the Smart Fun Run event. Built using a multithreaded Python Flask framework, the server concurrently handles multiple live tracking data feeds. It synchronizes online runner registrations directly from a live Google Sheet endpoint, listens for real-time runner checkpoint tags pulled from a Firebase Real-Time Database, and maintains synchronized state updates. To prevent race conditions and data corruption across these concurrent processing workers, the system implements robust OS Mutex synchronization mechanisms (`data_lock`), exposing data seamlessly to a dynamically updating Cyberpunk HUD web front-end.

## 2. Team Members & Roles
[cite_start]This repository represents the unified engineering efforts of our 9-member sub-group across both IoT and OS disciplines[cite: 6, 44]:

| Name | Matric Number | Core Project Role | Discipline |
| :--- | :--- | :--- | :--- |
| [Your Name Here] | [Your Matric] | [cite_start]OS Lead / Backend Architect [cite: 44] | OS (BNF32303) |
| [OS Member 2] | [Matric 2] | OS Concurrency Developer | OS (BNF32303) |
| [OS Member 3] | [Matric 3] | UI/UX Frontend Engineer | OS (BNF32303) |
| [OS Member 4] | [Matric 4] | Data Pipeline Analyst | OS (BNF32303) |
| [OS Member 5] | [Matric 5] | Technical Writer / QA | OS (BNF32303) |
| [OS Member 6] | [Matric 6] | System Integration Tester | OS (BNF32303) |
| [IoT Member 1] | [Matric 7] | [cite_start]IoT Lead / Firmware Engineer [cite: 44] | IoT (BNF44403) |
| [IoT Member 2] | [Matric 8] | Hardware Prototyping Specialist | IoT (BNF44403) |
| [IoT Member 3] | [Matric 9] | Edge Network Deployment Lead | IoT (BNF44403) |

## 3. Quick Start Guide
[cite_start]Follow these instructions to boot up and test the integrated system locally:

### Prerequisites
Ensure you have Python 3.x installed along with the required execution dependencies:
```bash
pip install flask pandas openpyxl requests
