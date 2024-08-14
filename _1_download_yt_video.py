from yt_dlp import YoutubeDL
from _utils import VIDEO_DIR, PARAMS_JSON_PATH, json_read, RESOLUTION_MAP


# Downloading a video in 360p as we only need its audio
def download_video(yt_video_url, file_name, resolution_key="HD"):
    resolution = RESOLUTION_MAP[resolution_key]
    try:
        format='mp4'
        print(f'Download in progress at resolution: {resolution}')
        downloaded_video_path_wo_ext = f'{VIDEO_DIR}/{file_name}'
        downloaded_video_path = f'{VIDEO_DIR}/{file_name}.mp4'
        ydl_opts = {
            # 'format': f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]',
            'format': f'bestvideo[height<={resolution}]+bestaudio[ext=m4a]',
            'outtmpl': downloaded_video_path_wo_ext,
            'merge_output_format': format,
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(yt_video_url)
        print("Video downloaded successfully")
        print(f"downloaded_video_path: {downloaded_video_path}")
        return downloaded_video_path
    except:
        print("Failed to download video")

if __name__ == "__main__":
    params_dict = json_read(PARAMS_JSON_PATH)
    yt_video_url = params_dict['YT_VIDEO_URL']
    file_name = params_dict['FILE_NAME']

    download_video(yt_video_url, file_name, "SD")


    ##################################################################
    # Use the below method when not using gradio
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-v", "--video", required=True, help="URL to yt video")
    # ap.add_argument("-f", "--filename", required=False, help="Video save file name")
    # ap.add_argument("-l", "--language", default='English', help="Language for the summary text")
    # ap.add_argument("-n", "--word_limit", default=0, help="The number of words in the summary")
    # ap.add_argument("-b", "--as_bullets", default=False, help="Whether summarize as bullet points (T/F)")
    # args = vars(ap.parse_args())
    # yt_video_url = args["video"]
    # video_save_name = args["filename"]
    # lang = args["language"]
    # word_limit = args["word_limit"]
    # as_bullets = args["as_bullets"]
    #
    # file_name = video_save_name
    # if video_save_name.endswith('.mp4'):
    #     file_name = video_save_name.split('.')[0]
    #
    # params_dict = { # Use this when not using gradio app
    #     'YT_VIDEO_URL': yt_video_url,
    #     'FILE_NAME': file_name,
    #     'LANGUAGE': lang,
    #     'WORD_LIMIT': word_limit,
    #     'AS_BULLETS': as_bullets
    # }
    #
    # json_write(PARAMS_JSON_PATH, params_dict)
    #
    # download_video(yt_video_url, file_name, lang, word_limit, as_bullets)
    # Sample run:
    # p3 _1_download_yt_video.py -v https://www.youtube.com/watch?v=WsEQjeZoEng&t=7s -f no_jobs




