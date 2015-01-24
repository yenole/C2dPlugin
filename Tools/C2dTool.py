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
		is3x = not os.path.exists(utils.get_project_dir('/Classes'))
		if is3x:
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
		file_src = utils.get_sdk_dir('/Libs/lib_%s/sdk' % platform)
		[utils.copy,utils.delete][operate](file_src,file_desc)
		if platform == 'android':
			file_src = utils.get_sdk_dir('/Libs/lib_%s/lib' % platform)
			file_desc = '%s/../proj.android/libs' % utils.get_project_dir(utils.get_sdk_info())
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

class androidmkModule(module):
	def __init__(self):
		super(androidmkModule, self).__init__()
		self.__path_project = None
		self.__mk_file = None
		self.__cpp_file = []
		self.__h_file = []
		
	def handle(self):
		info = utils.get_platform_info('android')
		self.__mk_file = utils.get_project_dir('%s/jni/android.mk' % info['src'])
		if not os.path.exists(self.__mk_file):
			return 'not found android.mk file!'
		self.__path_project = utils.get_project_dir('%s/..' % info['src'])
		sys.argv.append('Classes')
		for i in xrange(2,len(sys.argv)):
			path = '%s/%s' % (self.__path_project,sys.argv[i])
			if self.__scan_file(path) > 0:
				self.__h_file.append('$(LOCAL_PATH)/../..%s' % path[len(self.__path_project):])
		return self.__write_to_mkfile()



	def __scan_file(self,path):
		file_list = os.listdir(path)
		count = 0
		for file_name in file_list:
			if file_name.startswith('.') or file_name == 'main.cpp':
				continue
			file_name = path + '/' + file_name
			if os.path.isdir(file_name) and self.__scan_file(file_name) > 0:
				self.__h_file.append('$(LOCAL_PATH)/../..%s' % file_name[len(self.__path_project):])
			elif file_name.endswith('.cpp'):
				count += 1
				self.__cpp_file.append('../..%s' % file_name[len(self.__path_project):])
		return count

	def __write_to_mkfile(self):
		try:
			mkfile = open(self.__mk_file)
			self.__cnt = mkfile.read()
			key = 'LOCAL_SRC_FILES'
			idx = self.__cnt.find(key)
			bcnt = self.__cnt[:idx + len(key)] + ' := '
			key = 'LOCAL_C_INCLUDES'
			idx = self.__cnt.find(key)
			icnt = self.__cnt[idx:idx + len(key)] + ' := '
			ecnt = self.__cnt[idx + len(key) + 4:]
			idx = ecnt.find('\x0A\x0A')
			ecnt = ecnt[idx:]

			count = len(self.__cpp_file)
			for i,v in enumerate(self.__cpp_file):
				bcnt += v + ('\x20\x5C\x0A\x09\x09\x09\x09' if i < count - 1 else '')

			count = len(self.__h_file)
			for i,v in enumerate(self.__h_file):
				icnt +=  v + ('\x20\x5C\x0A\x09\x09\x09\x09\x20' if i < count - 1 else '')

			mkfile = open(self.__mk_file,'w')
			mkfile.write(bcnt + '\x0A\x0A' + icnt + ecnt)

			mkfile.close()
			return 'build android.mk file successful!'

		except Exception, e:
			mkfile.close
			return 'Error: build android.mk fail!'
			

		
class disponseModule(object):
	def __init__(self):
		super(disponseModule, self).__init__()
	
	def handle(self):
		mds = {'plugin':pluginModule,'android.mk':androidmkModule}
		if len(sys.argv) > 1 and sys.argv[1] in mds:
			print('MSG:%s' % mds[sys.argv[1]]().handle())
		else:
			print('argv error!')


if __name__ == '__main__':
	disponseModule().handle()