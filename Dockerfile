# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

FROM anasty17/mltb-repo:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

# Install system dependencies for TTV and Web UI
RUN apt-get update && apt-get install -y ffmpeg python3-pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# Grant execution rights to the startup script
RUN chmod +x start.sh

# Professor-X Startup command
CMD ["bash", "start.sh"]
