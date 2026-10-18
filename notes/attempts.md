# Captain attempts

One line per call: what failed and what to change.

- 2026-10-18 16:44:34 FAIL (ollama, 12.1s): ReadTimeout: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=10.0) | change: raise CAPTAIN_TIMEOUT_S or use a smaller model
- 2026-10-18 16:44:53 FAIL (ollama, 12.1s): ReadTimeout: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=10.0) | change: raise CAPTAIN_TIMEOUT_S or use a smaller model
- 2026-10-18 16:45:06 FAIL (ollama, 12.1s): ReadTimeout: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=10.0) | change: raise CAPTAIN_TIMEOUT_S or use a smaller model
- 2026-10-18 16:45:58 FAIL (ollama, 12.1s): ReadTimeout: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=10.0) | change: raise CAPTAIN_TIMEOUT_S or use a smaller model
- 2026-10-18 16:47:00 OK (ollama, 8.8s): {"target_alt_ft": 3500, "target_heading_deg": 90, "target_speed_kts": 105, "callout": "Maintain heading and airspeed."}
- 2026-10-18 16:47:30 OK (ollama, 17.3s): {"target_alt_ft": 3500, "target_heading_deg": 95, "target_speed_kts": 105, "callout": "Leveling out now."}
- 2026-10-18 16:47:52 OK (ollama, 17.3s): {"target_alt_ft": 3500, "target_heading_deg": 90, "target_speed_kts": 105, "callout": "Maintaining heading and altitude."}
- 2026-10-18 17:03:23 OK (ollama, 15.0s): {"target_alt_ft": 3500, "target_heading_deg": 90, "target_speed_kts": 105, "callout": "Maintain heading and airspeed."}
- 2026-10-18 17:15:23 OK (ollama, 16.8s): {"target_alt_ft": 3500, "target_heading_deg": 95, "target_speed_kts": 105, "callout": "Leveling out now."}
- 2026-10-18 17:15:41 OK (ollama, 13.8s): {"target_alt_ft": 3600, "target_heading_deg": 90, "target_speed_kts": 90, "callout": "Slightly higher heading."}
- 2026-10-18 17:16:10 OK (ollama, 13.6s): {"target_alt_ft": 3500, "target_heading_deg": 90, "target_speed_kts": 105, "callout": "Maintain heading and airspeed."}
- 2026-10-18 17:16:28 OK (ollama, 13.7s): {"target_alt_ft": 3600, "target_heading_deg": 90, "target_speed_kts": 90, "callout": "Level flight maintained."}
- 2026-10-18 17:16:45 OK (ollama, 13.8s): {"target_alt_ft": 3900, "target_heading_deg": 90, "target_speed_kts": 90, "callout": "Maintain current airspeed."}
- 2026-10-18 17:35:44 OK (ollama, 16.4s): {"target_alt_ft": 3500, "target_heading_deg": 90, "target_speed_kts": 105, "callout": "Maintain heading and airspeed."}
- 2026-10-18 17:36:01 OK (ollama, 13.5s): {"target_alt_ft": 3600, "target_heading_deg": 90, "target_speed_kts": 90, "callout": "Level flight maintained."}
- 2026-10-18 17:36:18 OK (ollama, 13.3s): {"target_alt_ft": 3900, "target_heading_deg": 90, "target_speed_kts": 88, "callout": "Maintain current airspeed."}
- 2026-10-18 17:36:36 OK (ollama, 13.6s): {"target_alt_ft": 3650, "target_heading_deg": 90, "target_speed_kts": 88, "callout": "Continue maintaining airspeed."}
- 2026-10-18 17:36:54 OK (ollama, 13.6s): {"target_alt_ft": 4200, "target_heading_deg": 90, "target_speed_kts": 95, "callout": "Level flight is maintained."}
- 2026-10-18 17:37:11 OK (ollama, 13.4s): {"target_alt_ft": 4312, "target_heading_deg": 92, "target_speed_kts": 86, "callout": "Maintain current airspeed."}
- 2026-10-18 17:37:29 OK (ollama, 14.2s): {"target_alt_ft": 4500, "target_heading_deg": 90, "target_speed_kts": 80, "callout": "Maintain airspeed and heading."}
- 2026-10-18 17:45:35 OK (ollama, 17.0s): {"target_alt_ft": 3500, "target_heading_deg": 90, "target_speed_kts": 105, "callout": "Maintain heading and airspeed."}
- 2026-10-18 17:45:53 OK (ollama, 14.1s): {"target_alt_ft": 3600, "target_heading_deg": 90, "target_speed_kts": 90, "callout": "Level flight maintained."}
- 2026-10-18 17:46:11 OK (ollama, 13.6s): {"target_alt_ft": 3900, "target_heading_deg": 90, "target_speed_kts": 90, "callout": "Maintain current airspeed."}
- 2026-10-18 17:46:28 OK (ollama, 13.3s): {"target_alt_ft": 3618, "target_heading_deg": 90, "target_speed_kts": 88, "callout": "Continue maintaining airspeed."}
- 2026-10-18 17:46:46 OK (ollama, 13.8s): {"target_alt_ft": 4200, "target_heading_deg": 88, "target_speed_kts": 98, "callout": "Maintain current heading and airspeed."}
- 2026-10-18 17:47:04 OK (ollama, 14.4s): {"target_alt_ft": 4200, "target_heading_deg": 89, "target_speed_kts": 80, "callout": "Maintain airspeed and heading."}
- 2026-10-18 17:47:22 OK (ollama, 14.1s): {"target_alt_ft": 4500, "target_heading_deg": 90, "target_speed_kts": 75, "callout": "Maintain airspeed and heading."}
- 2026-10-18 17:47:41 OK (ollama, 14.8s): {"target_alt_ft": 4700, "target_heading_deg": 89, "target_speed_kts": 80, "callout": "Maintain airspeed and heading."}
- 2026-10-18 17:48:00 OK (ollama, 14.4s): {"target_alt_ft": 4900, "target_heading_deg": 90, "target_speed_kts": 75, "callout": "Maintain current airspeed and heading."}
- 2026-10-18 17:48:18 OK (ollama, 14.0s): {"target_alt_ft": 4800, "target_heading_deg": 90, "target_speed_kts": 75, "callout": "Maintain airspeed and heading."}
- 2026-10-18 17:49:09 OK (ollama, 14.4s): {"target_alt_ft": 3500, "target_heading_deg": 80, "target_speed_kts": 108, "callout": "Maintain heading and airspeed."}
- 2026-10-18 17:49:28 OK (ollama, 14.3s): {"target_alt_ft": 3600, "target_heading_deg": 85, "target_speed_kts": 95, "callout": "Increase airspeed slightly."}

