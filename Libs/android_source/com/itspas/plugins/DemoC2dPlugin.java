package com.itspas.plugins;

import com.itspas.c2dplugin.JC2dPlugin;

public class DemoC2dPlugin extends JC2dPlugin {

	@Override
	public String invoke(String funcName) {
		if ("string".equals(funcName)) {
			return "string";
		}else if("int".equals(funcName)){
			return 1 + "";
		}
		return null;
	}

}
