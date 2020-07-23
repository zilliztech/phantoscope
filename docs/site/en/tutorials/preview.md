
Phantoscope Preview is a GUI interface designed for Phantoscope users to verify the search results of their applications.

## Installation
```bash
$ export LOCAL_ADDRESS=$(ip a | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'| head -n 1)
$ docker run -d -e API_URL=$LOCAL_ADDRESS:5000 -p 8000:80 phantoscope/preview:0.2.0
```

## Search with Phantoscope Preview

Open http://127.0.0.1:8000 with a Web browser to view the interface of Phantoscope Preview. 


![](https://live.staticflickr.com/65535/50140138947_2801b030df_o.gif)



## Phantoscope Preview 
![](../../../../.github/phantoscope-preview.png)

1. Click the lens image on the top left to choose a local image for an image search. 
2. You can pull an image to the left area for an image search. 
3. You can crop up the image to search with part of the image. 
4. Click **application** to switch between applications.

> Note: You need to use a RESTful API to create an application. 
