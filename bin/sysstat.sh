#!/bin/bash
# System stats for tmux status bar (macOS)

# CPU usage (normalized by core count)
CORES=$(sysctl -n hw.ncpu)
CPU=$(ps -A -o %cpu | awk -v cores="$CORES" '{sum+=$1} END {printf "%.0f", sum/cores}')

# Memory usage (matches htop: active + wired - purgeable)
TOTAL_BYTES=$(sysctl -n hw.memsize)
TOTAL_GB=$(echo "scale=1; $TOTAL_BYTES/1024/1024/1024" | bc)

USED_GB=$(vm_stat | awk '
/page size/ { page_size = $8 }
/Pages active/ { active = $3 }
/Pages wired/ { wired = $4 }
/Pages purgeable/ { purgeable = $3 }
END {
    gsub(/\./, "", active)
    gsub(/\./, "", wired)
    gsub(/\./, "", purgeable)
    used = (active + wired - purgeable) * page_size / 1024 / 1024 / 1024
    printf "%.2f", used
}')

echo "CPU:${CPU}% MEM:${USED_GB}G/${TOTAL_GB}G"
