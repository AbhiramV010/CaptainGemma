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

- 2026-10-18 18:04:44 OK (ollama, 17.7s): {"target_alt_ft": 3500, "target_heading_deg": 80, "target_speed_kts": 108, "callout": "Maintain heading and airspeed."}
- 2026-10-18 18:05:03 OK (ollama, 14.8s): {"target_alt_ft": 3600, "target_heading_deg": 80, "target_speed_kts": 88, "callout": "Increase airspeed slightly."}
- 2026-10-18 18:05:23 OK (ollama, 15.7s): {"target_alt_ft": 3700, "target_heading_deg": 85, "target_speed_kts": 68, "callout": "Increase airspeed gently."}
- 2026-10-18 18:05:42 OK (ollama, 15.5s): {"target_alt_ft": 3950, "target_heading_deg": 85, "target_speed_kts": 82, "callout": "Increase airspeed slightly."}
- 2026-10-18 18:06:02 OK (ollama, 16.1s): {"target_alt_ft": 3800, "target_heading_deg": 86, "target_speed_kts": 72, "callout": "Increase airspeed a little more."}
- 2026-10-18 18:06:22 OK (ollama, 15.8s): {"target_alt_ft": 4377, "target_heading_deg": 90, "target_speed_kts": 84, "callout": "Increase airspeed slightly."}
- 2026-10-18 18:06:42 OK (ollama, 15.7s): {"target_alt_ft": 4437, "target_heading_deg": 92, "target_speed_kts": 72, "callout": "Increase airspeed further."}
- 2026-10-18 18:07:03 OK (ollama, 16.9s): {"target_alt_ft": 4500, "target_heading_deg": 90, "target_speed_kts": 80, "callout": "Increase airspeed further."}
- 2026-10-18 18:07:22 OK (ollama, 15.7s): {"target_alt_ft": 4800, "target_heading_deg": 87, "target_speed_kts": 84, "callout": "Increase airspeed further."}
- 2026-10-18 18:07:42 OK (ollama, 15.4s): {"target_alt_ft": 4850, "target_heading_deg": 95, "target_speed_kts": 85, "callout": "Increase airspeed slightly."}
- 2026-10-18 18:08:01 OK (ollama, 15.4s): {"target_alt_ft": 5400, "target_heading_deg": 105, "target_speed_kts": 95, "callout": "Increase airspeed further."}
- 2026-10-18 18:08:21 OK (ollama, 15.4s): {"target_alt_ft": 5600, "target_heading_deg": 110, "target_speed_kts": 88, "callout": "Increase airspeed further."}
- 2026-10-18 18:08:40 OK (ollama, 15.4s): {"target_alt_ft": 5600, "target_heading_deg": 116, "target_speed_kts": 72, "callout": "Increase airspeed further."}
- 2026-10-18 18:09:00 OK (ollama, 15.5s): {"target_alt_ft": 5800, "target_heading_deg": 125, "target_speed_kts": 75, "callout": "Increase airspeed further."}
- 2026-10-18 18:09:19 OK (ollama, 15.4s): {"target_alt_ft": 5100, "target_heading_deg": 119, "target_speed_kts": 82, "callout": "Increase airspeed further."}
- 2026-10-18 18:09:39 OK (ollama, 16.1s): {"target_alt_ft": 5100, "target_heading_deg": 125, "target_speed_kts": 105, "callout": "Increase airspeed to maintain altitude."}
- 2026-10-18 18:09:59 OK (ollama, 15.7s): {"target_alt_ft": 5700, "target_heading_deg": 127, "target_speed_kts": 95, "callout": "Increase airspeed slightly."}
- 2026-10-18 18:10:19 OK (ollama, 16.0s): {"target_alt_ft": 5900, "target_heading_deg": 121, "target_speed_kts": 90, "callout": "Increase airspeed to maintain altitude."}
- 2026-10-18 18:10:39 OK (ollama, 15.6s): {"target_alt_ft": 5000, "target_heading_deg": 135, "target_speed_kts": 80, "callout": "Increase airspeed to maintain altitude."}
- 2026-10-18 18:10:59 OK (ollama, 16.2s): {"target_alt_ft": 5100, "target_heading_deg": 135, "target_speed_kts": 95, "callout": "Increase airspeed to maintain altitude."}
- 2026-10-18 18:11:22 OK (ollama, 18.9s): {"target_alt_ft": 5800, "target_heading_deg": 130, "target_speed_kts": 105, "callout": "Increase airspeed slightly."}
- 2026-10-18 18:11:45 OK (ollama, 19.1s): {"target_alt_ft": 5900, "target_heading_deg": 135, "target_speed_kts": 85, "callout": "Increase airspeed to maintain altitude."}
- 2026-10-18 18:12:07 OK (ollama, 17.9s): {"target_alt_ft": 5250, "target_heading_deg": 135, "target_speed_kts": 80, "callout": "Increase airspeed slightly."}
- 2026-10-18 18:12:26 OK (ollama, 15.5s): {"target_alt_ft": 5200, "target_heading_deg": 140, "target_speed_kts": 90, "callout": "Increase airspeed to maintain altitude."}
- 2026-10-18 18:12:47 OK (ollama, 17.1s): {"target_alt_ft": 5800, "target_heading_deg": 130, "target_speed_kts": 90, "callout": "Increase airspeed to maintain altitude."}
- 2026-10-18 18:13:13 FAIL (ollama, 22.0s): ReadTimeout: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=20.0) | change: raise CAPTAIN_TIMEOUT_S or use a smaller model
- 2026-10-18 18:13:34 OK (ollama, 16.7s): {"target_alt_ft": 5121, "target_heading_deg": 135, "target_speed_kts": 75, "callout": "Increase airspeed to maintain altitude."}
- 2026-10-18 18:13:57 OK (ollama, 18.6s): {"target_alt_ft": 5200, "target_heading_deg": 135, "target_speed_kts": 95, "callout": "Increase airspeed slightly."}
- 2026-10-18 18:14:18 OK (ollama, 16.9s): {"target_alt_ft": 5800, "target_heading_deg": 130, "target_speed_kts": 97, "callout": "Increase airspeed to maintain altitude."}
- 2026-10-18 18:14:39 OK (ollama, 17.5s): {"target_alt_ft": 5900, "target_heading_deg": 140, "target_speed_kts": 80, "callout": "Increase airspeed slightly."}
- 2026-10-18 18:15:04 OK (ollama, 20.4s): {"target_alt_ft": 5100, "target_heading_deg": 135, "target_speed_kts": 75, "callout": "Increase airspeed to maintain altitude."}
- 2026-10-18 18:15:25 OK (ollama, 17.4s): {"target_alt_ft": 5000, "target_heading_deg": 135, "target_speed_kts": 95, "callout": "Increase airspeed slightly."}
- 2026-10-18 18:15:47 OK (ollama, 18.4s): {"target_alt_ft": 5800, "target_heading_deg": 130, "target_speed_kts": 95, "callout": "Increase airspeed to maintain altitude."}

