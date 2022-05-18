import streamlit as st
st.title('MoonEcho APP')
st.write('''Let's talk with your friend with delayed your voice''')
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



DEFAULT_DELAY = 0.04

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
st.write('''[How to Use]''')
st.write('''Attach the headphones to your smartphone and press the START button below to stream video and audio.
You will hear a delay in the audio, so try talking to someone near you in that state.
If you are alone, read aloud from a book set up at the venue.
Listen carefully to how the tone of your voice sounds.
It is the same voice your friend is hearing.''')

webrtc_ctx = webrtc_streamer(
        key="delay",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=VideoProcessor,
        audio_processor_factory=AudioProcessor,
        async_processing=True,
    )
if webrtc_ctx.video_processor and webrtc_ctx.audio_processor:
     delay = st.slider("Delay time", 0.0, 2.0, DEFAULT_DELAY, 0.01)
     webrtc_ctx.video_processor.delay = delay
     webrtc_ctx.audio_processor.delay = delay

st.title('Moon Echo Concept')
st.write('''This piece focuses on the nature of "communication" in today's society.
The audience is invited to participate in this work by using their own voices.
By having a time lag in the audio, this work allows the audience to listen to their own words at different times, and thus objectively hear how they usually communicate with their own voice.
On this occasion, I use a device to separate the sound from the body for my artwork. This device allows a period of delay for the sound.

Through interaction, audiences are expected to recognize these following experiences:
-What kind of sound you are producing?
-What does your voice sound like to yourself?
-What does your voice sound like to other people?
-How does your voice reach the person you communicate with?
-How do your words feel like to other people?

Communication provide the basis for successful Diplomatic negotiations, trade and commerce. Therefore, it is essential to be able to recognize different perspectives and interest of the other person.
For example,
-Is it a self-directed action?
-What does the other person feel/think about your action? Etc.
I think, if a lot of people realize it, people will have a more in-depth communication with each other.

In the virtual space on the internet and in a technology-advanced society, it has been possible to live without communicating with other people. However, in the real world and in actual situation it is not possible to live without communicating with other people, and there are a lot of people in the world who cannot communicate well with other people, which has gradually became a problem.
Furthermore, with the spread of the metaverse in the future, it is expected that people will be required to have the same smooth communication skills as in reality, even in virtual spaces.

In the real world, the pandemic that has been going on since 2020 has dramatically increased the percentage of online communication. Unlike traditional means of communication, several elements in communication have been cut out, creating unique difficulties and problems.
Especially hate comments on the internet, which have become increasingly aggressive in recent years, have created a variety of problems.
The cause is a lack of imagination.
If they can imagine the feelings of the person who received that statement, I believe that the world can gradually change.
Through this work, I believe that the audience will have an opportunity to imagine what kind of impression they are unknowingly giving to others by actually hearing their own words with a time difference.''')




with st.sidebar:
  st.title("About Moon Echo")
  st.image('moonechoP_001.jpg')
  st.write('This app is for experiencing Moon Echo, an interactive sound artwork by Japanese artist Hiroshi Mehata presented at Kameyama Triennale 2017 and Makassar Biennale 2019, via smartphone.')
  st.image('moonechoP_002.jpg')
  st.sidebar.write('The article is in here')
  link = '[Makassar Biennale](https://makassarbiennale.org/suara-yang-terlepas-dari-tubuh/)'
  st.sidebar.markdown(link, unsafe_allow_html=True)
  link = '[Hiroshi Mehata Web site](https://www.mehatasentimentallegend.com/)'
  st.sidebar.markdown(link, unsafe_allow_html=True)

  st.write('''*The streaming program code for this application is based on streamlit-webrtc-example.''')




