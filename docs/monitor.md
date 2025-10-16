# ML Cluster Monitoring Scripts

A collection of bash scripts for monitoring ML cluster hardware, specifically designed for H100 setups with Ollama.

## Scripts Overview

### 1. `cluster_stats.sh` - Comprehensive Cluster Overview
Shows complete cluster status including:
- GPU summary (H100 count, total VRAM)
- Detailed GPU statistics
- System resources (CPU, memory, disk)
- Running ML workloads
- Network and driver information

```bash
./cluster_stats.sh
```

### 2. `vram_monitor.sh` - Real-time VRAM Usage
Lightweight VRAM monitoring with progress bars:
- Visual progress bars for each GPU
- Color-coded usage levels (green/yellow/red)
- Real-time updates with configurable intervals

```bash
./vram_monitor.sh        # 1-second intervals
./vram_monitor.sh 5      # 5-second intervals
```

### 3. `gpu_monitor.sh` - Comprehensive GPU Monitoring
Detailed real-time GPU monitoring:
- GPU utilization and VRAM usage
- Running processes on each GPU
- Docker container status
- Temperature and power consumption

```bash
./gpu_monitor.sh         # 2-second intervals
./gpu_monitor.sh 1       # 1-second intervals
```

### 4. `ollama_monitor.sh` - Ollama-Specific Monitoring
Monitors Ollama container and GPU usage:
- Container status and health
- API endpoint testing
- GPU processes related to Ollama
- Performance metrics and logs

```bash
./ollama_monitor.sh status    # Show current status
./ollama_monitor.sh monitor   # Real-time monitoring
./ollama_monitor.sh logs      # Show recent logs
./ollama_monitor.sh restart   # Restart container
```

## Setup

1. Make scripts executable:
```bash
chmod +x *.sh
# or run the setup script:
./setup_scripts.sh
```

2. Install dependencies (if not already installed):
```bash
# For progress bars and calculations
sudo apt install bc

# Optional: For better GPU monitoring
sudo apt install nvtop
```

## Quick Commands

For our H100 setup specifically:

```bash
# Quick cluster overview
./cluster_stats.sh

# Real-time VRAM monitoring (recommended for Ollama usage)
./vram_monitor.sh 1

# Monitor Ollama specifically
./ollama_monitor.sh monitor

# Traditional nvidia-smi real-time
nvidia-smi -l 1
```

## Usage Examples

### Monitor VRAM During Ollama Usage
```bash
# Terminal 1: Start VRAM monitoring
./vram_monitor.sh 1

# Terminal 2: Use Ollama
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "your-model", "prompt": "Hello!"}'
```

### Check Cluster Status Before Training
```bash
./cluster_stats.sh
# Verify 4x H100 NVL with ~95GB each = ~380GB total VRAM
```

### Monitor During Model Loading
```bash
./ollama_monitor.sh monitor 1
# Watch VRAM allocation as models load
```

## System Requirements

- NVIDIA drivers with nvidia-smi
- Docker (for container monitoring)
- Basic Unix tools (bc, curl, jq recommended)
- Linux/Unix environment

## Features

- **Color-coded output** for easy reading
- **Progress bars** for VRAM usage visualization
- **Real-time updates** with configurable intervals
- **Process tracking** to see what's using GPU memory
- **Container integration** for Docker/Ollama monitoring
- **Comprehensive stats** including temps, power, utilization

## Your H100 Setup

Based on:
- 4x NVIDIA H100 NVL GPUs
- ~95,830 MB VRAM per GPU (~380GB total)
- Ollama container running on port 11434

These scripts are optimized for this configuration and will help monitor VRAM usage as Ollama loads and runs models.