#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-01-20 16:20:51
# @Author  : ITspas (ITspas@vip.qq.com)
# @Link    : http://blog.itspas.com/
# @Version : 1.0
import os,sys,zipfile,json,shutil

class Handle(object):
	def __init__(self):
		super(Handle, self).__init__()
	
	def handle(self):
		pass

class DisponseHandle(Handle):
	def __init__(self):
		super(DisponseHandle, self).__init__()

	def handle(self):
		if not os.path.exists('%s/Classes' % os.getcwd()):
			print(u'当前目录不是cocos2d-x项目,请切换到cocos2d-x项目中!')
		else:
			hds = {'init':InitHandle,'add':AddHandle,'rm':RmHandle}
			if len(sys.argv) > 2 and sys.argv[2] in hds:
				hds[sys.argv[2]]().handle()
			else:
				print(u'参数不对!')

class InitHandle(Handle):
	def __init__(self):
		super(InitHandle, self).__init__()
				
	def handle(self):
		if len(sys.argv) > 3:
			platform = sys.argv[3]
			# 检查是否支持此平台
			path_lib = '%s/../Libs/lib_%s.zip' % (sys.path[0],platform)
			if os.path.exists(path_lib):
				file_lib = zipfile.ZipFile(path_lib)
				file_lib.extractall('%s/Classes' % os.getcwd())
				file_lib.close()
				print(u'初始化成功!')
			else:
				print(u'暂时不支持此平台!')
		else:
			print(u"初始化失败,缺少平台参数!")


class AddHandle(Handle):
	def __init__(self):
		super(AddHandle, self).__init__()
		
	def handle(self):
		plugin = sys.argv[3]
		platform = sys.argv[4]
		language = sys.argv[5] if len(sys.argv) > 5 else 'cpp'
		
		# 判断是否有此插件 跟 是否支持此平台
		if os.path.exists('%s/../Plugins/%s' % (sys.path[0],plugin)):
			hds = {'android':AndroidPlatformHandle,'ios':IOSPlatformHandle}
			hds[platform](plugin).install()
			pass
		else:
			print(u'未查到插件或%s平台安装包!' % platform)


class RmHandle(Handle):
	def __init__(self):
		super(RmHandle, self).__init__()

	def handle(self):
		plugin = sys.argv[3]
		platform = sys.argv[4]
		# 判断是否有此插件 跟 是否支持此平台
		if os.path.exists('%s/../Plugins/%s' % (sys.path[0],plugin)):
			hds = {'android':AndroidPlatformHandle,'ios':IOSPlatformHandle}
			hds[platform](plugin).unInstall()
			pass
		else:
			print(u'未查到插件或%s平台安装包!' % platform)


class PlatformHandle(object):
	def __init__(self,argv):
		super(PlatformHandle, self).__init__()
		self.plugin = argv;
		self.path_plugin = '%s/../Plugins/%s' % (sys.path[0],argv)

	def install(self):
		pass

	def unInstall(self):
		pass

	def loadPluginJson(self):
		file_json = open('%s/plugin.json' % self.path_plugin,'r')
		json_plugin = json.loads(file_json.read())
		file_json.close()
		return json_plugin;

	def copy(self,src,desc):
		if not os.path.exists(desc):
			os.makedirs(desc)
		file_list = os.listdir(src)
		for file_name in file_list:
			file_real = '%s/%s' % (src,file_name)
			if os.path.isdir(file_real):
				self.copy(file_real,'%s/%s' % (desc,file_name))
			else:
				shutil.copy(file_real,desc)
				print('copy %s successfull!' % file_real[len(self.path_plugin) + 1:])

	def delete(self,src,desc):
		if not os.path.exists(desc):
			return
		file_list = os.listdir(src)
		for file_name in file_list:
			file_real = '%s/%s' % (src,file_name)
			if os.path.isdir(file_real):
				file_real = '%s/%s' % (desc,file_name)
				self.delete(file_real,file_real)
				if len(os.listdir(file_real)) == 0:
					os.rmdir(file_real)
				
			elif os.path.exists('%s/%s' % (desc,file_name)):
				file_real = '%s/%s' % (desc,file_name)
				os.remove(file_real)
				print('delete %s successfull!' % file_real[len(os.getcwd()) + 1:])


