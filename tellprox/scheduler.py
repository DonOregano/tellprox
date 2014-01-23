from bottle import *
import bottle_helpers as bh
import tellcore.telldus as td
import time

class SchedulerAPI(object):
	config = None
	core = td.TelldusCore()
	jobs = {}

	def __init__(self, api, config):
		self.config = config
		
		self.jobs = config['jobs']
		self.jobs['1'] = {
			"id":"335108",
			"deviceId":"2",
			"method":"16",
			"methodValue":"217",
			"nextRunTime":0,
			"type":"time",
			"hour":"6",
			"minute":"25",
			"offset":0,
			"randomInterval":0,
			"retries":3,
			"retryInterval":5,
			"reps":1,
			"active":"0",
			"weekdays":"1,2,3,4,5"
		}
		
		id = { 'name': 'id', 'type': 'int', 'description': 'The id of the device' }
		
		api.add_route('scheduler', {
			'joblist': {
				'fn': self.joblist
			},
			'setjob': {
				'fn': self.setjob,
				'inputs': [
				{ 'name': 'id', 'type': 'string', 'description': 'The job id, when updating an existing job' },
				{ 'name': 'deviceId', 'type': 'string', 'description': 'The device id to schedule. Only valid when creating a new job' },
				{ 'name': 'method', 'type': 'string', 'description': 'What to do when the schdule runs. This should be any of the method constants' },
				{ 'name': 'methodValue', 'type': 'string', 'description': 'Only required for methods that requires this.' },
				{ 'name': 'type', 'type': 'dropdown', 'description': 'This can be \'time\', \'sunrise\' or \'sunset\'', 'options': ['time', 'sunrise', 'sunset'] },
				{ 'name': 'hour', 'type': 'string', 'description': 'A value between 0-23', 'default': time.strftime("%H") },
				{ 'name': 'minute', 'type': 'string', 'description': 'A value between 0-59' },
				{ 'name': 'offset', 'type': 'string', 'description': 'A value between -1439-1439. This is only used when type is either \'sunrise\' or \'sunset\'' },
				{ 'name': 'randomInterval', 'type': 'string', 'description': 'Number of minutes after the specified time to randomize.' },
				{ 'name': 'retries', 'type': 'string', 'description': 'If the client is offline, this specifies the number of times to retry executing the job before consider the job as failed.' },
				{ 'name': 'retryInterval', 'type': 'string', 'description': 'The number if minutes between retries. Example: If retries is 3 and retryInterval is 5 the scheduler will try executing the job every five minutes for fifteen minutes.' },
				{ 'name': 'reps', 'type': 'string', 'description': 'Number of times to resend the job to the client, for better reliability' },
				{ 'name': 'active', 'type': 'dropdown', 'description': 'Is the job active or paused?', 'options': ['1|1 (active)', '0|0 (paused)'] },
				{ 'name': 'weekdays', 'type': 'dropdown-multiple', 'description': 'A comma separated list of weekdays. 1 is monday. Example: 2,3,4', 'options': ['1|1 (Monday)', '2|2 (Tuesday)', '3|3 (Wednesday)', '4|4 (Thursday)', '5|5(Friday)', '6|6(Saturday)', '7|7(Sunday)'] }
				]
			}
		})

	def joblist(self, func):
		"""Job list"""
		return { 'job': [
			job for id, job in self.jobs.iteritems()
		]}
	
	def setjob(self, func, id, deviceId, method, methodValue, type, hour,
	minute, offset, randomInterval, retries, retryInterval, reps, active, weekdays):
		
		# If no ID is provided, find the next available
		if id:
			try:
				int(number)
			except ValueError:
				id = None
		
		if id is None or len(id) == 0:
			id = str(max([int(k) for k in self.config['jobs'].keys()]) + 1)

		self.config['jobs'][id] = {
			'id'             : id,
			'deviceId'       : deviceId,
			'method'         : method,
			'methodValue'    : methodValue,
			'nextRunTime'    : 'todo',
			'type'           : type,
			'hour'           : hour,
			'minute'         : minute,
			'offset'         : offset,
			'randomInterval' : randomInterval,
			'retries'        : retries,
			'retryInterval'  : retryInterval,
			'reps'           : reps,
			'active'         : active,
			'weekdays'       : weekdays
		}
		self.config.write()
		return { 'id' : id, 'nextRunTime': 'todo', 'w': weekdays }