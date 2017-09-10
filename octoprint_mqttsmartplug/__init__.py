# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from octoprint.server import user_permission

class MqttsmartplugPlugin(octoprint.plugin.StartupPlugin,
                          octoprint.plugin.SettingsPlugin,
                          octoprint.plugin.TemplatePlugin,
						  octoprint.plugin.SimpleApiPlugin,
						  octoprint.plugin.AssetPlugin):

	def get_update_information(self):
		return dict(
			mqttsmartplug=dict(
				displayName="Mqttsmartplug Plugin",
				displayVersion=self._plugin_version,

				type="github_release",
				user="kezmdor",
				repo="OctoPrintMqttSmartPlug",
				current=self._plugin_version,

				pip="https://github.com/kezmdor/OctoPrintMqttSmartPlug/archive/{target_version}.zip"
			)
		)

	def __init__(self):
		self.mqtt_publish = lambda *args, **kwargs: None
		self.mqtt_subscribe = lambda *args, **kwargs: None
		self.mqtt_unsubscribe = lambda *args, **kwargs: None

	def on_after_startup(self):
		helpers = self._plugin_manager.get_helpers("mqtt", "mqtt_publish", "mqtt_subscribe", "mqtt_unsubscribe")
		if helpers:
			if "mqtt_publish" in helpers:
				self.mqtt_publish = helpers["mqtt_publish"]
			if "mqtt_subscribe" in helpers:
				self.mqtt_subscribe = helpers["mqtt_subscribe"]
			if "mqtt_unsubscribe" in helpers:
				self.mqtt_unsubscribe = helpers["mqtt_unsubscribe"]

		self.mqtt_subscribe(self._settings.get(["subscription"]), self._on_mqtt_subscription)
		self._logger.debug("Subscribed to %s" % self._settings.get(["subscription"]))

	def on_settings_save(self,data):
		octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
		self._logger.debug("Settings changed, will unsubscribe and subscribe again.")
		self.mqtt_unsubscribe(self._on_mqtt_subscription)
		self.mqtt_subscribe(self._settings.get(["subscription"]), self._on_mqtt_subscription)
		self._logger.debug("Subscribed to %s" % self._settings.get(["subscription"]))
	
	def _on_mqtt_subscription(self, topic, message, retained=None, qos=None, *args, **kwargs):
		self._logger.debug("Received a message for {topic}: {message}".format(**locals()))
		if message == self._settings.get(["msgon"]):
			self._plugin_manager.send_plugin_message(self._identifier, dict(currentState="on"))
			self._logger.debug("Current state of the plug is ON.")
		elif message == self._settings.get(["msgoff"]):
			self._plugin_manager.send_plugin_message(self._identifier, dict(currentState="off"))
			self._logger.debug("Current state of the plug is OFF.")
		else:
			self._plugin_manager.send_plugin_message(self._identifier, dict(currentState="unknown"))
			self._logger.debug("Don't know what this message should mean: {message}".format(**locals()))	

	def get_settings_defaults(self):
		return dict(
			publish = 'cmnd/plug/POWER',
			subscription = 'stat/plug/POWER',
			msgon = 'ON', 
			msgoff = 'OFF'
		)

	def get_template_vars(self):
		return dict(
			publish = self._settings.get(["publish"]),
			subscription = self._settings.get(["subscription"]),
			msgon = self._settings.get(["msgon"]), 
			msgoff = self._settings.get(["msgoff"])
		)

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]

	def get_assets(self):
		return dict(
			js=["js/mqttsmartplug.js"]
		)

	def get_api_commands(self):
		return dict(
			getState=[],
			turnOn=[],
			turnOff=[]
		)

	def on_api_command(self, command, data):
#		if not user_permission.can():
#			return make_response("Insufficient rights", 403)
        
		if command == 'turnOn':
			self.mqtt_publish(self._settings.get(["publish"]), self._settings.get(["msgon"]), retained=True)
			self._logger.debug("Published a message to %s: %s" % (self._settings.get(["publish"]), self._settings.get(["msgon"])))
		elif command == 'turnOff':
			self.mqtt_publish(self._settings.get(["publish"]), self._settings.get(["msgoff"]), retained=True)
			self._logger.debug("Published a message to %s: %s" % (self._settings.get(["publish"]), self._settings.get(["msgoff"])))
		elif command == 'getState':
			self._logger.debug("Sync with MQTT broker requested, will unsubscribe and subscribe again.")
			self.mqtt_unsubscribe(self._on_mqtt_subscription)
			self.mqtt_subscribe(self._settings.get(["subscription"]), self._on_mqtt_subscription)
			self._logger.debug("Subscribed to %s" % self._settings.get(["subscription"]))


__plugin_name__ = "MQTT Smart Plug"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = MqttsmartplugPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

