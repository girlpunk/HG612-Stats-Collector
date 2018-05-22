import requests
import sys

import re

device_host = "http://192.168.42.253"

paths = {
    "deviceInfo": {
        "path": "/html/status/deviceinfo.asp",
        "regex": r"(?:stDeviceInfo\(\".*)(?:\",\")(?P<ProductType>.*)(?:\",\")(?P<DeviceID1>.*)(?:\",\")(?P<HardwareVersion>.*)(?:\",\")(?P<SoftwareVersion>.*)(?:\",\")(?P<DeviceID2>.*)(?:\",\")(?P<FirmwareVersion>.*)(?:\",\".*\"\).*\")(?P<BatchNumber>.*)\""
    },
    "ATM": {
        "path": "/html/status/atmStatus.asp",
        "regex": r"(?:XtmConstruction\(\".*\",\")(?P<TXByteCount>.*)(?:\",\")(?P<RXByteCount>.*)(?:\",\")(?P<TXPacketCount>.*)(?:\",\")(?P<RXPacketCount>.*)(?:\",\")(?P<CellErrors>.*)(?:\"\).*)"
    },
    "WAN": {
        "path": "/html/status/internetstatus.asp",
        "regex": r"(?:stStats\(\".*\",\")(?P<TXByteCount>.*)(?:\",\")(?P<RXByteCount>.*)(?:\",\")(?P<TXPacketCount>.*)(?:\",\")(?P<RXPacketCount>.*)(?:\",\")(?P<TXError>.*)(?:\",\")(?P<RXError>.*)(?:\",\")(?P<TXDiscard>.*)(?:\",\")(?P<RXDiscard>.*)(?:\"\).*)"
    },
    "VDSL": {
        "path": "/html/status/xdslStatus.asp",
        "regex": r"(?:stDsl\(\"[\w\.]*\",\")(?P<status>\w*)(?:\",\")(?P<modulation>\w*)(?:\",\")(?P<dataPath>\w*)(?:\",\")(?P<upCurrRate>\d*)(?:\",\")(?P<downCurrRate>\d*)(?:\",\".*?\",\".*?\",\")(?P<upMaxRate>\d*)(?:\",\")(?P<downMaxRate>\d*)(?:\",\")(?P<upSNR>\d*)(?:\",\")(?P<downSNR>\d*)(?:\",\")(?P<upAttenuation>\d*)(?:\",\")(?P<downAttenuation>\d*)(?:\",\")(?P<upPower>\d*)(?:\",\")(?P<downPower>\d*)(?:\",\")(?P<traffType>.*?)(?:\".*stStats\(\"[\w\.]*?\",\")(?P<downHEC>\d*)(?:\",\")(?P<upHEC>\d*)(?:\",\")(?P<downCRC>\d*)(?:\",\")(?P<upCRC>\d*)(?:\",\")(?P<downFEC>\d*)(?:\",\")(?P<upFEC>\d*)(?:\",\")"
    },
    "LAN": {
        "path": "/html/status/ethenet.asp",
        "regex": r"(?:\[\[\"[\w\.]*?\",\")(?P<LAN1State>\w*)(?:\",\")(?P<LAN1Speed>\d*)(?:\",\")(?P<LAN1Duplex>\w*)(?:\",\")(?P<LAN1RXBytes>\d*)(?:\",\")(?P<LAN1RXPackets>\d*)(?:\",\")(?P<LAN1RXError>\d*)(?:\",\")(?P<LAN1RXDiscard>\d*)(?:\",\")(?P<LAN1TXBytes>\d*)(?:\",\")(?P<LAN1TXPackets>\d*)(?:\",\")(?P<LAN1TXError>\d*)(?:\",\")(?P<LAN1TXDiscard>\d*)(?:\"\],[\"[\w\.]*?\",\")(?P<LAN2State>\w*)(?:\",\")(?P<LAN2Speed>\d*)(?:\",\")(?P<LAN2Duplex>\w*)(?:\",\")(?P<LAN2RXBytes>\d*)(?:\",\")(?P<LAN2RXPackets>\d*)(?:\",\")(?P<LAN2RXError>\d*)(?:\",\")(?P<LAN2RXDiscard>\d*)(?:\",\")(?P<LAN2TXBytes>\d*)(?:\",\")(?P<LAN2TXPackets>\d*)(?:\",\")(?P<LAN2TXError>\d*)(?:\",\")(?P<LAN2TXDiscard>\d*)"
    }
}


def do_login():
    session = requests.session()

    session.get(device_host + "/login.cgi", params={
        "Username": "admin",
        "Password": "YWRtaW4",  # admin
        "Language": 0,
        "RequestFile": "html/content.asp"
    }).raise_for_status()

    return session


def __main__():
    session = do_login()
    request = session.get(device_host + paths[sys.argv[1]]["path"])
    request.raise_for_status()

    x = re.search(paths[sys.argv[1]]["regex"], request.text, re.S)

    print(x.group(sys.argv[2]))


if __name__ == "__main__":
    __main__()
