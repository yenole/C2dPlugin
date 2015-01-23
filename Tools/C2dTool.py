#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-01-23 09:40:25
# @Author  : ITspas (Netxy@vip.qq.com)
# @Link    : http://blog.itspas.com/
# @Version : 1.0

import os,sys,shutil,json

class utils(object):

	@staticmethod
	def copy(src,desc):
		if not os.path.exists(desc):
			os.makedirs(desc)
		file_list = os.listdir(src)
		for file_name in file_list:
			file_src = '%s/%s' % (src,file_name)
			file_desc = '%s/%s' % (desc,file_name)
			if os.path.isdir(file_src):
				utils.copy(file_src,file_desc)
			else:
				shutil.copy(file_src,file_desc)

	@staticmethod
	def delete(src,desc):
		if os.path.exists(desc):
			file_list = os.listdir(src)
			for file_name in file_list:
				file_src = '%s/%s' % (src,file_name)
				file_desc = '%s/%s' % (desc,file_name)	
				if os.path.isdir(file_src):
					utils.delete(file_src,file_desc)
				elif os.path.exists(file_desc):
					os.remove(file_desc)
		if os.path.exists(desc) and len(os.listdir(desc)) == 0 :
			os.rmdir(desc)

	@staticmethod
	def get_platform_info(platform):
		isLua = not os.path.exists(utils.get_project_dir('/Classes'))
		if isLua:
			info = {'res':'/res','src':'/frameworks/runtime-src/'}
		else:
			info = {'res':'/Resources','src':'/'}
		if 'ios' == platform and os.path.exists('%sproj.%s_mac' % (utils.get_project_dir(info['src']),platform)):
			info['src'] = '%sproj.%s_mac/ios' % (info['src'],platform)
		else:
			info['src'] = '%sproj.%s' % (info['src'],platform)
		return info

	@staticmethod
	def get_sdk_info():
		return '/Classes' if os.path.exists(utils.get_project_dir('/Classes')) else '/frameworks/runtime-src/Classes'

	@staticmethod
	def get_project_dir(path = ''):
		return os.getcwd() + path

	@staticmethod
	def get_sdk_dir(path = ''):
		return sys.path[0] + '/..' + path

	@staticmethod
	def sdk_operate(platform,operate):
		file_desc = '%s/C2dPlugin' % utils.get_project_dir(utils.get_sdk_info())
		file_src = utils.get_sdk_dir('/Libs/lib_%s' % platform)
		[utils.copy,utils.delete][operate](file_src,file_desc)
		return 'C2dPlugin SDK %sinstall successfull!' % ['','un'][operate]

	@staticmethod
	def plugin_operate(plugin,platform,operate):
		path_plugin = '%s/%s' % (utils.get_sdk_dir('/Plugins'),plugin)
		if os.path.exists(path_plugin):
			json_plugin = utils.get_json('%s/plugin.json' % path_plugin)
			if json_plugin and platform in json_plugin['platform']:
				return {'ios':install.iosOperate,'android':install.androidOperate}[platform](plugin,operate)
			elif json_plugin:
				return '%s plugin not support %s platform!' % (plugin,platform)
			else:
				return '%s plugin uninstall fail!' % plugin
		return '%s plugin not found!' % plugin


	@staticmethod
	def get_json(path):
		if os.path.exists(path):
			file_json = open(path,'r')
			json_plugin = json.loads(file_json.read())
			file_json.close()
			return json_plugin
		return None


class install(object):
	
	@staticmethod
	def iosOperate(plugin,operate):
		info = utils.get_platform_info('ios')
		info['lib'] = '%s/C2dPlugin/%s' % (info['src'],plugin)
		info['src'] = '%s/C2dPlugin/%s' % (info['src'],plugin)
		path_plugin = utils.get_sdk_dir('/Plugins/%s/ios' % plugin)
		for key in ['lib','src','res']:
			file_src = '%s/%s' % (path_plugin,key)
			file_desc = '%s/%s' % (utils.get_project_dir(info[key]),key if key != 'res' else '')
			if os.path.exists(file_src):
				[utils.copy,utils.delete][operate](file_src,file_desc)
		file_desc = utils.get_project_dir(info['lib'])
		if os.path.exists(file_desc) and len(os.listdir(file_desc)) == 0:
			os.rmdir(file_desc)
		return '%s plugin %sinstall ios platform successfull!' % (plugin,['','un'][operate])

	@staticmethod
	def androidOperate(plugin,operate):
		info = utils.get_platform_info('android')
		info['lib'] = '%s/libs' % (info['src'])
		info['src'] = '%s/src' % (info['src'])
		path_plugin = utils.get_sdk_dir('/Plugins/%s/android' % plugin)
		print(info)
		for key in ['lib','src','res']:
			file_src = '%s/%s' % (path_plugin,key)
			file_desc = '%s' % utils.get_project_dir(info[key])
			if os.path.exists(file_src):
				[utils.copy,utils.delete][operate](file_src,file_desc)
		file_desc = utils.get_project_dir(info['lib'])
		if os.path.exists(file_desc) and len(os.listdir(file_desc)) == 0:
			os.rmdir(file_desc)
		return '%s plugin %sinstall android platform successfull!' % (plugin,['','un'][operate])


class module(object):
	def __init__(self):
		super(module, self).__init__()
		
	def handle(self):
		return None

class pluginModule(object):
	def __init__(self):
		super(pluginModule, self).__init__()
		
	def handle(self):
		hds = {'uninit':self.__uninit,'init':self.__init,'add':self.__add,'rm':self.__remove}
		if len(sys.argv) > 2 and sys.argv[2] in hds:
			return hds[sys.argv[2]]()
		return 'handle not found!'

	def __uninit(self):
		if len(sys.argv) > 3:
			return utils.sdk_operate(sys.argv[3],1)
		return 'plugin uninit error!'

	def __init(self):
		if len(sys.argv) > 3:
			return utils.sdk_operate(sys.argv[3],0)
		return 'plugin init error!'

	def __add(self):
		if len(sys.argv) > 4:
			return utils.plugin_operate(sys.argv[3],sys.argv[4],0)
		return 'plugin add error!'

	def __remove(self):
		if len(sys.argv) > 4:
			return utils.plugin_operate(sys.argv[3],sys.argv[4],1)
		return 'plugin remove error!'


		
class disponseModule(object):
	def __init__(self):
		super(disponseModule, self).__init__()
	
	def handle(self):
		mds = {'plugin':pluginModule}
		if len(sys.argv) > 1 and sys.argv[1] in mds:
			print('MSG:%s' % mds[sys.argv[1]]().handle())
		else:
			print('argv error!')


if __name__ == '__main__':
	disponseModule().handle()