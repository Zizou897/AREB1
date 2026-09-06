import logging
import subprocess

import imageio_ffmpeg

logger = logging.getLogger(__name__)

MAX_VIDEO_SIZE = 20 * 1024 * 1024  # 20 Mo — aligné sur client_max_body_size (nginx)
ALLOWED_VIDEO_EXTENSIONS = {'.mp4', '.mov', '.webm', '.avi', '.mkv'}


def _ffmpeg_exe():
    return imageio_ffmpeg.get_ffmpeg_exe()


def is_valid_video_file(path):
    """Vérifie que le fichier contient réellement un flux vidéo décodable (pas juste
    une extension trompeuse). Rejette silencieusement tout ce que ffmpeg ne sait pas lire."""
    try:
        subprocess.run(
            [
                _ffmpeg_exe(), '-v', 'error', '-i', path,
                '-map', '0:v:0', '-t', '0.1', '-f', 'null', '-',
            ],
            check=True, capture_output=True, timeout=30,
        )
        return True
    except Exception:
        return False


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
