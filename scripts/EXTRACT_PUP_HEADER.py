import struct
import sys

def parse_pup(pup_path):
    print(f"Analyzing PS5 PUP: {pup_path}")
    
    with open(pup_path, "rb") as f:
        # Read potential BLS header (first 0x400 bytes)
        data = f.read(0x400)
        
        # BLS Header Magic: "BLS2" (0x32424C53)
        magic = struct.unpack("<I", data[0:4])[0]
        if magic == 0x32424C53:
            print("✅ Detected BLS2 Header")
            # Parse BLS Entry List
            entry_count = struct.unpack("<I", data[0xC:0x10])[0]
            print(f"  Entries: {entry_count}")
            
            # Entry list start: 0x20 for 12.70+, 0x40 for legacy?
            # Let's detect based on name position
            if data[0x30:0x33] == b"PS5":
                list_start = 0x20
                entry_size_bytes = 0x30
            else:
                list_start = 0x40
                entry_size_bytes = 0x30
                
            for i in range(entry_count):
                offset = list_start + (i * entry_size_bytes)
                # For 12.70, metadata is BEFORE name
                if list_start == 0x20:
                    entry_offset_sectors = struct.unpack("<I", data[offset:offset+4])[0]
                    entry_size_bytes_total = struct.unpack("<I", data[offset+4:offset+8])[0]
                    entry_name = data[offset+16:offset+48].split(b'\x00')[0].decode('utf-8', errors='ignore')
                else:
                    # Legacy: Name then metadata
                    entry_name = data[offset:offset+32].split(b'\x00')[0].decode('utf-8', errors='ignore')
                    entry_offset_sectors = struct.unpack("<I", data[offset+32:offset+36])[0]
                    entry_size_bytes_total = struct.unpack("<I", data[offset+36:offset+40])[0]

                entry_offset = entry_offset_sectors * 512
                print(f"  - Entry {i}: {entry_name} (Offset: 0x{entry_offset:X}, Size: {entry_size_bytes_total} bytes)")
                
                # Peek into the PUP header
                f.seek(entry_offset)
                pup_header_data = f.read(0x20)
                pup_magic = struct.unpack("<I", pup_header_data[0:4])[0]
                if pup_magic == 0xEEF51454:
                    print(f"    ✅ Valid PUP Magic for {entry_name}")
                    if i == 0: # PS5UPDATE1.PUP usually has count at 0xE
                        segment_count = struct.unpack("<H", pup_header_data[0xE:0x10])[0]
                    else:
                        segment_count = struct.unpack("<H", pup_header_data[0x18:0x1A])[0]
                    print(f"    Segments: {segment_count}")
                    
                    # Read segments
                    f.seek(entry_offset + 0x20)
                    for j in range(segment_count):
                        seg_data = f.read(32)
                        flags = struct.unpack("<I", seg_data[0:4])[0]
                        flags2 = struct.unpack("<I", seg_data[4:8])[0]
                        offset = struct.unpack("<Q", seg_data[8:16])[0]
                        c_size = struct.unpack("<Q", seg_data[16:24])[0]
                        u_size = struct.unpack("<Q", seg_data[24:32])[0]
                        
                        # Identify segment type based on flags
                        seg_type = "DATA"
                        if (flags & 0xF0000000) == 0xE0000000: seg_type = "SIG"
                        elif (flags & 0xF0000000) == 0xF0000000: seg_type = "WM"
                        
                        print(f"      - Seg {j:2d}: [{seg_type}] Flags: 0x{flags:08X}, Offset: 0x{offset:X}, Size: {c_size}")
                else:
                    print(f"    ❌ Invalid PUP Magic for {entry_name}: 0x{pup_magic:X}")
        else:
            print(f"❌ Not a standard BLS2 file (Magic: 0x{magic:X})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python EXTRACT_PUP_HEADER.py <pup_path>")
    else:
        parse_pup(sys.argv[1])
