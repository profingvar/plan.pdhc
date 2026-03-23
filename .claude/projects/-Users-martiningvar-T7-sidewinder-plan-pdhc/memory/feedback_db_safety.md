---
name: feedback_db_safety
description: Never perform destructive Docker volume operations — always back up DB first, verify volume names before copying
type: feedback
---

Never run destructive Docker volume operations (rm, copy between volumes, down -v) without explicit user confirmation and a fresh backup.

**Why:** During a directory rename from gateway/ to planp/, a volume copy command ran in the wrong direction and destroyed the production database contents. The data was irrecoverable.

**How to apply:** Before any restart, rebuild, or volume operation: (1) back up with pg_dumpall, (2) verify volume names and directions, (3) use docker-compose down without -v. Treat the database as the most valuable thing in the project. Include backup steps in start.sh. Never assume volumes are safe across directory renames — Docker Compose prefixes volume names with the project directory.
