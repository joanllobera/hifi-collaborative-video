import datetime
import uuid
from copy import copy

from core.exceptions.generic_exceptions import NotExistingResource
from core.model.video import Video


class VideoEditorHelper(object):

    @staticmethod
    def build_next_video_slice_info(video_info):
        """

        :return:
        """
        if video_info is None or type(video_info) != dict:
            raise ValueError("Expected a dictionary as parameter.")
        video = Video.objects(id=video_info['id']).first()
        if video is None:
            raise NotExistingResource("There's no video with such id.")
        video_slice_info = {}
        video_slice_info['file'] = "{}/dasher-output/video.mp4".format(video['video_path'])
        video_slice_info['inpoint'] = str(datetime.timedelta(seconds=video_info['init'])).replace(
            ":", ".")
        video_slice_info['outpoint'] = str(datetime.timedelta(seconds=video_info['end'])).replace(
            ":", ".")
        return video_slice_info

    @staticmethod
    def create_videoslices_info(edit_info):
        """

        :param edit_info:
        :return:
        """
        video_slices = []
        videos = copy(edit_info['videos_slices'])
        for video in videos:
            video_slice = VideoEditorHelper.build_next_video_slice_info(video_info=video)
            video_slices.append(video_slice)
        return video_slices

    @staticmethod
    def save_edit_info_to_file(session_path, video_slices):
        """

        :param session_path:
        :param video_slices:
        :return:
        """
        filename = "{}/edited-video-{}.txt".format(session_path, uuid.uuid4().hex)
        f = open(filename, "w")
        for video_slice in video_slices:
            f.write("file {}\n".format(video_slice['file']))
            f.write("inpoint {}\n".format(video_slice['inpoint']))
            f.write("outpoint {}\n".format(video_slice['outpoint']))
        f.close()
        return filename
