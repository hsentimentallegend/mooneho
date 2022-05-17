import streamlit as st
st.title('MoonEcho APP')
st.write('talk with you friend with delayed your voice')
st.image('moonecho.jpg')
import asyncio
import logging
from pathlib import Path
from typing import List
import av
from streamlit_webrtc import (
    AudioProcessorBase,
    RTCConfiguration,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)
HERE = Path(__file__).parent
logger = logging.getLogger(__name__)

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


DEFAULT_DELAY = 0.08

class VideoProcessor(VideoProcessorBase):
    delay = DEFAULT_DELAY
    async def recv_queued(self, frames: List[av.VideoFrame]) -> List[av.VideoFrame]:
        logger.debug("Delay:", self.delay)
        await asyncio.sleep(self.delay)
        return av.VideoFrame.from_ndarray(frames, format="bgr24")

class AudioProcessor(AudioProcessorBase):
    delay = DEFAULT_DELAY

    async def recv_queued(self, frames: List[av.AudioFrame]) -> List[av.AudioFrame]:
        await asyncio.sleep(self.delay)
        return frames

webrtc_ctx = webrtc_streamer(
        key="delay",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=VideoProcessor,
        audio_processor_factory=AudioProcessor,
        async_processing=True,
    )

with st.sidebar:
  st.write("Moon Echo concept")

#streamlit webrtcのデモを参考にさせて頂いております。

