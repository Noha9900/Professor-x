# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

from flask import Flask, render_template
from professorx import LOGGER, bot_start_time
from professorx.helper.ext_utils.status_utils import get_readable_time
import time

app = Flask(__name__)

@app.route('/')
def index():
    uptime = get_readable_time(time.time() - bot_start_time)
    return render_template('index.html', uptime=uptime)

def start_web_server():
    LOGGER.info("Professor-X Web Dashboard Starting on Port 80...")
    # Standard server config
    app.run(host='0.0.0.0', port=80)
