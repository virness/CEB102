from pytube import YouTube                                          
#安裝最新版本pytube後輸入網址即可下載。  
yt=YouTube("https://www.youtube.com/watch?v=g9fnNQgOP40&t=1673s")  
yt.streams.first().download()  
