from math import floor


class DataTransformer(object):

    @staticmethod
    def generate_video_list_view(session, db_videos):
        """

        :param db_videos:
        :return:
        """
        if db_videos is None:
            return ValueError("Expected a QuerySet for the db_videos parameter.")
        if session is None:
            return ValueError("Expected a RumbaSession object for the session parameter.")
        view_videos = []
        for video in db_videos:
            session_video = {'session_id': session['id'],
                             'band': session['band'],
                             'video_name': video['name'],
                             'video_id': str(video['id'],)
                             }
            view_videos.append(session_video)
        return view_videos

    @staticmethod
    def transform_seconds_to_ffmpeg_offset(seconds):
        if seconds is None or type(seconds) != float:
            raise ValueError("Expected a float.")

        mseconds = str(seconds).split(".")[1]
        int_seconds = int(seconds)
        remain = int_seconds
        # we calculate the hours, minutes and the seconds
        hours = floor(remain/3600)
        remain = remain - (hours*3600)
        minutes = floor(remain/60)
        seconds = remain - (minutes*60)
        # let's format the result according to ffmpeg expected value
        if hours < 10:
            str_hours = "0{}".format(hours)
        else:
            str_hours = str(hours)
        if seconds < 10:
            str_seconds = "0{}".format(seconds)
        else:
            str_seconds = "{}".format(seconds)
        if minutes < 10:
            str_minutes = "0{}".format(minutes)
        else:
            str_minutes = "{}".format(minutes)
        if len(mseconds) < 2:
            str_ms = "00{}".format(mseconds)
        elif len(mseconds) < 3:
            str_ms = "0{}".format(mseconds)
        else:
            str_ms = "{}".format(mseconds)
        init_ts = "{}:{}:{}.{}".format(str_hours, str_minutes, str_seconds, str_ms)
        return init_ts
