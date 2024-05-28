import base64

class DecoderManager:
    def __init__(self):
        self.decoders = {}

    def add_decoder(self, topic, decoder_function):
        self.decoders[topic] = base64.b64encode(decoder_function.encode('utf-8'))

    def remove_decoder(self, topic):
        if topic in self.decoders:
            del self.decoders[topic]

    def decode(self, topic, payload):
        if topic in self.decoders:
            decoder_function = base64.b64decode(self.decoders[topic]).decode('utf-8')
            exec(decoder_function)
            return locals()['decode'](payload)
        return payload