
# Ubahn Displayer

A terminal display for live public transport departures in Berlin, showing northbound and southbound trains with real-time delays and disruption alerts.

## Run with Docker

No setup required — just run:

```bash
docker run -it shanecolfer/ubahn-displayer
```

You'll be prompted to search for a stop by name, then select from the results. The display will show the next two departures in each direction, updating in real time.

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


## Screens
<img width="1911" height="1072" alt="image" src="https://github.com/user-attachments/assets/fee88889-74c6-4f3f-a7fc-326d6e21adf3" />
