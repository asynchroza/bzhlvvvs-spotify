# bzhlvvvs-spotify 

Yo, nice to see you there! 👋  
This is the github repo containing the source code of the random Spotify song picker you're probably coming from. 🔥

If you're interested in creating your own lambda using this one as a template, don't hesitate to reach out to me with any questions you may have.   
I'll be happy to help! 🤓

Anyway, I'm off to work now! 🌴🔨🥥

[Lambda URL](https://bzhlvvvs.com)  
[Playlist URL](https://open.spotify.com/playlist/4qw4F3Mi3eGjXwLeKM5pYx?si=e26637db63a94ca0)

# Documentation:

## Environment Variables:

Before running or deploying the lambda, you need to create a copy of the sample env file called `.env.spotify` and place it 
in the `src` directory:
```shell
cp src/.env.sample src/.env.spotify
```

* `CLIENT_ID` and `CLIENT_SECRET` are the corresponding client id and client secret of your spotify app. The lambda 
is using [client credentials flow](https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow) for authorizing towards Spotify's API. (**REQUIRED**)

* `TITLE` is the title you want the generated static page to have. (**REQUIRED**)  

![image](https://github.com/asynchroza/bzhlvvvs-spotify/assets/104720011/bc3f9c5d-b5b3-4208-b054-9b3e83032a28)

* `FAVICON_URL` is the url pointing to the location of your favicon. If left empty, your page won't have a favicon. 
```bash
FAVICON_URL="https://personal-misho.s3.eu-north-1.amazonaws.com/favicon.ico"  # I am using an S3 bucket to host my favicon
```

* `PLAYLIST_ID` is the id of the playlist you want to fetch songs from. (**REQUIRED**)  
To obtain the ID of your playlist, you can click on the three dots icon located next to your playlist. Then, copy the URL of the playlist:

![image](https://github.com/asynchroza/bzhlvvvs-spotify/assets/104720011/f35009c3-d461-4532-bad7-75bd9d2ca8e7)
![image](https://github.com/asynchroza/bzhlvvvs-spotify/assets/104720011/4430d79e-60e1-468c-8ca4-c494b08057d0)

* `LINKEDIN` and `GITHUB` are links to your socials. If left empty, icons won't be rendered when page is shipped.
```bash
LINKEDIN="https://www.linkedin.com/me/mbozhilov/"
GITHUB="https://github.com/asynchroza/bzhlvvvs-spotify"
```
