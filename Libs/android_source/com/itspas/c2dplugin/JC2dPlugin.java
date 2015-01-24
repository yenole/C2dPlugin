package com.itspas.c2dplugin;

public class JC2dPlugin {

	public String invoke(String funcName) {
		return null;
	}
	
	public native void postNotification(String notify,String value);
	
	public native boolean getBooleanArgv();
	
	public native char getCharArgv();
	
	public native int getIntArgv();
	
	public native long getLongArgv();
	
	public native float getFloatArgv();
	
	public native double getDoubleArgv();
	
	public native String getStringArgv();
}
