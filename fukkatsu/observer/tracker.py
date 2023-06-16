import logging

track = logging.getLogger(__name__)
track.setLevel(logging.WARNING)

handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)

formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)

track.addHandler(handler)
