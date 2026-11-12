"""Read-only check of the 405 TS washer, using PyLabRobot pull request #1266's driver.

Opens the port, pings, and reads firmware, fitted options, serial number and run status, then
closes. Sends only GET queries and a ping: nothing moves and no fluid is pumped.

Usage, from the repo root, with the washer's COM port:
  .venv\\Scripts\\python lab\\405ts\\readonly_405ts.py COM6
"""

import asyncio
import sys

from pylabrobot.agilent.biotek.lhc.devices.washer_405ts import Washer405TS


async def main(port: str) -> None:
  device = Washer405TS(port=port)
  try:
    await device.setup()
    print("\n=== fitted options ===")
    print(device.settings)
    print("\n=== serial number ===")
    print(await device.get_serial_number())
    print("\n=== firmware ===")
    print(await device.get_firmware_version())
    print("\n=== status ===")
    print(await device.get_status())
    print("\n=== steps this unit can run ===")
    print([s.name for s in device.get_available_steps()])
  finally:
    await device.stop()


if __name__ == "__main__":
  asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "COM6"))
