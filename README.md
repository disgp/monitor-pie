# Monitor Pie v0.1

Monitor Pie is a simple, lightweight, and elegant web-based dashboard for monitoring the real-time CPU and RAM usage of a remote computer. It's designed for users who want a quick visual overview of their system's performance from any device on their local network.

![Monitor Pie Screenshot](Screenshot-2025-11-10-Google Chrome-131413.png)  

---

## Features

- **Real-Time Statistics**: View live CPU and RAM load with updates every 2 seconds.
- **Web-Based Dashboard**: Access the dashboard from any browser on your local network (e.g., a tablet, phone, or another computer).
- **Elegant UI**: A clean, modern interface with liquid-fill gauges provides an intuitive look at system load.
- **Dynamic IP Configuration**: Easily set and change the IP address of the monitored machine directly from the web interface. The address is saved in your browser's local storage, so you only need to set it once.
- **Clear Status Indicators**: The dashboard provides clear visual feedback for different states:
  - **Not Configured**: When the dashboard hasn't been pointed to a machine yet.
  - **Offline**: When the target machine is not reachable on the network.
  - **Disconnected**: When the machine is reachable, but the monitoring script isn't running.
- **Minimal Dependencies**: The backend script only requires Python 3 and the `psutil` library. The frontend is plain HTML, CSS, and JavaScript with no frameworks.

## How It Works

The project has two main components:

1.  **Backend (`monitor.py`)**: A lightweight Python server that runs on the machine you want to monitor (e.g., your MacBook). It uses the `psutil` library to get system stats and serves them as JSON at a `/stats` endpoint.
2.  **Frontend (`index.html`, `style.css`, `script.js`)**: A set of static web files that you can host anywhere (e.g., on a NAS, a Raspberry Pi, or another web server). Your browser loads these files, and the JavaScript then fetches the data from the backend server to display it.

## Setup and Usage

Follow these steps to get your Monitor Pie dashboard running.

### 1. Backend Setup (On the Computer to Monitor)

This script runs on the machine whose stats you want to see (e.g., your MacBook).

- **Prerequisite**: Make sure you have Python 3 installed.
- **Install the required library**: Open your terminal and install `psutil`:
  ```bash
  pip3 install psutil
  ```
- **Run the monitoring script**: In the same terminal, navigate to the project folder and run:
  ```bash
  python3 monitor.py
  ```
  The server will start, and you'll see the message: `Monitoring server started on http://0.0.0.0:8000`. Leave this terminal window running.

### 2. Frontend Setup (On a Web Server or NAS)

Copy the frontend files (`index.html`, `style.css`, `script.js`) to a web-accessible folder on your NAS, Raspberry Pi, or any other web server.

### 3. First-Time Configuration

- **Find the IP Address**: On the computer you are monitoring, find its local IP address. On macOS, you can find this in **System Settings > Network**.
- **Open the Dashboard**: In a browser on any device (like a tablet), navigate to the URL where you placed the frontend files (e.g., `http://your-nas-ip/dashboard/`).
- **Configure the IP**:
  1. You will see a "Not Configured" message. Click the settings icon (⚙️) in the top-right corner.
  2. Enter the IP address of the computer running `monitor.py`.
  3. Click **Save**.

The dashboard will immediately connect and start displaying real-time stats. The IP address is saved in your browser, so you won't have to enter it again unless it changes.
