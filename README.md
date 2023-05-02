# fukkatsu 復活 

## Description

This is a proof of concept for a library that will leverage LLMs to dynamically fix and improve code during execution. Fukkatsu is the japanese word, `復活`, for "resurrection" or "revival". Metaphorically speaking, this library will attempt to fix your cars tire while you are driving it at 300 km/h. 

Insane? Yes. Possible? Maybe. Fun? Definitely.


Here is a representation of what we are trying to do: https://giphy.com/gifs/tire-kNRqJCLOe6ri8/fullscreen 


## MVP

You can find a MVP within the `poc` folder. You can simpy run the code via `python mvp.py`. The code will simulate a failing function, which will be repaird during execution. The mvp.py code will not request a correction to an OpenAi LLM but simply ueses a mock corrected function.