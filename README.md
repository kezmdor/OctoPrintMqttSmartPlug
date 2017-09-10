# OctoPrintMqttSmartPlug

This plugin enables one to control a smart plug from within OctoPrint using MQTT messages.

## Disclaimer

This plugin is inspired by the plugins 'OctoPrint-TPLinkSmartplug' and 'PSU Control'.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/kezmdor/OctoPrintMqttSmartPlug/archive/master.zip

Please make sure you have also installed and configured the plugin 'MQTT'.

## Configuration

The broker setup is done within the configuration of the plugin 'MQTT'.

Afterwards please configure the control topic and the state topic of your smart plug.
Example:
* cmnd/plug/POWER
* stat/plug/POWER

You can also configure the messages sent and expected on these MQTT topics.