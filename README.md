# IoT_Project

This project is an Internet of Things (IoT) application developed for academic purposes. It consists of a Python Flask web application and an Arduino sketch.

In this project an iot device was developed which collected data on temperature, humidity and light and then sent to the application via cloud. The user could then see these values live and the user could set some threasholds in which the application would send an informative email to the user depending on the weather conditions.

![image](https://github.com/user-attachments/assets/fc4833cd-29ea-4e7a-8cb2-20f00c86c55a)


## Project Structure

```
ergasia.ino                # Arduino source code
secrets.h                  # Arduino secrets/config
app/
  app.py                   # Main Flask application
  send_email.py            # Email sending utility
  .cache.sqlite            # SQLite database
  static/
    css/
      styles.css           # CSS styles
  templates/
    index.html             # Main HTML template
    settings.html          # Settings page template
```

## Features

- **Web Interface:** Built with Flask, provides a user-friendly interface.
- **Email Notifications:** Sends emails using the `send_email.py` utility.
- **Database:** Uses SQLite for data storage.
- **Arduino Integration:** Communicates with an Arduino device using `ergasia.ino`.

## Setup for static version of the site

```sh
git clone https://github.com/Alfonsos-Kotsios/IoT_Project.git
cd app
```

Install dependencies (if not already installed):

```sh
pip install flask
```

### 2. Running the Flask App

```sh
python app.py
```

The web app will be available at `http://127.0.0.1:5000/`.

### 3. Arduino

- Open `ergasia.ino` in the Arduino IDE.
- Update `secrets.h` with your WiFi credentials and other secrets.
- Upload to your Arduino board.

## File Descriptions

- **app/app.py:** Main entry point for the Flask web server.
- **app/send_email.py:** Handles sending emails from the application.
- **app/static/css/styles.css:** Stylesheet for the web interface.
- **app/templates/index.html:** Home page template.
- **app/templates/settings.html:** Settings/configuration page.
- **ergasia.ino:** Arduino sketch for device-side logic.
- **secrets.h:** Contains sensitive configuration for Arduino (not to be shared).

## License

This project is for educational use.

---
