

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