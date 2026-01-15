#!/bin/bash
# System stats for tmux status bar (macOS)

# CPU usage (normalized by core count)
CORES=$(sysctl -n hw.ncpu)
CPU=$(ps -A -o %cpu | awk -v cores="$CORES" '{sum+=$1} END {printf "%.0f", sum/cores}')

# Memory usage as percentage
TOTAL_BYTES=$(sysctl -n hw.memsize)

MEM_PCT=$(vm_stat | awk -v total_bytes="$TOTAL_BYTES" '
/page size/ { page_size = $8 }
/Pages active/ { active = $3 }
/Pages wired/ { wired = $4 }
/Pages purgeable/ { purgeable = $3 }
END {
    gsub(/\./, "", active)
    gsub(/\./, "", wired)
    gsub(/\./, "", purgeable)
    used_bytes = (active + wired - purgeable) * page_size
    printf "%.0f", (used_bytes / total_bytes) * 100
}')

echo "CPU:${CPU}% MEM:${MEM_PCT}%"
