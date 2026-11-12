# 405 TS washer: running it from a laptop

Lab scripts for a BioTek 405 TS microplate washer (REF 405TSRS: single 96-tube manifold,
ultrasonic cleaner, one buffer). They use the `Washer405TS` driver from
[PyLabRobot pull request #1266](https://github.com/PyLabRobot/pylabrobot/pull/1266), which is not
merged into PyLabRobot yet. This branch is that pull request's code (commit `53c63b36c`) plus
this folder.

## Safety rule

Never drive the washer from code without an explicit go-ahead for that run. This is the PyLabRobot
repo's rule (`AGENTS.md`), and approval for one run doesn't carry over to the next.

Before every run:
- The washer's touch screen shows the **Home screen**. The washer only talks to a computer from there.
- Nothing else has the washer's COM port open.
- Mist shield on, hands clear.
- Only one cable connected: the washer's USB port **or** its RS232 port, never both.

## Setup (Windows)

1. Install **Python 3.10 or newer** (python.org) and **Git** (git-scm.com).
2. Clone this branch and install:

   ```
   git clone -b lab/405ts-handover https://github.com/KarlAntoun/pylabrobot.git
   cd pylabrobot
   python -m venv .venv
   .venv\Scripts\python -m pip install -e ".[serial]"
   ```

3. Plug the washer's USB cable into the laptop. Windows installs the FTDI driver by itself.
4. Find the port: Device Manager > Ports (COM & LPT) > "USB Serial Port (COMn)". On the first
   laptop it was COM6.

## Scripts

Run them from the repo root, with your COM number:

```
.venv\Scripts\python lab\405ts\readonly_405ts.py COM6
```

| Script | What it does | Moves anything? |
|---|---|---|
| `readonly_405ts.py` | Pings, then prints fitted options, serial number, firmware and status | No. Queries only. |
| `selfcheck_405ts.py` | Runs the washer's self-check, about 16 s | Yes: homes the motors, empties the trough, tests the vacuum. No buffer is pumped. Needs the waste bottles and pump connected. |

Results on 12 Nov 2026: both passed. The washer reported firmware 1.40 (basecode 1170202, settings
data version 103), a single 96-tube manifold and the ultrasonic cleaner, and the driver's own unit
tests passed (824 passed, 184 skipped).

## Still to do

- **Fit the supply-bottle filter first** (PN 01310, plus steel adapter PN 1172031 if the tube end is
  bare). Nothing that pumps fluid runs until it's on.
- Then, one run at a time: prime, a short wash on an empty 96-well plate, and an ultrasonic
  auto-clean. The driver has `washer.prime(...)`, `washer.wash(...)` and `washer.auto_clean(...)`;
  check their arguments in `pylabrobot/agilent/biotek/lhc/devices/components/washer.py` first.
- Post those results as a follow-up on pull request #1266. The first test report is
  [here](https://github.com/PyLabRobot/pylabrobot/pull/1266#issuecomment-6826837752).

## If the port doesn't open

Check the COM number in Device Manager again, and that nothing else has the port open. After a
washer error the USB link can drop; unplug and replug the cable, then retry.
