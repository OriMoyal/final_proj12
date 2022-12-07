import os
import psutil
import platform, help
from datetime import datetime

def create_file():
    # Boot Time
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    with open('ComputerInfo.txt', 'w') as f:
        f.write("======================================== Boot Time ========================================\n")
        f.write(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n")
        f.write("\n")
        f.write("======================================== System Information ========================================\n")
        uname = platform.uname()
        f.write(f"System: {uname.system}\n")
        f.write(f"Node Name: {uname.node}\n")
        f.write(f"Release: {uname.release}\n")
        f.write(f"Version: {uname.version}\n")
        f.write(f"Machine: {uname.machine}\n")
        f.write(f"Processor: {uname.processor}\n")

        f.write("\n")
        # let's print CPU information
        f.write("======================================== CPU Info ========================================\n")
        # number of cores
        f.write("Physical cores:", )
        f.write(str(psutil.cpu_count(logical=False)))
        f.write("\n")
        f.write("Total cores:")
        f.write(str(psutil.cpu_count(logical=True)))
        f.write("\n")
        f.write("======================================== Disk Information ========================================\n")
        # CPU frequencies
        cpufreq = psutil.cpu_freq()
        f.write(f"Max Frequency: {cpufreq.max:.2f}Mhz\n")
        f.write(f"Min Frequency: {cpufreq.min:.2f}Mhz\n")
        f.write(f"Current Frequency: {cpufreq.current:.2f}Mhz\n")
        # CPU usage
        f.write("\n")
        f.write("CPU Usage Per Core:\n")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            f.write(f"Core {i}: {percentage}%\n")
        f.write(f"Total CPU Usage: {psutil.cpu_percent()}%\n")

        f.write("\n")

        # Disk Information
        f.write("======================================== Disk Information ========================================\n")
        f.write("Partitions and Usage:\n")
        # get all disk partitions
        partitions = psutil.disk_partitions()
        for partition in partitions:
            f.write(f"=== Device: {partition.device} ===\n")
            f.write(f"  Mountpoint: {partition.mountpoint}\n")
            f.write(f"  File system type: {partition.fstype}\n")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                continue
            f.write(f"  Total Size: {help.get_size(partition_usage.total)}\n")
            f.write(f"  Used: {help.get_size(partition_usage.used)}\n")
            f.write(f"  Free: {help.get_size(partition_usage.free)}\n")
            f.write(f"  Percentage: {partition_usage.percent}%\n")
        # get IO statistics since boot
        disk_io = psutil.disk_io_counters()
        f.write(f"Total read: {help.get_size(disk_io.read_bytes)}\n")
        f.write(f"Total write: {help.get_size(disk_io.write_bytes)}\n")

        f.write("\n")

        # Memory Information
        f.write("======================================== Memory Information ========================================\n")
        # get the memory details
        svmem = psutil.virtual_memory()
        f.write(f"Total: {help.get_size(svmem.total)}\n")
        f.write(f"Available: {help.get_size(svmem.available)}\n")
        f.write(f"Used: {help.get_size(svmem.used)}\n")
        f.write(f"Percentage: {svmem.percent}%\n")
        f.write("==================== SWAP ====================\n")
        # get the swap memory details (if exists)
        swap = psutil.swap_memory()
        f.write(f"Total: {help.get_size(swap.total)}\n")
        f.write(f"Free: {help.get_size(swap.free)}\n")
        f.write(f"Used: {help.get_size(swap.used)}\n")
        f.write(f"Percentage: {swap.percent}%\n")

        f.write("\n")

        # Network information
        f.write("======================================== Network Information ========================================\n")
        # get all network interfaces (virtual and physical)
        if_addrs = psutil.net_if_addrs()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                f.write(f"=== Interface: {interface_name} ===\n")
                if str(address.family) == 'AddressFamily.AF_INET':
                    f.write(f"  IP Address: {address.address}\n")
                    f.write(f"  Netmask: {address.netmask}\n")
                    f.write(f"  Broadcast IP: {address.broadcast}\n")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    f.write(f"  MAC Address: {address.address}\n")
                    f.write(f"  Netmask: {address.netmask}\n")
                    f.write(f"  Broadcast MAC: {address.broadcast}\n")
        # get IO statistics since boot
        net_io = psutil.net_io_counters()
        f.write(f"Total Bytes Sent: {help.get_size(net_io.bytes_sent)}\n")
        f.write(f"Total Bytes Received: {help.get_size(net_io.bytes_recv)}\n")


create_file()