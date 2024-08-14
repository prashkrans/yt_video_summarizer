import gradio as gr

from _1_download_yt_video import download_video
from _2_extract_audio_from_yt_video import extract_audio
from _3_transcribe import transcribe
from _4_summarize import summarize
from _utils import PARAMS_JSON_PATH, json_write

js = """
function createGradioAnimation() {
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '2em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'center';
    container.style.marginBottom = '20px';

    var text = 'YouTube Video Summarizer: Summarize youtube videos within given word limit and other custom options';
    for (var i = 0; i < text.length; i++) {
        (function(i){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.5s';
                letter.innerText = text[i];

                container.appendChild(letter);

                setTimeout(function() {
                    letter.style.opacity = '1';
                }, 100);
            }, i * 100);
        })(i);
    }

    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(container, gradioContainer.firstChild);

    return 'Animation created';
}
"""

def summarize_yt_video_gr(
    yt_video_url,
    file_name,
    to_eng,
    word_limit,
    as_bullets,
    video_resolution
):
    if (yt_video_url == '' or file_name == ''):
        raise gr.Error("Please enter a valid YouTube video URL and file name to continue")

    # Create dictionary
    params_dict = {
        'YT_VIDEO_URL': f'{yt_video_url}',
        'FILE_NAME': f'{file_name}',
        'TRANSLATE_TO_ENGLISH': f'{to_eng}',
        # 'LANGUAGE': f'{lang}',
        'WORD_LIMIT': f'{word_limit}',
        'AS_BULLETS': f'{as_bullets}',
        'VIDEO_RESOLUTION': f'{video_resolution}'
    }

    print(f'params_dict: {params_dict}')

    # We are saving params.json only for testing in a modular manner, the main gradio app doesn't need it
    json_write(PARAMS_JSON_PATH, params_dict)

    downloaded_video_path = download_video(yt_video_url, file_name, video_resolution)
    audio_file_path = extract_audio(file_name)
    transcription = transcribe(file_name, to_eng)

    (
        word_count,
        word_limit,
        summarized_text_1,
        summarized_text_2,
        summarized_text_path_1,
        summarized_text_path_2,
        transcribed_text_path
     ) = summarize(file_name, word_limit, as_bullets)

    proc_message = (f'Processing completed! The transcription has a word count of {word_count} which has been '
                          f'summarized within the word limit of {word_limit}. Please download the summarized text files '
                          f'as well as the original transcription (if required).')

    return (
        gr.Video(value=downloaded_video_path),
        gr.Audio(value=audio_file_path),
        gr.Textbox(value=proc_message, visible=True),
        gr.Textbox(value=summarized_text_1, visible=True),
        gr.Textbox(value=summarized_text_2, visible=True),
        gr.Textbox(value=transcription, visible=True),
        gr.DownloadButton(value=summarized_text_path_1, visible=True, interactive=True),
        gr.DownloadButton(value=summarized_text_path_2, visible=True, interactive=True),
        gr.DownloadButton(value=transcribed_text_path, visible=True, interactive=True)
    )


with gr.Blocks(
        title='Video Summarizer',
        # theme=gr.themes.Monochrome(), # Monochrome theme is good but js doesn't work with gr.themes.Monochrome()
        theme=gr.themes.Base(),
        # theme='gstaff/sketch',
        js=js,
        # head=head,
        analytics_enabled=False,
        # fill_height=True
) as yt_summarizer:
    with gr.Row():
        with gr.Column(scale=1):
            yt_video_url = gr.Textbox(label="Provide YT Video URL", info="Ideally source audio should be in English")
            file_name = gr.Textbox(label="Provide File Name")
            # lang = gr.Radio(
            #         label="Select Summary language",
            #         choices=['English', 'Hindi', 'Spanish', 'French'],
            #         # Verified that both mixtral and llama3 works well with the above five languages
            #         value='English'
            # )
            to_eng = gr.Checkbox(
                info="Should the summary be in English?",
                label="Translate to English",
                value=True
            )
            word_limit = gr.Slider(
                    50,
                    1000,
                    value=200,
                    step=50,
                    label="Select Word Limit",
                    info="Choose between 50 and 1000 | Ideally should be between 20% to 50% of the size of the \
                    original transcription"
            )
            as_bullets = gr.Checkbox(
                    info="Should the summary be in bullet points?",
                    label='Summarize as bullet points',
                    value=False
            )
            video_resolution = gr.Radio(
                label='Select video resolution',
                choices=['SD', 'HD', 'FHD'],
                value='HD'
            )
            button = gr.Button("Summarize video", variant="primary", interactive=True, scale=1)
            proc_message = gr.Textbox(label="Processing Status", visible=False)
        with gr.Column(scale=1):
            video_preview = gr.Video(label="YT Video Preview", height=480)
            audio_preview = gr.Audio(label="YT Audio Preview")

    with gr.Row():
        with gr.Column(variant='panel'):
            summarized_text_1 = gr.Textbox(label="Summary Version 1", lines=5, visible=False)
            download_button_1 = gr.DownloadButton(label="Download Summary Version 1", variant="primary", visible=False)
        with gr.Column(variant='panel'):
            summarized_text_2 = gr.Textbox(label="Summary Version 2", lines=5, visible=False)
            download_button_2 = gr.DownloadButton(label="Download Summary Version 2", variant="primary", visible=False)

    with gr.Row():
        with gr.Column(variant='panel'):
            original_text = gr.Textbox(label='Transcription', lines=7, visible=False)
            download_button_3 = gr.DownloadButton(label="Download Transcription", variant="primary", visible=False)

    button.click(
        fn=summarize_yt_video_gr,
        inputs=[
            yt_video_url,
            file_name,
            to_eng,
            word_limit,
            as_bullets,
            video_resolution
        ],
        outputs=[
            video_preview,
            audio_preview,
            proc_message,
            summarized_text_1,
            summarized_text_2,
            original_text,
            download_button_1,
            download_button_2,
            download_button_3
        ]
    )

yt_summarizer.queue(
    api_open=False,
    default_concurrency_limit=1
).launch(server_port=7862)  # Local launch
