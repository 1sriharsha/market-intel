# MIOS Deployment Guide

Deploy the full Market Intelligence Operating System on Oracle Cloud Free Tier — permanently free, no expiry.

**What you get:** 4-core ARM CPU · 24 GB RAM · 200 GB storage · $0/month forever

---

## Prerequisites

Before touching the server, collect all API keys. Everything listed as Free has no cost.

| Key | Where to get it | Cost |
|---|---|---|
| `ANTHROPIC_API_KEY` | console.anthropic.com | Pay-per-use (~$2–5/month) |
| `OPENAI_API_KEY` | platform.openai.com | Pay-per-use (~$1–3/month) |
| `TELEGRAM_BOT_TOKEN` | Message `@BotFather` on Telegram → `/newbot` | Free |
| `TELEGRAM_CHAT_ID` | Message `@userinfobot` on Telegram | Free |
| `FINNHUB_API_KEY` | finnhub.io/register | Free |
| `MARKETAUX_API_KEY` | marketaux.com | Free |
| `ALPHA_VANTAGE_KEY` | alphavantage.co/support/#api-key | Free |

---

## Step 1 — Push the code to GitHub

Do this on your local machine first. The VM will clone from GitHub.

```bash
cd /path/to/market-intel

git init
git add .
git commit -m "initial: MIOS v1"

# Create a private GitHub repo and push (requires GitHub CLI)
gh repo create market-intel --private --push --source=.
```

If you don't have the GitHub CLI: create the repo at github.com manually, then:

```bash
git remote add origin https://github.com/YOUR_USERNAME/market-intel.git
git push -u origin main
```

---

## Step 2 — Provision Oracle Cloud VM

### 2.1 Create account

