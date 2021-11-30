import pyads

AMSNETID = "10.123.67.6.1.1"

plc = pyads.Connection(AMSNETID, pyads.PORT_TC3PLC1)
plc.open()
print(f"Connected?: {plc.is_open}") #debugging statement, optional
print(f"Local Address? : {plc.get_local_address()}") #debugging statement, optional

plc.write_by_name("MAIN.sWord", 'yeyeyeyyeye')
print(plc.read_by_name("Main.sWord"))

plc.close()
