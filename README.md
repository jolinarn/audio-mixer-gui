# Audio Mixer GUI

A small PyQt6 tray app for mixing and routing audio across a fixed set of
PulseAudio/PipeWire virtual sinks — handy if you split app audio across
multiple virtual sinks (e.g. a "desktop" sink you screen-share/stream and a
"private" sink for things like music or browser audio you want to keep out
of the capture).

For each managed sink it shows:
- a volume slider and mute toggle
- a live list of the apps currently playing through that sink
- a dropdown on each app to move its audio stream to one of the other
  managed sinks on the fly

Runs as a normal window and lives in the system tray; click the tray icon
to show/hide it.

## Requirements

- PyQt6
- [pulsectl](https://github.com/mk-fg/python-pulsectl) (works against
  PipeWire via `pipewire-pulse`)

```
pip install -r requirements.txt
```

On Arch/CachyOS these are also packaged: `pacman -S python-pyqt6 python-pulsectl`.

## Running

```
python3 main.py
```

## Configuring sinks

By default it manages two sinks named `desktop_audio` and `music_private`
(see `DEFAULT_SINK_NAMES` in `mixer_backend.py`). Edit that list — or pass
your own list to `AudioMixerBackend(sink_names=[...])` in `main.py` — to
match sink names you've created yourself, e.g. via:

```
pactl load-module module-null-sink sink_name=desktop_audio sink_properties=device.description="Desktop-Audio"
```

The app only manages sinks that already exist; it doesn't create them.

## Autostart

To launch on login, add a `.desktop` file to `~/.config/autostart/` that
runs `python3 /path/to/main.py`.
