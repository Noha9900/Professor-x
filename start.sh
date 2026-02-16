#!/bin/bash
# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

ARIA2C=$1
SABNZBDPLUS=$2

tracker_list=$(curl -Ns https://ngosang.github.io/trackerslist/trackers_all_http.txt | awk '$0' | tr '\n\n' ',')

# PROFESSOR-X ULTRA SPEED TWEAKS
$ARIA2C --allow-overwrite=true --auto-file-renaming=true --bt-enable-lpd=true --bt-detach-seed-only=true \
       --bt-remove-unselected-file=true --bt-tracker="[$tracker_list]" --bt-max-peers=0 --enable-rpc=true \
       --rpc-max-request-size=1024M \
       --max-connection-per-server=16 \
       --max-concurrent-downloads=2000 \
       --split=16 \
       --min-split-size=5M \
       --seed-ratio=0 \
       --check-integrity=true --continue=true --daemon=true \
       --disk-cache=128M \
       --file-allocation=falloc \
       --force-save=true \
       --follow-torrent=mem --check-certificate=false \
       --optimize-concurrent-downloads=true \
       --http-accept-gzip=true --max-file-not-found=0 --max-tries=10 \
       --peer-id-prefix=-qB4520- --reuse-uri=true \
       --content-disposition-default-utf8=true \
       --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
       --peer-agent=qBittorrent/4.5.2 --quiet=true \
       --summary-interval=0 --max-upload-limit=1K

cpulimit -l 40 -- $SABNZBDPLUS -f sabnzbd/SABnzbd.ini -s :::8070 -b 0 -d -c -l 0 --console

source .venv/bin/activate && python3 update.py && python3 -m bot
