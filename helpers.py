#!/usr/bin/env python3
"""
__author__ = "Praveen Kumar Pendyala"
__email__ = "mail@pkp.io"
"""
import logging
import json
import fitbit
import httplib2
import types
from oauth2client.file import Storage
from apiclient.discovery import build

def get_sleep_v12(self, date):
	"""
	https://wiki.fitbit.com/display/API/API-Get-Sleep
	date should be a datetime.date object.
	"""
	url = "{0}/1.2/user/-/sleep/date/{year}-{month}-{day}.json".format(
		*self._get_common_args(),
		year=date.year,
		month=date.month,
		day=date.day
	)
	return self.make_request(url)


class Helper(object):
	"""Helper methods to hide trivial methods"""

	def __init__(self, fitbitCredsFile, googleCredsFile):
		""" Intialize a helper object.

		fitbitCredsFile -- Fitbit credentials file
		googleCredsFile -- Google Fits credentials file
		"""
		self.fitbitCredsFile = fitbitCredsFile
		self.googleCredsFile = googleCredsFile

	def GetFitbitClient(self):
		"""Returns an authenticated fitbit client object"""
		logging.debug("Creating Fitbit client")
		credentials = json.load(open(self.fitbitCredsFile))  
		client = fitbit.Fitbit(**credentials)
		client.get_sleep_v12 = types.MethodType(get_sleep_v12, client)
		logging.debug("Fitbit client created")
		return client

	def GetGoogleClient(self):
		"""Returns an authenticated google fit client object"""
		logging.debug("Creating Google client")
		credentials = Storage(self.googleCredsFile).get()
		http = credentials.authorize(httplib2.Http())
		client = build('fitness', 'v1', http=http)
		logging.debug("Google client created")
		return client

	def UpdateFitbitCredentials(self, fitbitClient):
		"""Persists new fitbit credentials to local storage

		fitbitClient -- fitbit client object that contains the latest credentials
		"""
		credentials = json.load(open(self.fitbitCredsFile)) 
		for t in ('access_token', 'refresh_token'):
			credentials[t] = fitbitClient.client.session.token[t]
		json.dump(credentials, open(self.fitbitCredsFile, 'w'))
