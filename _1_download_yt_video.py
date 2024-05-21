# import argparse
from pytube import YouTube as yt
from _utils import VIDEO_DIR, PARAMS_JSON_PATH, json_read, json_write

def download_video(yt_video_url, file_name):

    video = yt(yt_video_url).streams.filter(res="360p", progressive=True).first() # This downloads in 360p without audio
    # Moving ahead with 360p only as we only need to work with audio
    # video = yt(yt_video_url).streams.get_highest_resolution() # This downloads in 720p with audio
    # video = yt(yt_video_url).streams.filter(res="1080").first() # This downloads in 1080p without audio
    try:
        print('Download in progress')
        downloaded_video_path = f'{VIDEO_DIR}/{file_name}.mp4'
        video.download(VIDEO_DIR, filename=f'{file_name}.mp4')
        print("Video downloaded successfully")
        return downloaded_video_path
    except:
        print("Failed to download video")


# if __name__ == "__main__": # Commented out as using gradio app instead of running step wise | May need debugging
#     params_dict = json_read(PARAMS_JSON_PATH)
#     yt_video_url = params_dict['YT_VIDEO_URL']
#     file_name = params_dict['FILE_NAME']
#     lang = params_dict['LANGUAGE']
#     word_limit = params_dict['WORD_LIMIT']
#     as_bullets = eval(params_dict['AS_BULLETS'])
#
#     download_video(yt_video_url, file_name)


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
    # p3 _1_download_yt_video.py -v https://www.youtube.com/watch?v=safdaf -f name




