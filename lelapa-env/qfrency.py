# -*- coding: utf-8 -*-
################################################################################
# Copyright (c) 2020-2024, CSIR, South Africa.                                 #
#                                                                              #
# This is proprietary software and is protected under copyright laws.          #
# You recognize that the Software, and all data and materials contain          #
# confidential and proprietary trade secrets that are owned by the CSIR        #
# ("Confidential Information"). You agree not to disclose, or permit any       #
# third party or entity access to such Confidential Information without        #
# prior written permission of the CSIR. Without limiting the foregoing,        #
# you agree to protect the Confidential Information with commercially          #
# reasonable procedures that are no less restrictive than the strictest        #
# procedures you use to protect your own confidential information.             #
#                                                                              #
################################################################################
import requests
import base64


URL="https://tts.qfrency.com/api"
VERSION="v1"
X_API_KEY="X-API-KEY"
X_ACCOUNT_ID="X-ACCOUNT-ID"


class QfrencyCloudTTS(object):
    def __init__(self, AccountID, API_Key):
        """
        Create a new Qfrency cloud TTS object which can be used to
        interact with the Qfrency TTS Cloud API.

        Parameters
        ----------
        AccountID : str
            Your account identifier UUID string.
        API_Key : str
            Your API_Key for this session.
        """
        self._AccountID = AccountID
        self._API_Key = API_Key
        self._url = "{}/{}".format(URL, VERSION)
        self._voices_url = "{}/voices".format(self._url)
        self._synth_url = "{}/synthesize".format(self._url)
        self._voices = self._get_voices()

    def _get_voices(self):
        headers = {X_API_KEY: self._API_Key}
        request_object = requests.get(self._voices_url,
                                      headers=headers)
        print("request_object = {}".format(request_object.url))
        if not request_object.ok:
            return []
        try:
            rv = request_object.json()
            if "voices" not in rv:
                return []
            return rv["voices"]
        except Exception as e:
            return []

    @property
    def voices(self):
        """
        Get a list of available voices for synthesis.
        """
        return self._voices

    def synth(self, voice_code, text, args=None):
        """
        Synthesize the given text with the given voice name and
        return the wav bytestream.

        Parameters
        ----------
        voice_code : str
            The voice-code of the voice to be used for synthesis.
        text : str
            The text for to be synthesize.
        args : dict
            A dictionary of extra (optional) arguments to pass to the
            cloud based service.
        """
        params = {"voice-code": voice_code, "text": text}
        if args:
            params.update(args)
        headers = {X_API_KEY: self._API_Key}
        request_object = requests.post(self._synth_url,
                                       headers=headers,
                                       json=params)
        rv = request_object.json()
        if request_object.ok:
            return base64.decodebytes(rv["wav_64"].encode('utf8'))
        else:

            raise RuntimeError("({}) {}".format(rv["error"]["code"],
                                                rv["error"]["message"]))
