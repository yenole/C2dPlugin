package com.itspas.c2dplugin;

import java.util.HashMap;
import java.util.Map;

import android.content.Context;

public class JC2dPluginContext {
	private static JC2dPluginContext instance = null;
	private Map<String, Object> mapObject;
	
	
	private JC2dPluginContext() {
		this.mapObject = new HashMap<String, Object>();
	}
	
	public static JC2dPluginContext SharedCentext() {
		return instance==null?(instance = new JC2dPluginContext()):instance;
	}
	
	public void initContext(Context context) {
		this.mapObject.put("Context", context);
	}
	
	public Context getContext() {
		return mapObject.containsKey("Context")?(Context)mapObject.get("Context"):null;
	}
	
	public void push(String key,Object value) {
		mapObject.put(key, value);
	}
	
	public Object get(String key) {
		return mapObject.get(key);
	}
	
	public <T> T get(String key,Class<T> clazz) {
		if (mapObject.containsKey(key)) {
			return clazz.cast(mapObject.get(key));
		}
		return null;
	}
}
