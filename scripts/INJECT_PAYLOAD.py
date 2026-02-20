import os

# Sovereign Universal Bridge Offsets
OFFSETS = {
    "1.02_8.00": 0x3C68,  # Baseline
    "12.70": 0x27C68     # Sigma = 0x24000
}

def send_payload(ps5_ip, port, file_path):
    print(f"🚀 Sending Payload to PS5: {ps5_ip}:{port}")
    print(f"   Payload: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return

    try:
        # Create a socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10) # 10s timeout
            print(f"   Connecting...", end="", flush=True)
            s.connect((ps5_ip, port))
            print(" Connected! ✅")
            
            with open(file_path, "rb") as f:
                data = f.read()
                print(f"   Sending {len(data)} bytes...", end="", flush=True)
                s.sendall(data)
                print(" Sent! 📤")
                
        print("✅ Injection Complete.")
        
    except ConnectionRefusedError:
        print("\n❌ Connection Refused. Is the ELF Loader running on the PS5?")
    except socket.timeout:
        print("\n❌ Connection Timed Out. Check IP/Port and Firewall.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SpookyOS Payload Injector")
    parser.add_argument("ip", help="PS5 IP Address")
    parser.add_argument("--port", type=int, default=9020, help="ELF Loader Port (Default: 9020)")
    parser.add_argument("--file", help="Payload File Path")
    parser.add_argument("--fw", choices=["1.02", "8.00", "12.70"], default="12.70", help="Firmware version for offset calculation")
    
    args = parser.parse_args()
    
    if args.file:
        send_payload(args.ip, args.port, args.file)
    else:
        # Implicit Stage 0 Mutation (Concept)
        target_offset = OFFSETS.get(args.fw) if args.fw != "8.00" else OFFSETS["1.02_8.00"]
        print(f"💎 Target Offset for {args.fw}: 0x{target_offset:X}")
        # Logic for BNE -> NOP mutation would go here