Go to [cloud.oracle.com](https://cloud.oracle.com) and sign up.
- Use a credit card for identity verification — you will not be charged
- Choose the region closest to you (US East Ashburn recommended)

### 2.2 Create the VM instance

1. Console → Compute → Instances → **Create Instance**
2. Name: `mios-prod`
3. Image: **Ubuntu 22.04** (Canonical)
4. Shape: Click "Change Shape" → Ampere → **VM.Standard.A1.Flex**
   - OCPUs: **4**
   - Memory: **24 GB**
5. Networking: accept defaults (creates a new VCN)
6. SSH keys: upload your public key (`~/.ssh/id_ed25519.pub`)
   - If you don't have one: `ssh-keygen -t ed25519` on your Mac first
7. Boot volume: **100 GB**
8. Click **Create**

Wait ~2 minutes. Note the **Public IP** on the instance detail page.

### 2.3 Add a Block Volume for database storage

The boot volume is ephemeral risk. Store all data on a separate block volume.

1. Block Storage → Block Volumes → **Create Block Volume**
2. Name: `mios-data`
3. Size: **100 GB**
4. Same Availability Domain as your VM
5. Click Create
6. After it's provisioned: Actions → **Attach to Instance**
   - Attachment type: **Paravirtualized**
   - Access: Read/Write

### 2.4 Reserve a public IP (recommended)

Prevents your IP from changing on VM reboots.

Networking → IP Management → Reserved IPs → Reserve IP → associate with your instance.

---

## Step 3 — Open the Oracle firewalls

Oracle has **two independent firewalls**. Miss either one and nothing connects.

### 3.1 VCN Security List (cloud-level)

Networking → Virtual Cloud Networks → your VCN → Security Lists → Default Security List → **Add Ingress Rules**

| Source CIDR | Protocol | Dest Port | Notes |
|---|---|---|---|
| `0.0.0.0/0` | TCP | 22 | SSH |
| `YOUR_HOME_IP/32` | TCP | 8000 | API server — restrict to your IP |
| `YOUR_HOME_IP/32` | TCP | 3000 | Grafana — restrict to your IP |

Find your home IP: `curl ifconfig.me`

Do **not** expose ports 5432 (Postgres) or 6379 (Redis) — access those via SSH tunnel only.

### 3.2 OS-level firewall (iptables)

Ubuntu 22.04 on Oracle ships with iptables blocking everything beyond SSH.

```bash
ssh ubuntu@YOUR_PUBLIC_IP

sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8000 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 3000 -j ACCEPT
sudo apt-get install iptables-persistent -y
sudo netfilter-persistent save
```

---

## Step 4 — Initial server setup

```bash
ssh ubuntu@YOUR_PUBLIC_IP

# System update
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y git curl wget htop unzip tmux netfilter-persistent

# Non-negotiable: UTC timezone
sudo timedatectl set-timezone UTC

# 8 GB swap — prevents OOM during 2–4 hour bootstrap
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Mount the block volume

```bash
# Identify the block volume device (usually /dev/sdb)
lsblk

# Format — run this ONCE only. Skip if re-attaching an existing volume.
sudo mkfs.ext4 /dev/sdb

# Mount
sudo mkdir -p /mnt/data
sudo mount /dev/sdb /mnt/data

# Auto-mount on reboot
echo '/dev/sdb /mnt/data ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab

# Create directories for Postgres and Redis data
sudo mkdir -p /mnt/data/postgres /mnt/data/redis
sudo chmod 777 /mnt/data/postgres /mnt/data/redis
```

### Install Docker

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu
newgrp docker

# Verify
docker --version
docker compose version
```

---

## Step 5 — Deploy the application

```bash
# Clone your repo
git clone https://github.com/YOUR_USERNAME/market-intel.git
cd market-intel

# Create the environment file
cp .env.example .env
nano .env
```

Fill in every value in `.env`:

```env
# Database — use the service name "postgres" as the host (Docker internal DNS)
DATABASE_URL=postgresql+asyncpg://mios:CHANGE_THIS_PASSWORD@postgres:5432/mios
DB_PASSWORD=CHANGE_THIS_PASSWORD

# Redis
REDIS_URL=redis://redis:6379/0

# LLM APIs
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Telegram delivery
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...

# Market data APIs (all free tier)
FINNHUB_API_KEY=...
MARKETAUX_API_KEY=...
ALPHA_VANTAGE_KEY=...

# Grafana
GRAFANA_PASSWORD=CHANGE_THIS_PASSWORD

# Optional
SIGNIFICANCE_THRESHOLD=65.0
MAX_DAILY_ALERTS=5
ALERT_COOLDOWN_HOURS=4
RAG_CORPUS_DAYS=730
```

### Build the Docker image

```bash
docker compose build
```

---

## Step 6 — Bootstrap (run once, takes 2–4 hours)

This loads historical price data, macro series, and seeds the analogue database. Intelligence quality depends on this data being present.

```bash
# 1. Start databases only
docker compose up -d postgres redis
sleep 15

# 2. Run database migrations
docker compose run --rm api_server alembic upgrade head

# 3. Validate all 100+ RSS feeds are reachable
docker compose run --rm api_server python scripts/validate_sources.py

# 4. Run bootstrap — use tmux so SSH disconnect doesn't kill it
tmux new -s bootstrap
docker compose run --rm api_server python scripts/bootstrap.py
```

Detach from tmux without stopping it: `Ctrl+B` then `D`

Re-attach later to check progress: `tmux attach -t bootstrap`

```bash
# 5. After bootstrap completes: embed articles (can run overnight)
tmux new -s embed
docker compose run --rm api_server python scripts/backfill_embeddings.py
```

---

## Step 7 — Start all services

```bash
docker compose up -d

# Verify all 9 containers are running
docker compose ps
```

Expected output:

| Service | Status |
|---|---|
| `postgres` | healthy |
| `redis` | healthy |
| `api_server` | healthy |
| `ingestion_worker` | running |
| `enrichment_worker` | running |
| `intelligence_worker` | running |
| `delivery_worker` | running |
| `celery_beat` | running |
| `prometheus` | running |
| `grafana` | running |

```bash
# Trigger the first intelligence cycle manually
curl -X POST http://localhost:8000/intelligence/trigger

# Check system status
curl http://localhost:8000/status | python3 -m json.tool
```

Within 60 minutes you should receive a Telegram alert if any article scores above 70.

---

## Step 8 — Access from your laptop

Never expose Postgres, Redis, or Prometheus to the internet. Use SSH tunnels.

### Add to `~/.ssh/config` on your Mac

```
Host mios
  HostName YOUR_PUBLIC_IP
  User ubuntu
  IdentityFile ~/.ssh/id_ed25519
  LocalForward 8000 localhost:8000
  LocalForward 3000 localhost:3000
  LocalForward 9090 localhost:9090
  LocalForward 5432 localhost:5432
  ServerAliveInterval 60
  ServerAliveCountMax 3
```

### Connect

```bash
ssh mios
```

That one command connects SSH and forwards all ports. Then open in your browser:

| URL | What you see |
|---|---|
| http://localhost:8000/health | `{"status":"ok"}` — basic liveness |
| http://localhost:8000/status | Ingestion lag, feed health, article counts |
| http://localhost:8000/articles | Articles coming in with significance scores |
| http://localhost:8000/intelligence | Intelligence objects Claude has generated |
| http://localhost:8000/sources | All 100+ feed sources with health state |
| http://localhost:3000 | Grafana dashboard (admin / your GRAFANA_PASSWORD) |

**The primary output is Telegram.** Everything else is monitoring.

---

## Day-to-day operations

```bash
# Live logs for any service
docker compose logs -f intelligence_worker
docker compose logs -f ingestion_worker

# Resource usage across all containers
docker stats

# Trigger a manual intelligence cycle
curl -X POST http://localhost:8000/intelligence/trigger

# Disable a broken feed without deleting it
docker compose exec postgres psql -U mios -c \
  "UPDATE source_feeds SET is_active = false WHERE id = 'feed_slug';"

# Weekly database backup
docker compose exec postgres pg_dump -U mios mios | gzip > ~/backup_$(date +%Y%m%d).sql.gz
```

### Deploy a code update

```bash
git pull
docker compose build
docker compose up -d
docker compose run --rm api_server alembic upgrade head   # only if migrations changed
```

---

## Troubleshooting

| Problem | What to check |
|---|---|
| Can't SSH into VM | Check VCN Security List allows port 22 from your IP |
| Port 8000 not reachable | Both firewalls must be open — VCN Security List AND iptables |
| No articles ingesting | `curl localhost:8000/sources` — check `last_error` on each feed |
| No Telegram messages | `curl localhost:8000/intelligence` — if objects exist but aren't sent, check `significance_level` (only `critical`/`high` are delivered) |
| DB connection error | `docker compose ps` — confirm postgres is `healthy`, not just `running` |
| Intelligence not running | `docker compose logs celery_beat` — verify beat schedule is firing |
| Bootstrap interrupted | Re-run `python scripts/bootstrap.py` — it resumes from where it stopped |
| OOM during bootstrap | Check swap is active: `free -h` — should show 8G swap |

**`GET /status` is always the first thing to check** — it shows ingestion lag, embedding backlog, last intelligence run time, and feed health in one response.

---

## Cost summary

| Resource | Cost |
|---|---|
| Oracle VM (4 OCPU, 24 GB RAM) | Free forever |
| Oracle Block Volume (200 GB) | Free forever |
| Oracle Bandwidth (10 TB/month egress) | Free forever |
| Anthropic Claude (intelligence generation, ~60 calls/day) | ~$3–8/month |
| OpenAI Embeddings (text-embedding-3-small) | ~$1–3/month |
| All other APIs (Finnhub, Marketaux, Alpha Vantage, FRED) | Free |
| **Total** | **~$4–11/month** |

---

## Architecture running on the VM

```
Oracle ARM VM (4 OCPU · 24 GB RAM)
│
├── api_server          FastAPI on :8000
├── ingestion_worker    RSS + EDGAR every 15 min
├── enrichment_worker   Embeddings + abnormal returns
├── intelligence_worker Claude intelligence cycle every 60 min
├── delivery_worker     Telegram alerts
├── celery_beat         Scheduler
├── postgres            PostgreSQL 15 + TimescaleDB + pgvector (on /mnt/data)
├── redis               Cache + Celery broker (on /mnt/data)
├── prometheus          Metrics on :9090
└── grafana             Dashboard on :3000
```

All containers share a Docker bridge network. Only ports 8000 and 3000 are exposed externally. Postgres and Redis are only accessible on localhost or via SSH tunnel.
