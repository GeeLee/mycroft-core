# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from mycroft.tts import TTSValidator
from mycroft.tts.remote_tts import RemoteTTS
from mycroft.configuration import Configuration
from mycroft.util.log import LOG
from mycroft.util import play_wav
from urllib import parse
import requests

class Mimic2(RemoteTTS):
    PARAMS = {'accept': 'audio/wav'}

    def __init__(self, lang, config):
        super(Mimic2, self).__init__(
            lang, config, config['url'],
            config['api_path'], Mimic2Validator(self)
        )
        LOG.info("mimic2config: " + str(config))

    def _save(self, data):
        with open(self.filename, 'wb') as f:
            f.write(data)
    
    def _play(self, req):
        if req.status_code == 200:
            self._save(req.content)
            play_wav(self.filename).communicate()
        else:
            LOG.error(
                '%s Http Error: %s for url: %s' %
                (req.status_code, req.reason, req.url))

    def build_request_params(self, sentence):
        params = self.PARAMS.copy()
        params['text'] = sentence.encode('utf-8')
        return params

    def execute(self, sentence, ident=None):
        try:
            req_route = \
                self.url + self.api_path + parse.quote(sentence)
            LOG.info(req_route)
            req = requests.get(req_route)
            self.begin_audio()
            self._play(req)
        except Exception as e:
            LOG.error(e.message)
        finally:
            self.end_audio()
        

class Mimic2Validator(TTSValidator):
    def __init__(self, tts):
        super(Mimic2Validator, self).__init__(tts)

    def validate_lang(self):
        # TODO
        pass

    def validate_connection(self):
        # TODO
        pass

    def get_tts_class(self):
        return Mimic2