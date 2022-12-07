import os

os.system('cmd /c "arp -a> IP(LanNetwork).txt"')

# writing to file
file1 = open('IP(LanNetwork).txt', 'r')

Lines = file1.readlines()
file1.close()

# # Strips the newline character
for line in Lines[3:]:
    print(line.split()[0])

file2 = open('ComputerIP.txt', 'w')
for line in Lines[3:]:
    file2.write(line.split()[0] + "\n")
