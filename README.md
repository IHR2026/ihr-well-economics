# IHR Well Economics Dashboard

Interactive per-well economics for Ironhead Resources III & II — revenue, volumes,
realized prices, drilling capital, LOE, and payout by well and month.

**Live page:** enable GitHub Pages (Settings → Pages → deploy from `main`, root) and the
dashboard is served at your Pages URL.

## Ask Fable (AI queries)

The "Ask Fable" box answers questions like *"top performing wells from August 2025"*
or *"rank wells by first 5 months of production"* with text + charts. It needs one of:

1. **Your Claude Code CLI** (no API key): download `claude_bridge.py` from this repo and run
   `python3 claude_bridge.py` on your computer, then use the dashboard — it auto-detects
   the bridge at `http://localhost:8787` and routes queries through your Claude login.
2. **An Anthropic API key**: click ⚙ in the dashboard and paste a key from
   console.anthropic.com. It is stored only in your browser.

Charts, filters, and the well explorer work for everyone without any setup.

⚠ This page contains well-level financial data. Anyone with the Pages URL can view it.