class AndroidPlatformHandle(PlatformHandle):
	def __init__(self,argv):
		super(AndroidPlatformHandle, self).__init__(argv)
		
	def install(self):
		json_plugin = self.loadPluginJson()
		if 'android' in json_plugin['platform']:
			file_list = os.listdir('%s/android' % self.path_plugin)
			if 'libs' in file_list:
				src = '%s/android/libs' % self.path_plugin
				desc = '%s/proj.android/libs' % os.getcwd()
				self.copy(src,desc)
			if 'source' in file_list:
				src = '%s/android/source' % self.path_plugin
				desc = '%s/proj.android/src' % os.getcwd()
				self.copy(src,desc)
			if 'resource' in file_list:
				src = '%s/android/resource' % self.path_plugin
				desc = '%s/Resources' % os.getcwd()
				self.copy(src,desc)
			print(u'插件"%s"安装成功!' % self.plugin)
		else:
			print(u'插件不支持Android平台!')

	def unInstall(self):
		json_plugin = self.loadPluginJson()
		if 'android' in json_plugin['platform']:
			file_list = os.listdir('%s/android' % self.path_plugin)
			if 'libs' in file_list:
				src = '%s/android/libs' % self.path_plugin
				desc = '%s/proj.android/libs' % os.getcwd()
				self.delete(src,desc)
			if 'source' in file_list:
				src = '%s/android/source' % self.path_plugin
				desc = '%s/proj.android/src' % os.getcwd()
				self.delete(src,desc)
			if 'resource' in file_list:
				src = '%s/android/resource' % self.path_plugin
				desc = '%s/Resources' % os.getcwd()
				self.delete(src,desc)
			print(u'插件"%s"卸载成功!' % self.plugin)
		else:
			print(u'插件不支持Android平台!')


class IOSPlatformHandle(PlatformHandle):
	def __init__(self, argv):
		super(IOSPlatformHandle, self).__init__(argv)
		
	def install(self):
		json_plugin = self.loadPluginJson()
		if 'ios' in json_plugin['platform']:
			file_list = os.listdir('%s/ios' % self.path_plugin)
			if 'libs' in file_list:
				src = '%s/ios/libs' % self.path_plugin
				desc = '%s/proj.ios/libs' % os.getcwd()
				self.copy(src,desc)
			if 'source' in file_list:
				src = '%s/ios/source' % self.path_plugin
				desc = '%s/proj.ios/src' % os.getcwd()
				self.copy(src,desc)
			if 'resource' in file_list:
				src = '%s/ios/resource' % self.path_plugin
				desc = '%s/Resources' % os.getcwd()
				self.copy(src,desc)
			print(u'插件"%s"安装成功!' % self.plugin)
		else:
			print(u'插件不支持IOS平台!')

	def unInstall(self):
		json_plugin = self.loadPluginJson()
		if 'ios' in json_plugin['platform']:
			file_list = os.listdir('%s/ios' % self.path_plugin)
			if 'libs' in file_list:
				src = '%s/ios/libs' % self.path_plugin
				desc = '%s/proj.ios/libs' % os.getcwd()
				self.delete(src,desc)
			if 'source' in file_list:
				src = '%s/ios/source' % self.path_plugin
				desc = '%s/proj.ios/src' % os.getcwd()
				self.delete(src,desc)
			if 'resource' in file_list:
				src = '%s/ios/resource' % self.path_plugin
				desc = '%s/Resources' % os.getcwd()
				self.delete(src,desc)
			print(u'插件"%s"安装成功!' % self.plugin)
		else:
			print(u'插件不支持IOS平台!')



if __name__ == '__main__':
	DisponseHandle().handle()