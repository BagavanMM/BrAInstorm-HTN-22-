#BrAInstorm - Visualizing the art of the emotion 
## Inspiration
Globally, one in ten people do not know how to interpret their feelings. There's a huge global shift towards sadness and depression. At the same time, AI models like Dall-E and Stable Diffusion are creating beautiful works of art, completely automatically. Our team saw the opportunity to leverage AI image models and the emerging industry of Brain Computer Interfaces (BCIs) to create works of art from brainwaves: enabling people to learn more about themselves and 

## What it does
A user puts on a Brain Computer Interface (BCI) and logs in to the app. As they work in front of front of their computer or go throughout their day, the user's brainwaves are measured. These differing brainwaves are interpreted as indicative of different moods, for which key words are then fed into the Stable Diffusion model. The model produces several pieces, which are sent back to the user through the web platform.

## How we built it
We created this project using Python for the backend, and Flask, HTML, and CSS for the frontend. We made use of a BCI library available to us to process and interpret brainwaves, as well as Google OAuth for sign-ins. We made use of an OpenBCI Ganglion interface provided by one of our group members to measure brainwaves.

## Challenges we ran into
We faced a series of challenges throughout the Hackathon, which is perhaps the essential route of all Hackathons. Initially, we had struggles setting up the electrodes on the BCI to ensure that they were receptive enough, as well as working our way around the Twitter API. Later, we had trouble integrating our Python backend with the React frontend, so we decided to move to a Flask frontend. It was our team's first ever hackathon and first in-person hackathon, so we definitely had our struggles with time management and aligning on priorities. 

## Accomplishments that we're proud of
We're proud to have built a functioning product, especially with our limited experience programming and operating under a time constraint. We're especially happy that we had the opportunity to use hardware in our hack, as it provides a unique aspect to our solution. 

## What we learned
Our team had our first experience with a 'real' hackathon, working under a time constraint to come up with a functioning solution, which is a valuable lesson in and of itself. We learned the importance of time management throughout the hackathon, as well as the importance of a storyboard and a plan of action going into the event. We gained exposure to various new technologies and APIs, including React, Flask, Twitter API and OAuth2.0.

## What's next for BrAInstorm
We don't currently have any plans to take the project further, but who knows what could happen :)
