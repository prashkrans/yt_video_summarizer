# Youtube Video Summarizer
Summarizes a youtube video provided yt video url and file name 

### Prerequisites:
- Python 3.10 (Might work with other versions as well)
- Nvidia drivers installed along with CUDA
- Nvidia GPU with VRAM atleast 6GB
- CPU can also be used but is painfully slow
- Developed in Ubuntu 24.04 so linux based on debian is preferred

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
`pip install -r requirements.text`
4. Add the line to ~/.bashrc and then source it.  
```commandline
nano ~/.bashrc
export GROQ_AI_API_KEY='gsk_xxxxxxxxxxxxxx'
source ~/.bashrc
```
Note: GROQ_AI_API_KEY could be replaced with dot_env or direct api key in line 9 of `_4_summarize.py`
4. Run the gradio app and `Ctrl+LeftClick` on the local host link to use the gradio app in your browser.    
`python3 main_gradio.py`

### Usage:
1. When the gradio app has started, provide the YT video url and file name.
2. Select a language in which the summary is required.
3. Select the work limit.
4. Select "Summarize as bullet points" if the summary is to be created as bullet points.
5. Click on "Summarize Video" and wait for processing to end.
6. Upon completion of processing two different summaries and the original transcription would be presented which could be download as well.
