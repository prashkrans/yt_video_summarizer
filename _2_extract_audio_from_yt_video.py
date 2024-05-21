from moviepy.editor import VideoFileClip
from _utils import FILE_TYPE, VIDEO_DIR, AUDIO_DIR, PARAMS_JSON_PATH, get_file_from_dir, json_read

# Function to extract audio from a YouTube video
def extract_audio(file_name):
    video_file = get_file_from_dir(VIDEO_DIR, file_name, FILE_TYPE.VIDEO)
    video_file_path = f'{VIDEO_DIR}/{video_file}'
    print(f'Found {video_file}')

    file_name = video_file.split('.')[0]
    output_audio_path = f'{AUDIO_DIR}/{file_name}.wav'

    try:
        video_clip = VideoFileClip(video_file_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(output_audio_path) # Generates higher quality .wav files but could be avoided to save time
        video_clip.close()
        print("Audio extracted successfully!")
    except Exception as e:
        print("An error occurred:", e)

# if __name__ == "__main__": # Commented out as using gradio app instead of running step wise | May need debugging
#     params_dict = json_read(PARAMS_JSON_PATH)
#     file_name = params_dict['FILE_NAME']
#     extract_audio(file_name)

