# 通用 Linux 知识

> 通用 Linux 系统约束、API速查、编译参数

---

## 系统约束

### 文件系统
- **推荐**: ext4, xfs
- **权限**: 遵循 LSB 标准
- **路径**: 最大 4096 字符

### 进程管理
- **最大进程数**: `/proc/sys/kernel/pid_max`
- **最大文件描述符**: `/proc/sys/fs/file-max`
- **线程栈大小**: 默认 8MB

---

## API 速查

### 文件操作
```bash
# 文件权限
chmod 755 file.sh
chown user:group file.txt

# 文件查找
find /path -name "*.py"
locate filename

# 文件内容搜索
grep "pattern" file.txt
grep -r "pattern" /path/
```

### 进程管理
```bash
# 进程查看
ps aux
top
htop

# 进程控制
kill -9 PID
pkill process_name
```

### 网络操作
```bash
# 网络状态
ip addr show
netstat -tuln
ss -tuln

# 端口监听
nc -l 8080
```

### 系统信息
```bash
# 系统信息
uname -a
cat /etc/os-release

# 硬件信息
lscpu
lsblk
free -h
```

---

## 编译参数

### 通用编译选项
```bash
# 基础选项
CFLAGS="-Wall -Wextra -std=c11"

# 优化选项
CFLAGS+=" -O2 -pipe"

# 调试选项
CFLAGS+=" -g -DDEBUG"

# 位置无关代码
CFLAGS+=" -fPIC"
```

### 链接选项
```bash
# 基础选项
LDFLAGS="-Wl,-rpath,/usr/local/lib"

# 静态链接
LDFLAGS+=" -static"

# 动态链接
LDFLAGS+=" -shared"
```

---

## 包管理

### apt (Debian/Ubuntu)
```bash
# 更新包列表
apt update

# 安装包
apt install package_name

# 搜索包
apt search keyword

# 删除包
apt remove package_name
```

### yum (CentOS/RHEL)
```bash
# 更新包列表
yum update

# 安装包
yum install package_name

# 搜索包
yum search keyword

# 删除包
yum remove package_name
```

---

## 服务管理

### systemd
```bash
# 启动服务
systemctl start service_name

# 停止服务
systemctl stop service_name

# 重启服务
systemctl restart service_name

# 查看状态
systemctl status service_name

# 开机自启
systemctl enable service_name
```

---

## 日志管理

### 系统日志
```bash
# 查看系统日志
journalctl -f

# 查看特定服务日志
journalctl -u service_name

# 查看内核日志
dmesg | tail
```

### 应用日志
```bash
# 查看日志文件
tail -f /var/log/app.log

# 搜索日志
grep "ERROR" /var/log/app.log
```

---

## 常见问题

### 权限问题
```bash
# 错误: Permission denied
# 解决: 使用 sudo 或修改权限
sudo command
chmod +x script.sh
```

### 依赖问题
```bash
# 错误: library not found
# 解决: 安装依赖或设置库路径
sudo apt install libxxx-dev
export LD_LIBRARY_PATH=/path/to/library:$LD_LIBRARY_PATH
```

### 端口占用
```bash
# 错误: Address already in use
# 解决: 查找并停止占用端口的进程
lsof -i :8080
kill -9 PID
```

---

## 参考资料
- [Linux 手册页](https://man7.org/linux/man-pages/)
- [Linux 内核文档](https://www.kernel.org/doc/)
- [systemd 文档](https://www.freedesktop.org/software/systemd/man/)