## Run summary 2026-10-18 18:15:52
- ran 686s, final alt 5466 ft, hdg 131, ias 76 kt, crashes 0
- captain: 34 calls, 1 failures, last response 18.4s, backend ollama


## Run summary 2026-10-18 18:19:31
- ran 10s, final alt 2981 ft, hdg 93, ias 93 kt, crashes 0
- captain: 1 calls, 0 failures, last response 0.0s, backend ollama

- 2026-10-18 19:17:44 FAIL (ollama, 22.1s): ReadTimeout: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=20.0) | change: raise CAPTAIN_TIMEOUT_S or use a smaller model
- 2026-10-18 19:18:10 OK (ollama, 21.5s): {"target_alt_ft": 3490, "target_heading_deg": 89, "target_speed_kts": 102, "callout": "Increase speed slightly."}
- 2026-10-18 19:18:35 OK (ollama, 21.2s): {"target_alt_ft": 3460, "target_heading_deg": 95, "target_speed_kts": 90, "callout": "Maintain speed through the wind."}
- 2026-10-18 19:19:00 OK (ollama, 21.1s): {"target_alt_ft": 3800, "target_heading_deg": 95, "target_speed_kts": 85, "callout": "Increase speed to combat the wind."}
- 2026-10-18 19:19:26 OK (ollama, 21.5s): {"target_alt_ft": 3942, "target_heading_deg": 91, "target_speed_kts": 90, "callout": "Increase speed to maintain altitude."}
- 2026-10-18 19:19:48 OK (ollama, 18.5s): {"target_alt_ft": 4300, "target_heading_deg": 85, "target_speed_kts": 80, "callout": "Increase speed to maintain altitude."}
- 2026-10-18 19:20:10 OK (ollama, 18.3s): {"target_alt_ft": 4500, "target_heading_deg": 87, "target_speed_kts": 98, "callout": "Increase speed to maintain altitude."}
- 2026-10-18 19:20:32 OK (ollama, 18.0s): {"target_alt_ft": 4700, "target_heading_deg": 85, "target_speed_kts": 77, "callout": "Increase speed slightly."}
- 2026-10-18 19:20:54 OK (ollama, 17.8s): {"target_alt_ft": 4900, "target_heading_deg": 97, "target_speed_kts": 80, "callout": "Increase airspeed slightly."}
- 2026-10-18 19:21:17 OK (ollama, 19.2s): {"target_alt_ft": 5200, "target_heading_deg": 85, "target_speed_kts": 80, "callout": "Increase airspeed slightly."}

