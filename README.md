
# Ubahn Displayer

A terminal display for live S-Bahn departures at S Greifswalder Str. (Berlin), showing northbound and southbound trains with real-time delays and disruption alerts.

## Run with Docker

No setup required — just run:

```bash
docker run -it shanecolfer/ubahn-displayer
```

## Run locally

```bash
git clone https://github.com/shanecolfer/Ubahn-Displayer.git
cd Ubahn-Displayer
make virtualenv
source .venv/bin/activate
python -m ubahn_displayer
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
