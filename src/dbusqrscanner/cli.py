"""Console script for dbusqrdecoder."""
import argparse
from .dbusqrscanner import QRService

def main():
    parser = argparse.ArgumentParser(prog="dbusqrscanner", description="A package made for scanning qr codes")

    parser.add_argument("--show-messages", action="store_true", dest="sm", help="Shows print messages")

    args = parser.parse_args()

    scan = QRService(msgs=args.sm)
    scan.run()
