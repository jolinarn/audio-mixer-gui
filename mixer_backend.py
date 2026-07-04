"""PulseAudio/PipeWire backend for the audio mixer GUI.

Wraps pulsectl to manage a fixed set of virtual sinks (e.g. sinks created by
module-null-sink for routing app audio separately, such as a "desktop" vs.
"private" split for stream/screen-share setups).
"""
from __future__ import annotations

import pulsectl

DEFAULT_SINK_NAMES = ["desktop_audio", "music_private"]


def _app_label(sink_input) -> str:
    proplist = sink_input.proplist
    return (
        proplist.get("application.name")
        or proplist.get("media.name")
        or proplist.get("application.process.binary")
        or sink_input.name
        or f"stream #{sink_input.index}"
    )


class AudioMixerBackend:
    def __init__(self, sink_names: list[str] = None):
        self.sink_names = sink_names or DEFAULT_SINK_NAMES
        self._pulse = pulsectl.Pulse("audio-mixer-gui")

    def close(self):
        self._pulse.close()

    def _reconnect(self):
        try:
            self._pulse.close()
        except Exception:
            pass
        self._pulse = pulsectl.Pulse("audio-mixer-gui")

    def _call(self, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except pulsectl.PulseError:
            self._reconnect()
            fn = getattr(self._pulse, fn.__name__)
            return fn(*args, **kwargs)

    def _find_sink(self, sink_name: str):
        for sink in self._pulse.sink_list():
            if sink.name == sink_name:
                return sink
        return None

    def get_sinks(self) -> list[dict]:
        """Return managed sinks in configured order, each as a plain dict."""
        sinks = self._call(self._pulse.sink_list)
        by_name = {s.name: s for s in sinks}
        result = []
        for name in self.sink_names:
            sink = by_name.get(name)
            if sink is None:
                continue
            result.append(
                {
                    "name": sink.name,
                    "description": sink.description,
                    "index": sink.index,
                    "volume": round(sink.volume.value_flat * 100),
                    "muted": bool(sink.mute),
                }
            )
        return result

    def get_apps_by_sink(self) -> dict[int, list[dict]]:
        """Map sink index -> list of app stream dicts for managed sinks."""
        managed_indexes = {s["index"] for s in self.get_sinks()}
        apps_by_sink: dict[int, list[dict]] = {idx: [] for idx in managed_indexes}
        for stream in self._call(self._pulse.sink_input_list):
            if stream.sink not in managed_indexes:
                continue
            apps_by_sink[stream.sink].append(
                {
                    "index": stream.index,
                    "label": _app_label(stream),
                    "sink_index": stream.sink,
                }
            )
        return apps_by_sink

    def set_volume(self, sink_name: str, percent: int):
        sink = self._find_sink(sink_name)
        if sink is None:
            return
        percent = max(0, min(150, percent))
        self._call(self._pulse.volume_set_all_chans, sink, percent / 100)

    def set_mute(self, sink_name: str, muted: bool):
        sink = self._find_sink(sink_name)
        if sink is None:
            return
        self._call(self._pulse.mute, sink, muted)

    def move_app(self, app_index: int, target_sink_name: str):
        sink = self._find_sink(target_sink_name)
        if sink is None:
            return
        self._call(self._pulse.sink_input_move, app_index, sink.index)