## Run summary 2026-10-18 19:21:29
- ran 249s, final alt 5201 ft, hdg 88, ias 75 kt, crashes 0
- captain: 11 calls, 1 failures, last response 19.2s, backend ollama

- 2026-10-18 19:29:59 OK (ollama, 21.1s): {"target_alt_ft": 3500, "target_heading_deg": 80, "target_speed_kts": 110, "callout": "Maintain heading and airspeed."}
- 2026-10-18 19:30:21 OK (ollama, 17.3s): {"target_alt_ft": 3600, "target_heading_deg": 85, "target_speed_kts": 95, "callout": "Increase airspeed slightly."}
- 2026-10-18 19:30:42 OK (ollama, 17.6s): {"target_alt_ft": 3700, "target_heading_deg": 95, "target_speed_kts": 70, "callout": "Increase airspeed slightly."}
- 2026-10-18 19:31:04 OK (ollama, 18.0s): {"target_alt_ft": 3950, "target_heading_deg": 89, "target_speed_kts": 84, "callout": "Increase airspeed to maintain heading."}
- 2026-10-18 19:31:26 OK (ollama, 17.8s): {"target_alt_ft": 3650, "target_heading_deg": 89, "target_speed_kts": 75, "callout": "Increase airspeed to maintain heading."}
- 2026-10-18 19:31:48 OK (ollama, 18.0s): {"target_alt_ft": 3900, "target_heading_deg": 90, "target_speed_kts": 85, "callout": "Maintain airspeed."}
- 2026-10-18 19:32:10 OK (ollama, 17.9s): {"target_alt_ft": 3227, "target_heading_deg": 102, "target_speed_kts": 75, "callout": "Increase airspeed slightly."}
- 2026-10-18 19:32:32 OK (ollama, 18.2s): {"target_alt_ft": 3649, "target_heading_deg": 105, "target_speed_kts": 100, "callout": "Increase airspeed slightly."}
- 2026-10-18 19:32:55 OK (ollama, 19.1s): {"target_alt_ft": 3950, "target_heading_deg": 112, "target_speed_kts": 88, "callout": "Increase airspeed slightly."}
- 2026-10-18 19:33:18 OK (ollama, 18.6s): {"target_alt_ft": 4200, "target_heading_deg": 112, "target_speed_kts": 98, "callout": "Maintain airspeed in the wind."}
- 2026-10-18 19:33:40 OK (ollama, 18.5s): {"target_alt_ft": 4600, "target_heading_deg": 110, "target_speed_kts": 95, "callout": "Increase airspeed to maintain heading."}
- 2026-10-18 19:34:03 OK (ollama, 18.8s): {"target_alt_ft": 4800, "target_heading_deg": 115, "target_speed_kts": 95, "callout": "Increase airspeed to maintain heading."}
- 2026-10-18 19:34:26 OK (ollama, 18.5s): {"target_alt_ft": 4850, "target_heading_deg": 110, "target_speed_kts": 82, "callout": "Increase airspeed slightly."}
- 2026-10-18 19:34:48 OK (ollama, 18.2s): {"target_alt_ft": 5300, "target_heading_deg": 107, "target_speed_kts": 85, "callout": "Maintain airspeed to counteract the wind."}
- 2026-10-18 19:35:10 OK (ollama, 18.4s): {"target_alt_ft": 5350, "target_heading_deg": 117, "target_speed_kts": 78, "callout": "Increase airspeed slightly."}
- 2026-10-18 19:35:33 OK (ollama, 18.7s): {"target_alt_ft": 5600, "target_heading_deg": 120, "target_speed_kts": 70, "callout": "Increase airspeed to maintain heading."}
- 2026-10-18 19:35:56 OK (ollama, 18.7s): {"target_alt_ft": 5800, "target_heading_deg": 111, "target_speed_kts": 75, "callout": "Increase airspeed to maintain heading."}
- 2026-10-18 19:36:19 OK (ollama, 18.9s): {"target_alt_ft": 5800, "target_heading_deg": 110, "target_speed_kts": 80, "callout": "Increase airspeed to maintain heading."}
- 2026-10-18 19:36:41 OK (ollama, 18.8s): {"target_alt_ft": 5000, "target_heading_deg": 110, "target_speed_kts": 75, "callout": "Increase airspeed to maintain heading."}
- 2026-10-18 19:37:04 OK (ollama, 18.7s): {"target_alt_ft": 5200, "target_heading_deg": 110, "target_speed_kts": 110, "callout": "Increase airspeed slightly."}
- 2026-10-18 19:37:27 OK (ollama, 19.0s): {"target_alt_ft": 5850, "target_heading_deg": 112, "target_speed_kts": 108, "callout": "Maintain airspeed and heading."}
- 2026-10-18 19:37:49 OK (ollama, 18.2s): {"target_alt_ft": 5900, "target_heading_deg": 108, "target_speed_kts": 97, "callout": "Increase airspeed slightly."}
- 2026-10-18 19:38:12 OK (ollama, 18.3s): {"target_alt_ft": 5200, "target_heading_deg": 115, "target_speed_kts": 80, "callout": "Increase airspeed to maintain altitude."}
- 2026-10-18 19:38:34 OK (ollama, 18.2s): {"target_alt_ft": 5188, "target_heading_deg": 117, "target_speed_kts": 98, "callout": "Increase airspeed slightly."}
- 2026-10-18 19:38:56 OK (ollama, 18.4s): {"target_alt_ft": 5900, "target_heading_deg": 117, "target_speed_kts": 95, "callout": "Increase airspeed to maintain altitude."}
- 2026-10-18 19:39:18 OK (ollama, 18.3s): {"target_alt_ft": 5000, "target_heading_deg": 118, "target_speed_kts": 90, "callout": "Increase airspeed slightly."}
- 2026-10-18 19:39:41 OK (ollama, 18.8s): {"target_alt_ft": 5139, "target_heading_deg": 123, "target_speed_kts": 105, "callout": "Maintain airspeed to climb."}
- 2026-10-18 19:48:13 OK (ollama, 508.1s): {"target_alt_ft": 5700, "target_heading_deg": 121, "target_speed_kts": 108, "callout": "Increase airspeed slightly."}
- 2026-10-18 19:48:33 OK (ollama, 15.7s): {"target_alt_ft": 5800, "target_heading_deg": 120, "target_speed_kts": 75, "callout": "Increase airspeed to maintain climb."}

## Run summary 2026-10-18 19:48:36
- ran 1139s, final alt 5434 ft, hdg 121, ias 68 kt, crashes 0
- captain: 29 calls, 0 failures, last response 15.7s, backend ollama

