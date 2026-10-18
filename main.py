"""AI Pilot: sim -> captain -> bridge -> plane. Ctrl+C stops everything."""
import argparse
import os
import sys
import time

import config


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim-only", action="store_true", help="no hardware")
    ap.add_argument("--no-captain", action="store_true", help="hold the start targets")
    ap.add_argument("--backend", choices=["ollama", "api"], default=config.CAPTAIN_BACKEND)
    ap.add_argument("--port", default=config.COM_PORT)
    ap.add_argument("--crash-test", action="store_true", help="dive into the ground to test the crash buzzer")
    args = ap.parse_args()

    from sim import Sim
    from captain import Captain

    sim = Sim()
    print(f"SIM ready: trim pitch {sim.trim_pitch:.2f} deg, alt {sim.state['altitude']:.0f} ft")

    if args.crash_test:
        args.no_captain = True
        sim.set_targets(alt_ft=-2000)
        print("CRASH TEST: diving into the ground (about 40 s)")

    captain = None if args.no_captain else Captain(args.backend)
    if captain:
        captain.warm_up()
        captain.start()

    bridge = None
    if not args.sim_only:
        from bridge import Bridge
        bridge = Bridge(args.port)
        bridge.start()

    dt = 1.0 / config.SIM_HZ
    next_tick = time.perf_counter()
    last_print = 0.0
    stale_printed = False
    crashes = 0
    crash_time = None
    t_start = time.time()
    try:
        while True:
            if crash_time is not None:
                # Crashed: plane centred, sim frozen until the reset
                if config.CRASH_RESET_S and time.time() - crash_time >= config.CRASH_RESET_S:
                    sim.reset()
                    if args.crash_test:
                        sim.set_targets(alt_ft=-2000)
                    crash_time = None
                    print("SIM RESET")
                next_tick = time.perf_counter()
                time.sleep(dt)
                continue

            s = sim.step()
            p, r, y = sim.servo_offsets()
            if s["crashed"]:
                crashes += 1
                crash_time = time.time()
                print(f"CRASH at {s['airspeed']:.0f} kt, pitch {s['pitch']:.0f} deg")
                if bridge:
                    bridge.crash()
                    bridge.set(0, 0, 0)
                continue
            if bridge:
                bridge.set(p, r, y)
            if captain:
                captain.update_state(s)
                if captain.target:
                    t = captain.target
                    sim.set_targets(t["target_alt_ft"], t["target_heading_deg"], t["target_speed_kts"])
                if captain.stale():
                    if not stale_printed:
                        print("CAPTAIN STALE")
                        stale_printed = True
                else:
                    stale_printed = False

            now = time.time()
            if now - last_print >= 1.0:
                last_print = now
                cap = "-"
                if captain and captain.last_call:
                    cap = f"{now - captain.last_call:4.1f}s ago"
                link = "" if not bridge else (" uno=OK" if bridge.connected else " uno=DOWN")
                print(f"alt {s['altitude']:6.0f}ft ({sim.target_alt:.0f})  hdg {s['heading']:5.1f} ({sim.target_heading:.0f})  "
                      f"ias {s['airspeed']:5.1f}kt ({sim.target_speed:.0f})  pitch {s['pitch']:5.1f}  roll {s['roll']:5.1f}  "
                      f"Y{y:+3.0f} P{p:+3.0f} R{r:+3.0f}{'  STALL' if s['stall'] else ''}  captain {cap}{link}",
                      flush=True)

            next_tick += dt
            sleep = next_tick - time.perf_counter()
            if sleep > 0:
                time.sleep(sleep)
            else:
                next_tick = time.perf_counter()     # fell behind; don't try to catch up
    except KeyboardInterrupt:
        print("\nStopping")
    finally:
        if captain:
            captain.stop()
        if bridge:
            bridge.close()
        write_summary(sim, captain, time.time() - t_start, crashes)


def write_summary(sim, captain, elapsed, crashes=0):
    os.makedirs(os.path.dirname(config.ATTEMPTS_MD), exist_ok=True)
    with open(config.ATTEMPTS_MD, "a", encoding="utf-8") as fh:
        fh.write(f"\n## Run summary {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        fh.write(f"- ran {elapsed:.0f}s, final alt {sim.state['altitude']:.0f} ft, hdg {sim.state['heading']:.0f}, "
                 f"ias {sim.state['airspeed']:.0f} kt, crashes {crashes}\n")
        if captain:
            fh.write(f"- captain: {captain.calls} calls, {captain.failures} failures, "
                     f"last response {captain.last_rt or 0:.1f}s, backend {captain.backend}\n")
        fh.write("\n")
    print(f"Summary written to {config.ATTEMPTS_MD}")


if __name__ == "__main__":
    sys.exit(main())
