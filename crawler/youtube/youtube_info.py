import pafy


def get_video_by_url(url, is_playlist=False, index=0):
    if is_playlist:
        playlist = pafy.get_playlist(url)['items']
        if not(len(playlist) > index and index >= 0):
            index = 0
        video = playlist[index]['pafy']
    else:
        video = pafy.new(url)

    return video


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=bMt47wvK6u0"
    video = get_video_by_url(url)
    print(video)
    print(video.getbest().url)
