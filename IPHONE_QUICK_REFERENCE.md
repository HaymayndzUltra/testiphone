# iPhone Control Framework - Quick Reference

## 🚀 Quick Start

```bash
# 1. Setup
./iphone_quick_start.sh

# 2. Start System
./START_IPHONE_C2.sh

# 3. Launch Control
python3 control_iphone.py --mode interactive
```

## 📋 Essential Commands

### System Control
```bash
# Start all components
./START_IPHONE_C2.sh

# Start server only
./START_IPHONE_C2.sh --server-only

# Start agent only
./START_IPHONE_C2.sh --agent-only

# Stop all processes
./stop_all.sh
```

### Interactive Interface
```bash
# Launch interactive mode
python3 control_iphone.py --mode interactive

# Available commands:
controller> server          # Start C2 server
controller> connect <IP>    # Connect to agent
controller> list           # List agents
controller> session <ID>   # Start agent session
controller> monitor        # Monitor agents
controller> export <ID> <file>  # Export data
controller> exit           # Exit interface
```

## 🔌 Agent Management

### Connection Commands
```bash
# Connect to agent
controller> connect 192.168.1.100 4444

# List all agents
controller> list

# Start session with agent
controller> session agent_12345678

# Monitor all agents
controller> monitor
```

### Agent Session Commands
```bash
agent_123> help           # Show help
agent_123> info           # System information
agent_123> exec <cmd>     # Execute command
agent_123> ls [path]      # List files
agent_123> screenshot     # Take screenshot
agent_123> camera         # Capture camera
agent_123> exit           # Exit session
```

## 💻 Remote Commands

### System Information
```bash
# Basic info
agent_123> info

# Detailed system info
agent_123> exec "uname -a"
agent_123> exec "df -h"
agent_123> exec "free -m"
agent_123> exec "ps aux"
```

### Command Execution
```bash
# Single command
agent_123> exec "ls -la"

# With parameters
agent_123> exec "curl -I https://google.com"

# Background process
agent_123> exec "nohup python3 script.py &"

# Pipeline commands
agent_123> exec "ps aux | grep python"
```

### Process Control
```bash
# List processes
agent_123> exec "ps aux"

# Kill process
agent_123> exec "kill -9 1234"

# Start service
agent_123> exec "systemctl start nginx"

# Check status
agent_123> exec "systemctl status nginx"
```

## 📁 File Operations

### Navigation and Listing
```bash
# Current directory
agent_123> ls

# Specific directory
agent_123> ls /var/log

# Detailed listing
agent_123> exec "ls -la /home"

# Find files
agent_123> exec "find / -name '*.log' 2>/dev/null"
```

### File Management
```bash
# Copy files
agent_123> exec "cp source.txt dest.txt"

# Move files
agent_123> exec "mv old.txt new.txt"

# Remove files
agent_123> exec "rm -rf /tmp/junk"

# Create directory
agent_123> exec "mkdir -p /tmp/newdir"

# Change permissions
agent_123> exec "chmod 755 script.sh"
```

### File Content
```bash
# View file
agent_123> exec "cat /var/log/syslog"

# Search in file
agent_123> exec "grep 'error' app.log"

# Edit file
agent_123> exec "nano config.txt"

# Compress files
agent_123> exec "tar -czf backup.tar.gz data/"
```

## 🔍 Monitoring Commands

### System Monitoring
```bash
# Resource usage
agent_123> exec "top -b -n 1"
agent_123> exec "htop -n 1"

# Disk usage
agent_123> exec "df -h"

# Memory usage
agent_123> exec "free -h"

# Load average
agent_123> exec "cat /proc/loadavg"
```

### Network Monitoring
```bash
# Connections
agent_123> exec "netstat -tuln"
agent_123> exec "ss -tuln"

# Network stats
agent_123> exec "cat /proc/net/dev"

# Test connectivity
agent_123> exec "ping -c 4 google.com"
```

### Log Monitoring
```bash
# Follow logs
agent_123> exec "tail -f /var/log/syslog"

# Recent logs
agent_123> exec "tail -100 /var/log/app.log"

# Search logs
agent_123> exec "grep 'ERROR' /var/log/app.log"

# System logs
agent_123> exec "journalctl -n 50"
```

## 🛡️ Security Commands

### Authentication
```python
# Check authentication status
controller.check_auth_status()

# Generate new token
controller.generate_token(user_id)

# Revoke token
controller.revoke_token(token_id)
```

### SSL/TLS Operations
```bash
# Check certificate
openssl s_client -connect server:8080

# Verify certificate
openssl x509 -in server.crt -text -noout

# Generate new cert
openssl req -new -x509 -key server.key -out server.crt -days 365
```

### Access Control
```bash
# Check allowed IPs
agent_123> exec "cat /etc/hosts.allow"

# Firewall status
sudo ufw status

# Block IP
sudo ufw deny from 192.168.1.100
```

## 🔧 Configuration

### Server Configuration
```json
{
    "host": "0.0.0.0",
    "port": 8080,
    "ssl_enabled": true,
    "cert_file": "server.crt",
    "key_file": "server.key",
    "max_connections": 100,
    "timeout": 300
}
```

### Agent Configuration
```json
{
    "server_host": "localhost",
    "server_port": 8080,
    "heartbeat_interval": 60,
    "reconnect_interval": 30,
    "debug": false
}
```

### Environment Variables
```bash
export IPHONE_CONTROL_HOME="/opt/iphone_control"
export IPHONE_CONTROL_SERVER_PORT="8080"
export IPHONE_CONTROL_SSL_CERT="/path/to/cert"
export IPHONE_CONTROL_SSL_KEY="/path/to/key"
```

