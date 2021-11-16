import os
from collections import namedtuple
from datetime import datetime, timedelta
from enum import Enum
from multiprocessing import Pool

from moviepy.editor import CompositeAudioClip, VideoFileClip


THREADS = int(os.getenv("THREADS", 1))
PROCESSES = int(os.getenv("PROCESSES", os.cpu_count()))


# This is the master-piece from Maccio
master = VideoFileClip("auguri.mp4")

# Here we extract the sub-clips for all the different occasions:
BaseVideoClip = namedtuple("BaseVideoClip", ["name", "clip"])


class BaseClip(Enum):
    BIRTHDAY = "compleanno"
    DIPLOMA = "laurea"
    WEDDING = "matrimonio"
    DEATH = "morte"


BASE_CLIPS = {
    BaseClip.BIRTHDAY: BaseVideoClip("compleanno", master.subclip(49.5, 55)),
    BaseClip.DIPLOMA: BaseVideoClip("laurea", master.subclip(57.3, 62)),
    BaseClip.WEDDING: BaseVideoClip("matrimonio", master.subclip(63.8, 70)),
    BaseClip.DEATH: BaseVideoClip(
        "morte", master.subclip(17 * 60 + 31.8, 17 * 60 + 36)
    ),
}


# For each name we'll keep a data structure with the corresponding
# starting and ending time on the master track, so we can extract
# the relevant audio clip:
NameClip = namedtuple("NameClip", ["start", "stop"])


def load_names(path="names.txt"):
    loaded_names = {}
    with open(path, "r") as names:
        while True:
            start_time_line = names.readline().rstrip()
            if not start_time_line:
                break

            try:
                start_time = datetime.strptime(start_time_line, "%M:%S.%f")
            except ValueError:
                start_time = datetime.strptime(start_time_line, "%M:%S")

            end_time = (start_time + timedelta(seconds=2)).strftime("%M:%S.%f")
            name = names.readline().rstrip()
            loaded_names[name] = NameClip(start_time_line, end_time)
    return loaded_names


NAMES = load_names()


def get_name_clip(name):
    found = NAMES[name]
    return master.subclip(found.start, found.stop).audio


def overlay_name(name_clip, base_clip=BaseClip.BIRTHDAY):
    master_clip = BASE_CLIPS[base_clip].clip
    composite_audio = CompositeAudioClip(
        clips=[master_clip.audio, name_clip.set_start(1.2)],
    )
    return master_clip.set_audio(composite_audio)


def make_clip(name, base_clip=BaseClip.BIRTHDAY):
    name_clip = get_name_clip(name)
    return overlay_name(name_clip, base_clip=base_clip)


def reload_clip(name, base_clip=BaseClip.BIRTHDAY):
    global NAMES
    NAMES = load_names()
    make_clip(name, base_clip=base_clip).write_videofile(
        f"output/{base_clip.value}/{name}.mp4", threads=THREADS
    )


def generate_and_save_clip(name, clip_type):
    output_file = f"output/{clip_type.value}/{name}.mp4"
    if os.path.exists(output_file):
        return

    print(f"Making clip {output_file}")
    clip = make_clip(name=name, base_clip=clip_type)
    clip.write_videofile(output_file, threads=THREADS)


if __name__ == "__main__":
    with Pool(PROCESSES) as pool:

        # Pre-generate all possible clips
        clip_combinations = []
        for clip_type in BaseClip:
            os.makedirs(f"output/{clip_type.value}", exist_ok=True)

            for name in NAMES:
                clip_combinations.append((name, clip_type))

        # Run them on the multiprocess pool
        pool.starmap(generate_and_save_clip, clip_combinations)
