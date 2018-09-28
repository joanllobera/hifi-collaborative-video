import datetime
import os
from copy import copy
from operator import itemgetter

from core.exceptions.generic_exceptions import NotExistingResource
from core.helpers.validators import GenericValidator
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
        video_slice_info['inpoint'] = video_slice_info['inpoint'][-2:] + ".00"
        video_slice_info['outpoint'] = video_slice_info['outpoint'][-2:] + ".00"
        return video_slice_info

    @staticmethod
    def build_next_video_slice_information(video_id, initial_ts, end_ts):
        """

        :param video_info:
        :return:
        """
        if video_id is None or initial_ts is None or end_ts is None:
            raise ValueError("All parameters are mandatory.")
        video = Video.objects(id=video_id).first()
        if video is None:
            raise NotExistingResource("There's no video with such id.")
        video_slice_info = {}
        video_slice_info['file'] = "{}/dasher-output/video.mp4".format(video['video_path'])
        video_init = float(VideoEditorHelper.get_initial_ts(video_id=video_id))
        init_offset = float(initial_ts) - float(video_init)
        end_offset = float(end_ts) - float(video_init)
        video_slice_info['inpoint'] = str(datetime.timedelta(seconds=init_offset))
        video_slice_info['outpoint'] = str(datetime.timedelta(seconds=end_offset))
        return video_slice_info

    @staticmethod
    def create_videoslices_info(edit_info):
        """

        :param edit_info:
        :return:
        """
        video_slices = []
        videos = copy(edit_info)
        ordered_videos = sorted(videos, key=itemgetter('position'))
        prev_ts = -1
        for video in ordered_videos:
            ## if it's the first video, we don't have previous videos, so we just calculate
            ## the video slice.
            video_original_ts = VideoEditorHelper.get_initial_ts(video_id=video['id'])
            if prev_ts == -1:
                initial_ts = float(video_original_ts) + float(video['thumb'])
                end_ts = initial_ts + 1.0
                #end_ts = initial_ts + (float(video['end']) - float(video['init']))
                print("Video {}".format(video['id']))
                print("------------------------------")
                print("Info: {}".format(video))
                print("Original: \t{}".format(video_original_ts))
                print("Fixed: \t\t{}".format(initial_ts))
                print("End: \t\t{}".format(end_ts))
                prev_ts = end_ts
                video_slice = VideoEditorHelper.build_next_video_slice_information(video_id=video['id'],
                                                                            initial_ts=initial_ts,
                                                                            end_ts=end_ts)
                print("Video_slice_info:{}".format(video_slice))
            else:
                initial_ts = prev_ts
                end_ts = float(video_original_ts) + float(video['thumb']) + 1.0
                print("Video {}".format(video['id']))
                print("------------------------------")
                print("Info: {}".format(video))
                print("Original: \t{}".format(video_original_ts))
                print("Fixed: \t\t{}".format(initial_ts))
                print("End: \t\t{}".format(end_ts))
                video_slice = VideoEditorHelper.build_next_video_slice_information(video_id=video['id'],
                                                                            initial_ts=initial_ts,
                                                                            end_ts=end_ts)
                prev_ts = end_ts
            video_slices.append(video_slice)
        return video_slices, video['id']

    @staticmethod
    def save_edit_info_to_file(session_path, video_slices, edition_id):
        """

        :param session_path:
        :param video_slices:
        :return:
        """
        filename = "{}/edited-video-{}.txt".format(session_path, edition_id)
        f = open(filename, "w")
        for video_slice in video_slices:
            f.write("file {}\n".format(video_slice['file']))
            f.write("inpoint {}\n".format(video_slice['inpoint']))
            f.write("outpoint {}\n".format(video_slice['outpoint']))
        f.close()
        return filename

    @staticmethod
    def get_first_video_ts(edit_info):
        """

        :param edit_info:
        :return:
        """
        if edit_info is None or type(edit_info) != list:
            raise ValueError("Expected a list as parameter.")
        video_info = edit_info[0]
        ts = VideoEditorHelper.get_initial_ts(video_id=video_info['id'])
        updated_ts = float(ts) + float(video_info['thumb'])
        return str(updated_ts)

    @staticmethod
    def calculate_audio_init_offset(video_init_ts, audio_init_ts):
        """

        :param session_id:
        :return:
        """
        offset = float(video_init_ts) - float(audio_init_ts)
        offset = round(offset, 3)
        return str(offset)

    @staticmethod
    def calculate_audio_end_offset(edit_info, audio_init_offset, audio_init_ts):
        """

        :param session_id:
        :param edit_info:
        :return:
        """
        if edit_info is None or type(edit_info) != list:
            raise ValueError("Expected a list as parameter.")
        last_video = edit_info[-1]
        last_video_info = Video.objects(id=last_video['id']).first()
        if last_video_info is None:
            raise NotExistingResource("The last video of the edition does not exist.")
        video_initts = VideoEditorHelper.get_initial_ts(video_id=str(last_video_info['id']))
        end_ts = float(video_initts) + float(last_video['thumb']) + 1.0
        offset = float(end_ts) - float(audio_init_ts) - float(audio_init_offset)
        offset = round(offset, 3)
        return str(offset)

    @staticmethod
    def get_initial_ts(video_id):
        """

        :param video_id:
        :return:
        """
        GenericValidator.validate_id(video_id)
        video = Video.objects(id=video_id).first()
        if video is None:
            raise NotExistingResource("No video with such id.")
        video_path = video['video_path']
        ts_filename = "{}/ts.txt".format(video_path)
        file = open(ts_filename, "r")
        if not os.path.exists(ts_filename):
            raise NotExistingResource("Video is still being recorded or it failed.")
        ts = file.read().rstrip("\n")
        return ts
