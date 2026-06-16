# i.MX6ULL 平台知识

> NXP i.MX6ULL 芯片专属约束、API速查、编译参数

---

## 专属约束

### 编译器要求
- **必须使用**: `arm-linux-gnueabihf-gcc`
- **最低版本**: gcc 8.0+
- **架构**: ARM Cortex-A7

### 内核版本
- **推荐版本**: 5.4
- **设备树路径**: `/boot/dtb/imx6ull-*.dtb`

### 内存布局
- **DDR**: 256MB/512MB
- **起始地址**: `0x80000000`
- **内核地址**: `0x80800000`

---

## API 速查

### GPIO 操作
```bash
# 导出 GPIO
echo 50 > /sys/class/gpio/export

# 设置方向
echo out > /sys/class/gpio/gpio50/direction

# 设置值
echo 1 > /sys/class/gpio/gpio50/value
```

### 串口设备
```bash
# 串口列表
ls /dev/tty*

# 串口配置
stty -F /dev/ttymxc0 115200 cs8 -cstopb -parity
```

### I2C 设备
```bash
# I2C 总线扫描
i2cdetect -y 0

# I2C 读写
i2cget -y 0 0x50 0x00
i2cset -y 0 0x50 0x00 0xff
```

### SPI 设备
```bash
# SPI 设备列表
ls /dev/spidev*

# SPI 测试
spidev_test -D /dev/spidev0.0
```

---

## 编译参数

### 交叉编译工具链
```bash
export CROSS_COMPILE=arm-linux-gnueabihf-
export CC=${CROSS_COMPILE}gcc
export CXX=${CROSS_COMPILE}g++
export LD=${CROSS_COMPILE}ld
export AR=${CROSS_COMPILE}ar
export STRIP=${CROSS_COMPILE}strip
```

### 编译选项
```bash
# 基础选项
CFLAGS="-march=armv7-a -mtune=cortex-a7 -mfpu=neon"

# 优化选项
CFLAGS+=" -O2 -pipe"

# 调试选项
CFLAGS+=" -g"
```

### 链接选项
```bash
LDFLAGS="-march=armv7-a"
LDFLAGS+=" --sysroot=/path/to/sysroot"
```

---

## 设备树配置

### 常用节点
```dts
// GPIO 节点
&gpio1 {
    gpio50: gpio50 {
        gpio-hog;
        gpios = <&gpio1 18 GPIO_ACTIVE_HIGH>;
        output-high;
        line-name = "gpio50";
    };
};

// 串口节点
&uart1 {
    pinctrl-names = "default";
    pinctrl-0 = <&pinctrl_uart1>;
    status = "okay";
};

// I2C 节点
&i2c1 {
    clock-frequency = <100000>;
    pinctrl-names = "default";
    pinctrl-0 = <&pinctrl_i2c1>;
    status = "okay";
};
```

---

## 启动流程

### 启动顺序
1. **BootROM**: 芯片内部固件
2. **SPL (Secondary Program Loader)**: 初始化 DDR
3. **U-Boot**: 加载内核和设备树
4. **Kernel**: 启动 Linux 内核

### 启动参数
```bash
setenv bootargs 'console=ttymxc0,115200 root=/dev/mmcblk0p2 rootfstype=ext4 rw rootwait'
setenv bootcmd 'mmc read 0x80800000 0x4000 0x8000; bootm 0x80800000'
saveenv
```

---

## 常见问题

### 编译错误
```bash
# 错误: cannot find -lxxx
# 解决: 添加库路径
LDFLAGS+=" -L/path/to/library"

# 错误: undefined reference to xxx
# 解决: 添加库
LDFLAGS+=" -lxxx"
```

### 运行时错误
```bash
# 错误: error while loading shared libraries
# 解决: 设置库路径
export LD_LIBRARY_PATH=/path/to/library:$LD_LIBRARY_PATH

# 错误: No such file or directory
# 解决: 检查文件系统挂载
mount /dev/mmcblk0p2 /mnt
```

---

## 参考资料
- [i.MX6ULL 数据手册](https://www.nxp.com/)
- [U-Boot 文档](https://www.denx.de/wiki/U-Boot)
- [Linux 内核文档](https://www.kernel.org/doc/)