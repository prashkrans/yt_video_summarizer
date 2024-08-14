# Youtube Video Summarizer
- Summarizes a youtube video provided yt video url and file name.
- Customization options such as word limit, video resolution, bullet points are available.
- Also, provides an option to download the yt video or its audio track.

### Demo Video:
https://github.com/user-attachments/assets/d078759b-6ab4-4b1f-9323-3b9c7dc4b136

### Prerequisites:
- Python 3.10 (Might work with higher versions as well)
- Nvidia drivers installed along with CUDA for whisper
- Nvidia GPU with VRAM atleast 6GB (medium) or 10GB (large-v2)
- CPU can also be used but is awfully slow

### Setup:
1. Clone the repo and move to the root dir.
```commandline
git clone https://github.com/prashkrans/yt_video_summarizer.git
cd yt_video_summarizer/
```
2. Create a python virtual environment.
```commandline
python3 -m venv env_vid_sum
source env_vid_sum/bin/activate
```
3. Install the requirements (Might take some time).   
```
pip install -r requirements.text
```
4. Add the GROQ_API_KEY line to ~/.bashrc and then source it.  
```commandline
nano ~/.bashrc
export GROQ_API_KEY='gsk_xxxxxxxxxxxxxx'
source ~/.bashrc
```
Note: GROQ_API_KEY could be replaced with dot_env or direct api key in line 9 of `_4_summarize.py`
4. Run the gradio app and `Ctrl+LeftClick` on the local host link to use the gradio app in your browser.    
`python3 main_gradio.py`

### Usage:
1. When the gradio app has started, provide the YT video url and file name.
2. Select a language in which the summary is required.
3. Select the word limit.
4. Select "Summarize as bullet points" if the summary is to be created as bullet points.
5. Select the video resolution i.e. SD, HD or FHD
5. Click on "Summarize Video" and wait for processing to end.
6. Upon completion, two different summaries and the original transcription would be presented with the option to download them.

### Note:
- It uses **Whisper medium/large-v2** to generate transcription.
- It uses **mixtral and llama3.1_70b** (hosted on Groq) LLMs to summarize the transcription generated.

### License
This gradio app and Whisper's code and model weights are released under the MIT License. See [LICENSE](LICENSE) for further details.
