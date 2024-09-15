import os
import random
import time
from threading import Lock
from cryptofuzz import Convertor
from cryptofuzz.assest import MAX_PRIVATE_KEY
from colorthon import Colors

# Initialize Convertor
co = Convertor()

# COLORS CODE --------------------
RED = Colors.RED
GREEN = Colors.GREEN
YELLOW = Colors.YELLOW
CYAN = Colors.CYAN
WHITE = Colors.WHITE
RESET = Colors.RESET
# COLORS CODE -------------------

def getClear():
    """Clear the terminal screen."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def KeyGen(size):
    """Generate a random private key of specified size."""
    k = "".join(random.choice('0122333444455555666666777777788888888999999999abcdef') for _ in range(size))
    if int(k, 16) < MAX_PRIVATE_KEY:
        return k
    else:
        return KeyGen(size)

def Hex_To_Addr(hexed, compress):
    """Convert hexadecimal string to address."""
    return co.hex_to_addr(hexed, compress)

def Rich_Loader(FileName):
    """Load target addresses from a file."""
    with open(FileName, 'r') as file:
        return set(line.strip() for line in file)

def getHeader(richFile, loads, found):
    """Display the header information."""
    getClear()
    output = f"""
{RED}➜{RESET} {WHITE}BTC {RESET}{CYAN}Private Key Brute Force {RESET} v1 {GREEN}BETA{RESET}
{RED}➜{RESET} {WHITE}AUTHOR {RESET}{CYAN}:{RESET}-{GREEN}Hantu{RESET}
{RED}▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬{RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Address File     :{RESET}{CYAN} {richFile}                {RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Method           :{RESET}{CYAN} Random.                   {RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Address Type     :{RESET}{CYAN} Compressed / Uncompressed.{RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Max HEX Length  :{RESET}{CYAN} {MAX_PRIVATE_KEY}         {RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Result Checked   :{RESET}{CYAN} {loads}                   {RESET}
{RED}[{RESET}{WHITE}►{RESET}{RED}]{RESET}{GREEN} Matched Address  :{RESET}{CYAN} {found}                   {RESET}
"""
    print(output)

def MainCheck():
    """Main function to perform the brute-force search."""
    global z, wf
    target_file = 'btc.txt'
    Targets = Rich_Loader(target_file)
    z = 0
    wf = 0
    lg = 0
    getHeader(richFile=target_file, loads=lg, found=wf)
    
    while True:
        z += 1
        privatekey = KeyGen(64)
        CompressAddr = Hex_To_Addr(privatekey, True)
        UncompressAddr = Hex_To_Addr(privatekey, False)
        lct = time.localtime()
        
        # Check if the address is in the targets
        if str(CompressAddr) in Targets:
            wf += 1
            with open('Found.txt', 'a') as file:
                file.write(f"Compressed Address: {CompressAddr}\n"
                           f"Private Key: {privatekey}\n"
                           f"DEC: {int(privatekey, 16)}\n"
                           f"{'-' * 66}\n")
        elif str(UncompressAddr) in Targets:
            wf += 1
            with open('Found.txt', 'a') as file:
                file.write(f"Uncompressed Address: {UncompressAddr}\n"
                           f"Private Key: {privatekey}\n"
                           f"DEC: {int(privatekey, 16)}\n"
                           f"{'-' * 66}\n")
        elif int(z % 100000) == 0:
            lg += 100000
            getHeader(richFile=target_file, loads=lg, found=wf)
            print(f"Generated: {lg} (SHA-256 - HEX) ...")
        else:
            tm = time.strftime("%Y-%m-%d %H:%M:%S", lct)
            print(f"[{tm}][Total: {z} Check: {z * 2}] #Found: {wf} ", end="\r")
        
        # Optional: Add sleep to reduce CPU usage
        time.sleep(0.01)  # Adjust the sleep time as needed

if __name__ == '__main__':
    MainCheck()  # Start the main function directly