## Run summary 2026-10-18 17:49:28
- ran 35s, final alt 3212 ft, hdg 84, ias 81 kt, crashes 0
- captain: 2 calls, 0 failures, last response 14.3s, backend ollama

- 2026-10-18 17:50:51 OK (ollama, 14.7s): {"target_alt_ft": 3500, "target_heading_deg": 82, "target_speed_kts": 108, "callout": "Maintain current heading and speed."}
- 2026-10-18 17:51:09 OK (ollama, 14.3s): {"target_alt_ft": 3600, "target_heading_deg": 85, "target_speed_kts": 88, "callout": "Increase speed slightly."}
- 2026-10-18 17:51:28 OK (ollama, 14.6s): {"target_alt_ft": 3750, "target_heading_deg": 82, "target_speed_kts": 80, "callout": "Increase speed to maintain altitude."}
- 2026-10-18 17:51:47 OK (ollama, 14.8s): {"target_alt_ft": 3700, "target_heading_deg": 85, "target_speed_kts": 88, "callout": "Increase speed to maintain altitude."}
- 2026-10-18 17:52:05 OK (ollama, 14.5s): {"target_alt_ft": 3650, "target_heading_deg": 86, "target_speed_kts": 90, "callout": "Increase speed slightly."}
- 2026-10-18 17:52:24 OK (ollama, 14.8s): {"target_alt_ft": 4200, "target_heading_deg": 93, "target_speed_kts": 105, "callout": "Increase speed to maintain altitude."}
- 2026-10-18 17:52:43 OK (ollama, 15.0s): {"target_alt_ft": 3300, "target_heading_deg": 105, "target_speed_kts": 95, "callout": "Increase speed slightly."}
- 2026-10-18 17:53:02 OK (ollama, 14.9s): {"target_alt_ft": 3346, "target_heading_deg": 102, "target_speed_kts": 105, "callout": "Maintain speed to climb."}
- 2026-10-18 17:53:21 OK (ollama, 14.8s): {"target_alt_ft": 3950, "target_heading_deg": 115, "target_speed_kts": 105, "callout": "Increase speed to maintain altitude."}
- 2026-10-18 17:53:40 OK (ollama, 15.0s): {"target_alt_ft": 3680, "target_heading_deg": 118, "target_speed_kts": 85, "callout": "Increase speed to maintain altitude."}
- 2026-10-18 17:53:58 OK (ollama, 14.8s): {"target_alt_ft": 4300, "target_heading_deg": 120, "target_speed_kts": 105, "callout": "Increase speed slightly."}
- 2026-10-18 17:54:20 OK (ollama, 17.3s): {"target_alt_ft": 4450, "target_heading_deg": 130, "target_speed_kts": 80, "callout": "Maintain speed to climb."}
- 2026-10-18 17:54:39 OK (ollama, 15.0s): {"target_alt_ft": 4700, "target_heading_deg": 135, "target_speed_kts": 85, "callout": "Increase speed to maintain altitude."}

## Run summary 2026-10-18 17:54:48
- ran 253s, final alt 4316 ft, hdg 134, ias 72 kt, crashes 0
- captain: 14 calls, 0 failures, last response 15.0s, backend ollama

