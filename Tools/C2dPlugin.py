#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-01-20 16:20:51
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$
import sys,os,copy

class DisponseHandle(object):
	def __init__(self):
		super(DisponseHandle, self).__init__()
		
	def handle(self):
		if len(sys.argv) > 4:
			handles = {'add':AddHandle,'rm':RemoveHandle}
			handle = handles[sys.argv[2]] if sys.argv[2] in handles else  HelperHandle
			handle().handle()


class Handle(object):
	def __init__(self):
		super(Handle, self).__init__()
		
	def handle(self):
		pass

class HelperHandle(Handle):
	def __init__(self):
		super(HelperHandle, self).__init__()
		
	
		

class AddHandle(Handle):
	def __init__(self):
		super(AddHandle, self).__init__()

	def handle(self):
		handles = {'android':AndroidPlatformHandle,'ios':IOSPlatformHandle}
		if sys.argv[3] in handles :
			handles[sys.argv[3]]().install()
		else:
			print('Unknown platform!')


class RemoveHandle(Handle):
	def __init__(self):
		super(RemoveHandle, self).__init__()


class PlatformHandle(object):
	def __init__(self):
		super(PlatformHandle, self).__init__()

	def install(self):
		pass

	def unInstall(self):
		pass
		

class AndroidPlatformHandle(PlatformHandle):
	def __init__(self):
		super(AndroidPlatformHandle, self).__init__()

	def install(self):
		print('Plugin %s install successfull!' % sys.argv[4])

	def unInstall(self):
		print('Plugin %s unInstall successfull!' % sys.argv[4])
		
class IOSPlatformHandle(PlatformHandle):
	def __init__(self):
		super(IOSPlatformHandle, self).__init__()
		


if __name__ == '__main__':
	DisponseHandle().handle()
