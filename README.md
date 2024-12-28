# MonitoringBot

A lightweight Telegram bot for monitoring server health. This bot provides real-time CPU usage, CPU temperature, and RAM statistics, while sending alerts if thresholds are exceeded. Designed to work exclusively on Linux systems.

---

## Features

- Real-time server statistics: CPU usage, CPU temperature, RAM utilization.
- Alerts for exceeding thresholds (e.g., high temperature or CPU load).
- Configurable alert limits.
- Token management through an external file.
- Easily configurable for auto-start as a `systemd` service.

---

## Prerequisites

### System Requirements

1. **Operating System**: Linux (required).
2. **Python**: Version 3.6 or higher.
3. **lm-sensors**: Required for monitoring CPU temperature.

### Install and Configure `lm-sensors`

1. Install `lm-sensors`:

   **For Debian/Ubuntu-based systems**:
   ```bash
   sudo apt update
   sudo apt install lm-sensors
   ```

   **For Red Hat/CentOS-based systems**:
   ```bash
   sudo yum install lm_sensors
   ```

2. Configure and detect sensors:
   ```bash
   sudo sensors-detect
   ```
   - Follow the on-screen prompts to scan your hardware and detect available sensors.
   - When asked, accept defaults unless you have specific requirements.

3. Verify that sensors are working:
   ```bash
   sensors
   ```
   You should see temperature readings for your CPU cores and other supported components.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/MonitoringBot.git
   cd MonitoringBot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the bot's token:
   - The bot reads its token from a file named `token` in the root directory. If this file does not exist, it will be created automatically with placeholder text.
   - Open the `token` file and replace its contents with your Telegram Bot API token:
     ```
     PUT YOUR TG API TOKEN HERE
     ```

4. Configure alert thresholds in the script if needed:
   ```python
   # Example threshold values:
   cpu_limit = 60  # CPU usage limit in percent
   temp_limit = 60  # CPU temperature limit in Celsius
   ram_limit = 80  # RAM usage limit in percent
   ```

---

## Usage

### Commands

- `/stats`: Displays current server statistics, including CPU usage, CPU temperature, RAM usage, and available RAM. Indicates whether monitoring is enabled.
- `/start_monitoring`: Starts the monitoring process. The bot will send alerts if any thresholds are exceeded.

### Running the Bot Manually

1. Start the bot:
   ```bash
   python MonitoringBot.py
   ```

2. Use the commands mentioned above in your Telegram chat.

---

### Running the Bot as a `systemd` Service

To ensure the bot starts automatically at system boot:

1. Create a `systemd` unit file:
   ```bash
   sudo nano /etc/systemd/system/MonitoringBot.service
   ```

2. Add the following configuration:
   ```ini
   [Unit]
   Description=Telegram MonitoringBot
   After=network.target

   [Service]
   Type=simple
   User=your_user
   WorkingDirectory=/path/to/your/bot
   ExecStart=/path/to/your/bot/venv/bin/python /path/to/your/bot/MonitoringBot.py
   Restart=always
   RestartSec=5
   Environment="PYTHONUNBUFFERED=1"

   [Install]
   WantedBy=multi-user.target
   ```
   Replace `/path/to/your/bot` with the actual directory containing the bot.

3. Reload `systemd` to apply changes:
   ```bash
   sudo systemctl daemon-reload
   ```

4. Enable the service to start at boot:
   ```bash
   sudo systemctl enable MonitoringBot.service
   ```

5. Start the service:
   ```bash
   sudo systemctl start MonitoringBot.service
   ```

6. Check the service status:
   ```bash
   sudo systemctl status MonitoringBot.service
   ```

7. View logs if necessary:
   ```bash
   sudo journalctl -u MonitoringBot.service -e
   ```

---

## Notes

- **Linux Only**: This bot is not compatible with other operating systems.
- **Dependencies**: Ensure all Python dependencies are installed using the provided `requirements.txt` file.
- **lm-sensors Configuration**: Always run `sensors-detect` after installing `lm-sensors` to configure hardware monitoring correctly.
- **Customizable Intervals**: Modify the `metrics_frequency` variable in the script to set how often the bot checks server metrics (default is 20 seconds).
- **Token Management**: The bot will not run until a valid Telegram Bot API token is provided in the `token` file.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contributing

Contributions are welcome! Feel free to fork this repository, submit issues, or create pull requests to enhance the bot.

