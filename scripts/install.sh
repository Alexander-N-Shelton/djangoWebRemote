#!/bin/bash

echo "Updating system and installing dependencies..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git android-tools-adb

echo "Setting up WebRemote in /opt/web-remote..."
sudo mkdir -p /opt/web-remote
sudo chown $USER:$USER /opt/web-remote
cd /opt/web-remote

echo "Cloning webRemote..."
git clone https://github.com/Alexander-N-Shelton/webRemote.git .

echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Make and Apply Django migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Adding Navigation Buttons..."
python manage.py shell < scripts/setup_navigation_buttons.py

echo "Adding Favorite Buttons..."
python manage.py shell < scripts/setup_favorites_buttons.py

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating Django superuser..."
echo -e "Default administrator:\nusername = admin\npassword = password"
python manage.py shell < scripts/create_default_superuser.py

sudo tee /opt/web-remote/.env > /dev/null <<EOF
DJANGO_SECRET_KEY=$(openssl rand -hex 32)
EOF

echo "Creating systemd service..."
sudo tee /etc/systemd/system/web-remote.service > /dev/null <<EOF
[Unit]
Description=Web Remote Django Service
After=network.target

[Service]
User=$USER
WorkingDirectory=/opt/web-remote
EnvironmentFile=/opt/web-remote/.env
ExecStart=/opt/web-remote/venv/bin/python manage.py runserver 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo "Enabling and starting the web-remote service..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable web-remote
sudo systemctl start web-remote

echo "Allowing traffic on port 8000 through UFW (if active)..."
sudo ufw allow 8000

echo "Setup complete. Access the remote at: http://$(hostname -I | awk '{print $1}'):8000"
