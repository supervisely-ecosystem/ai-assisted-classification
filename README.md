<div align="center" markdown>
<img src="https://i.imgur.com/hh0VJ0S.png"/>

# AI assisted classification and tagging

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Run">How To Use</a>
</p>


[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervise.ly/apps/supervisely-ecosystem/nn-image-labeling/annotation-tool)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/ai-assisted-classification)
[![views](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/ai-assisted-classification&counter=views&label=views)](https://supervise.ly)
[![used by teams](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/ai-assisted-classification&counter=downloads&label=used%20by%20teams)](https://supervise.ly)
[![runs](https://app.supervise.ly/public/api/v3/ecosystem.counters?repo=supervisely-ecosystem/ai-assisted-classification&counter=runs&label=runs&123)](https://supervise.ly)

</div>

# Overview

Classification model can be integrated into labeling interface and significantly speed up manual images and objects tagging:
1. Model predicts most probable tags
2. Labeler visually compare predictions with target image/object and assign the correct tag
3. Also app allows to review already assigned tags

This approach significantly outperforms manual labeling especially when annotator has to select one of hundred or even 
thousand of tags. For example, in retail there are huge catalogs, and it is time-consuming and almost impossible to tag 
objects on shelves without special tool.

Watch demo: 

<a data-key="sly-embeded-video-link" href="https://youtu.be/eWAvbmkm6JQ" data-video-code="eWAvbmkm6JQ">
    <img src="https://i.imgur.com/ODlVoBh.png" alt="SLY_EMBEDED_VIDEO_LINK"  style="max-width:100%;">
</a>

# How To Run
1. Add app from Ecosystem to your team if it is not there
2. Deploy classification model
3. Run app from labeling interface

# How To Use

0. Connect to deployed classification model
1. Be sure that NN you are going to use is deployed in your team
2. To start using app, user has to run it (from Team Apps page or directly in labeling UI) or open already running session. App doesn't support multiuser mode: it means that every user has to run its own session, BUT multiple sessions can connect to a single NN. 
   
    For example: There are 5 labelers in your team and you would like to use YOLOv5. In that case you should have at least one session of the deployed NN and run separate sessions for every user.





