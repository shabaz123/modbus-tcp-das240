DAS240-BAT and DAS220-BAT Modbus TCP Library for Python

Usage:

    inport time
    import das240 as das

    ipaddr="192.168.1.100"
    channel=1
    filename="mylogfile.log"

    print("Logging for 60 seconds")
    for t in range (0, 60):
      das.log(ipaddr, channel, filename)
      time.sleep(1)
    print("Done!")


