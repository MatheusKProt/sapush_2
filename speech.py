import uuid
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class RequestError(Exception):
    pass


class UnknownValueError(Exception):
    pass


def recognize_bing(audio, key, language="en-US"):
    credential_url = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"
    credential_request = Request(credential_url, data=b"", headers={
        "Content-type": "application/x-www-form-urlencoded",
        "Content-Length": "0",
        "Ocp-Apim-Subscription-Key": key,
    })

    try:
        credential_response = urlopen(credential_request, timeout=60)  # credential response can take longer, use longer timeout instead of default one
    except HTTPError as e:
        raise RequestError("credential request failed: {}".format(e.reason))
    except URLError as e:
        raise RequestError("credential connection failed: {}".format(e.reason))
    access_token = credential_response.read().decode("utf-8")
    url = "https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1?{}".format(urlencode({
        "language": language,
        "locale": language,
        "requestid": uuid.uuid4(),
    }))

    request = Request(url, data=stream_audio_file(audio), headers={
        "Authorization": "Bearer {}".format(access_token),
        "Content-type": "audio/ogg; codec=\"audio/pcm\"; samplerate=16000",
        "Transfer-Encoding": "chunked",
    })

    try:
        response = urlopen(request)
    except HTTPError as e:
        raise RequestError("recognition request failed: {}".format(e.reason))
    except URLError as e:
        raise RequestError("recognition connection failed: {}".format(e.reason))
    response_text = response.read().decode("utf-8")

    result = json.loads(response_text)
    if "RecognitionStatus" not in result or result["RecognitionStatus"] != "Success" or "DisplayText" not in result:
        raise UnknownValueError()
    return result["DisplayText"]


def stream_audio_file(speech_file):
    # Chunk audio file
    with open(speech_file, 'rb') as f:
        while 1:
            data = f.read(1024)
            if not data:
                break
            yield data
