# MixItUp

MixItUp is a website that offers a unique music mashup experience to its users. By searching for an artist, users can create a continuous mix of their songs, with each track fetched from YouTube. The website allows users to specify various parameters, such as the number of songs, duration of each song, and their email ID.

The website's methodology involves downloading the artist's videos, converting them to audio, trimming the audio clips to the desired duration, and mixing them together to create a seamless mashup. This process ensures that the resulting mashup is of high quality.

A mail is sent to the user containing the Zip file of Mashup.

The Website uses the following packages:
- pytube
- moviepy
- ffmpeg
- youtube-search
