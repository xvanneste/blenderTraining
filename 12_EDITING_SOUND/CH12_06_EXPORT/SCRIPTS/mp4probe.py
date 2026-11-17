"""
mp4probe.py — analyseur minimal de fichiers MP4 (boîtes ISO) : conteneur, codecs, dimensions, durée. Sans dépendance externe (aucun ffprobe sur la machine).
analyse(chemin) -> {"brand": str, "duration": float, "tracks": [{"kind": "vide"|"soun", "codec": "avc1"|"mp4v"|"mp4a"|…, "width": int, "height": int}]}
Testé avec : des fichiers produits par Blender 5.3 (H.264/AAC, MPEG-4 Part 2/AAC) ; ne gère pas tous les cas (boîtes de taille 64 bits, fragments).
"""
import struct


def boxes(data, start, end):
    i = start
    while i + 8 <= end:
        size, typ = struct.unpack(">I4s", data[i:i + 8])
        hdr = 8
        if size == 1:
            size = struct.unpack(">Q", data[i + 8:i + 16])[0]
            hdr = 16
        elif size == 0:
            size = end - i
        if size < hdr:
            return
        yield typ.decode("latin1"), i + hdr, i + size
        i += size


def find(data, start, end, path):
    """Premier enfant de type path[0] ; récursion sur la suite du chemin."""
    for typ, s, e in boxes(data, start, end):
        if typ == path[0]:
            return (s, e) if len(path) == 1 else find(data, s, e, path[1:])
    return None


def analyse(path):
    data = open(path, "rb").read()
    out = {"brand": "", "duration": 0.0, "tracks": []}
    ft = find(data, 0, len(data), ["ftyp"])
    if ft:
        out["brand"] = data[ft[0]:ft[0] + 4].decode("latin1")
    moov = find(data, 0, len(data), ["moov"])
    if not moov:
        return out
    mv = find(data, moov[0], moov[1], ["mvhd"])
    if mv:
        ver = data[mv[0]]
        if ver == 0:
            ts, dur = struct.unpack(">II", data[mv[0] + 12:mv[0] + 20])
        else:
            ts, dur = struct.unpack(">IQ", data[mv[0] + 20:mv[0] + 32])
        out["duration"] = dur / float(ts) if ts else 0.0
    for typ, s, e in boxes(data, moov[0], moov[1]):
        if typ != "trak":
            continue
        hd = find(data, s, e, ["mdia", "hdlr"])
        kind = data[hd[0] + 8:hd[0] + 12].decode("latin1") if hd else ""
        sd = find(data, s, e, ["mdia", "minf", "stbl", "stsd"])
        codec, w, h = "", 0, 0
        if sd:
            ent = sd[0] + 8
            codec = data[ent + 4:ent + 8].decode("latin1")
            if kind == "vide":
                w, h = struct.unpack(">HH", data[ent + 32:ent + 36])
        out["tracks"].append({"kind": kind, "codec": codec, "width": w, "height": h})
    return out


if __name__ == "__main__":
    import json
    import sys
    print(json.dumps(analyse(sys.argv[1]), indent=1))
