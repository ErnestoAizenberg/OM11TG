![Python](https://img.shields.io/badge/Python-3.7-9c1aff) ![Flask](https://img.shields.io/badge/Flask-2.2.5-0ff0fc) ![Flask-SQLAlchemy](https://img.shields.io/badge/Flask--SQLAlchemy-3.1.1-00ff9d) ![redis](https://img.shields.io/badge/redis-latest-ff4d4d)

# OM11TG

Telegram integration for Open Manus Agent  

Provides chat UI and notifications, connecting OM11MACOS with open-manus-agent microservices.

## Quick Start

```shell
git clone https://github.com/ErnestoAizenberg/OM11TG.git
cd OM11TG
pip install -r requirements.txt
python run.py
```

- Configure ports during setup (press Enter for defaults)
- Service available at: http://localhost:5001/

## Related Components

- **macOS Web UI**: [OM11MACOS](https://github.com/ErnestoAizenberg/OM11MACOS)
- **Core Agent**: [open-manus-agent](https://github.com/ErnestoAizenberg/open-manus-agent) (Browser + LLM management)
