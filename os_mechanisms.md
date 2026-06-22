# OS Mechanisms & Backend Architecture

## 1. Concurrency Control (Mutual Exclusion / Mutex)
The Centralized Dashboard acts as the main API gateway for 4 different microservices. During the live 1.6km run, multiple teams (e.g., Registration and Environmental) might send HTTP POST requests to the server at the exact same millisecond. 
* **Mechanism Applied:** We implemented a `threading.Lock()` (Mutex) in Python. 
* **Justification:** Before any team's data is written to the central `live_system_data` dictionary, the thread must acquire the lock. This creates a **Critical Section**, preventing race conditions, data corruption, and backend crashes under heavy live load.

## 2. Multithreading
* **Mechanism Applied:** The Flask API Gateway runs with `threaded=True`.
* **Justification:** This allows the server to spawn a new thread for every incoming HTTP request. While one thread is locked writing data, other threads can queue up seamlessly without the server freezing or rejecting packets.

## 3. File Management (Logging)
* **Mechanism Applied:** Non-blocking file appending.
* **Justification:** To ensure no data is lost if the server restarts, every incoming POST request payload is written to a local log file (`system_logs.txt`). File handlers are opened and closed cleanly to prevent memory leaks.
