#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


def action_wrapper(hermes, intentMessage, conf):
    if len(intentMessage.slots.call) > 0 and len(intentMessage.slots.person) > 0:
    person = intentMessage.slots.person.first().value # We extract the value from the slot "person"
    result_sentence = "Do you want to make a call to  : {}".format(str(person))  # The response that will be said out loud by the TTS engine.
    elif len(intentMessage.slots.call) > 0 and len(intentMessage.slots.number) > 0:
    number = intentMessage.slots.number.first().value # We extract the value from the slot "number"
    result_sentence = "Dialing the number : {}".format(str(number))  # The response that will be said out loud by the TTS engine.
    else:
    result_sentence = "I did not understand that! Could you please repeat?" 

current_session_id = intentMessage.session_id
hermes.publish_end_session(current_session_id, result_sentence)


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("Aniket_J:MakeCalls", subscribe_intent_callback) \
         .start()