## 🐛 Troubleshooting

### Common Issues
```bash
# Check service status
systemctl status iphone-c2-server
systemctl status iphone-agent

# Check logs
tail -f logs/server.log
tail -f logs/agent.log

# Check network
netstat -ln | grep :8080
telnet localhost 8080

# Check SSL
openssl s_client -connect localhost:8080
```

### Debug Mode
```bash
# Enable debug
export IPHONE_CONTROL_DEBUG=true

# Verbose output
python3 -v c2_server.py

# Python debugger
python3 -m pdb control_iphone.py
```

### Recovery Commands
```bash
# Restart services
sudo systemctl restart iphone-c2-server
sudo systemctl restart iphone-agent

# Clear logs
> logs/server.log
> logs/agent.log

# Reset configuration
cp config/server_config.json.backup config/server_config.json
```

## 📊 Performance Commands

### Performance Monitoring
```bash
# CPU usage
agent_123> exec "cat /proc/stat"
agent_123> exec "mpstat 1 5"

# Memory usage
agent_123> exec "cat /proc/meminfo"
agent_123> exec "vmstat 1 5"

# Disk I/O
agent_123> exec "iostat 1 5"

# Network I/O
agent_123> exec "sar -n DEV 1 5"
```

### Optimization Commands
```bash
# Clear cache
agent_123> exec "sync && echo 3 > /proc/sys/vm/drop_caches"

# Check disk space
agent_123> exec "du -sh /tmp/*"

# Clean temp files
agent_123> exec "find /tmp -type f -mtime +7 -delete"

# Check open files
agent_123> exec "lsof | wc -l"
```

## 🔄 Batch Operations

### Python API Examples
```python
# Batch command execution
controller = iPhoneController()
agents = ["agent_1", "agent_2", "agent_3"]
results = controller.batch_command_execution(agents, "system_info")

# File operations
controller.upload_file("agent_1", "local.txt", "/tmp/remote.txt")
controller.download_file("agent_1", "/tmp/data.log", "local_data.log")

# Monitoring
for agent in controller.list_agents():
    info = controller.get_agent_system_info(agent.agent_id)
    print(f"{agent.agent_id}: {info}")
```

### Script Examples
```bash
#!/bin/bash
# Monitor all agents
python3 -c "
from control_iphone import iPhoneController
controller = iPhoneController()
for agent in controller.list_connected_agents():
    print(f'Agent: {agent.agent_id}, Status: {agent.status}')
"
```

## 📝 Quick Scripts

### Health Check Script
```bash
#!/bin/bash
echo "=== iPhone Control Framework Health Check ==="

# Check services
echo "Services:"
systemctl is-active iphone-c2-server && echo "✓ C2 Server" || echo "✗ C2 Server"
systemctl is-active iphone-agent && echo "✓ iPhone Agent" || echo "✗ iPhone Agent"

# Check ports
echo "Ports:"
netstat -ln | grep :8080 && echo "✓ Port 8080" || echo "✗ Port 8080"
netstat -ln | grep :4444 && echo "✓ Port 4444" || echo "✗ Port 4444"

# Check SSL
echo "SSL:"
test -f server.crt && echo "✓ Certificate exists" || echo "✗ Certificate missing"
test -f server.key && echo "✓ Private key exists" || echo "✗ Private key missing"
```

### Backup Script
```bash
#!/bin/bash
BACKUP_DIR="/opt/backups/iphone_control"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup configs
tar -czf $BACKUP_DIR/config_$DATE.tar.gz config/

# Backup data
tar -czf $BACKUP_DIR/data_$DATE.tar.gz data/

echo "Backup completed: $BACKUP_DIR"
```

### Cleanup Script
```bash
#!/bin/bash
echo "Cleaning up iPhone Control Framework..."

# Clean old logs
find logs/ -name "*.log" -mtime +30 -delete

# Clean temp files
find /tmp -name "iphone_*" -mtime +1 -delete

# Clean old backups
find /opt/backups/iphone_control -name "*.tar.gz" -mtime +30 -delete

echo "Cleanup completed."
```

## 🔑 Keyboard Shortcuts

### Interactive Mode
```
Ctrl+C    - Exit current operation
Ctrl+D    - Exit interface
Tab       - Auto-complete (if available)
↑/↓       - Command history
```

### Common Shortcuts
```bash
# Quick status check
python3 control_iphone.py --mode client --host localhost --port 8080

# Quick agent test
python3 -c "from iphone_remote_access import iPhoneRemoteAccess; print(iPhoneRemoteAccess('localhost', 4444).connect())"

# Quick log view
tail -f logs/server.log &
tail -f logs/agent.log &
```

## 📞 Emergency Commands

### System Recovery
```bash
# Emergency stop
pkill -f c2_server.py
pkill -f iphone_agent.py

# Emergency restart
./START_IPHONE_C2.sh --force

# Emergency reset
rm -f pids/*.pid
./START_IPHONE_C2.sh
```

### Security Emergency
```bash
# Block all connections
sudo ufw deny 8080
sudo ufw deny 4444

# Kill all agent connections
pkill -f iphone_agent

# Reset authentication
rm -f config/auth_tokens.json
```

---

## 📚 Additional Resources

- **Full Documentation**: `README_IPHONE_CONTROL.md`
- **Deployment Guide**: `iphone_deployment_guide.md`
- **Usage Guide**: `IPHONE_USAGE_GUIDE.md`
- **Configuration Files**: `config/`
- **Log Files**: `logs/`
- **Scripts**: `scripts/`

**Note**: This is a placeholder framework for demonstration purposes. Always ensure proper authorization and legal compliance when using such tools.
