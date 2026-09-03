import logging
import subprocess

import imageio_ffmpeg

logger = logging.getLogger(__name__)

MAX_VIDEO_SIZE = 20 * 1024 * 1024  # 20 Mo — aligné sur client_max_body_size (nginx)


def _ffmpeg_exe():
    return imageio_ffmpeg.get_ffmpeg_exe()


def compress_video(input_path, output_path):
    """Compresse une vidéo en H.264/AAC, largeur plafonnée à 1280px."""
    subprocess.run(
        [
            _ffmpeg_exe(), '-y', '-i', input_path,
            '-vcodec', 'libx264', '-crf', '28', '-preset', 'medium',
            '-vf', "scale='min(1280,iw)':-2",
            '-acodec', 'aac', '-b:a', '128k',
            '-movflags', '+faststart',
            output_path,
        ],
        check=True, capture_output=True,
    )


def extract_thumbnail(video_path, output_path, timestamp='00:00:01'):
    """Extrait une image de la vidéo pour servir de miniature."""
    subprocess.run(
        [
            _ffmpeg_exe(), '-y', '-ss', timestamp, '-i', video_path,
            '-frames:v', '1', '-q:v', '3',
            output_path,
        ],
        check=True, capture_output=True,
    )
