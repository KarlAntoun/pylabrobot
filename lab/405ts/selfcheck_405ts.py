"""Self-check of the 405 TS washer, using PyLabRobot pull request #1266's driver.

Runs setup() (read-only), then the washer's own self-check, then reads the status.
The self-check MOVES THE MOTORS: it homes them, empties the priming trough and tests the vacuum.
It pumps no buffer. Needs the waste bottles and pump connected, pump switched on.

Usage, from the repo root, with the washer's COM port:
  .venv\\Scripts\\python lab\\405ts\\selfcheck_405ts.py COM6
"""

import asyncio
import sys
import time

from pylabrobot.agilent.biotek.lhc.devices.washer_405ts import Washer405TS


async def main(port: str) -> None:
  device = Washer405TS(port=port)
  try:
    await device.setup()
    print("status before:", await device.get_status())
    t0 = time.monotonic()
    try:
      await device.self_check()
      print(f"self-check PASSED in {time.monotonic() - t0:.1f} s")
    except Exception as error:  # report the instrument's own fault text
      print(f"self-check FAILED after {time.monotonic() - t0:.1f} s: {type(error).__name__}: {error}")
    print("status after:", await device.get_status())
  finally:
    await device.stop()


if __name__ == "__main__":
  asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "COM6"))
