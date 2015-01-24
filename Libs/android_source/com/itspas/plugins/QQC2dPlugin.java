package com.itspas.plugins;

import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.util.Log;

import com.itspas.c2dplugin.JC2dPlugin;
import com.itspas.c2dplugin.JC2dPluginContext;
import com.tencent.connect.UserInfo;
import com.tencent.tauth.IUiListener;
import com.tencent.tauth.Tencent;
import com.tencent.tauth.UiError;

public class QQC2dPlugin extends JC2dPlugin {
	private Tencent tencent = null;
	
	@Override
	public String invoke(String funcName) {
		if ("login".equals(funcName)) {
			login();
		}else if ("getUserInfo".equals(funcName)){
			getUserInfo();
		}
		return null;
	}
	
	private void getUserInfo() {
		Log.i("", "GetUserInfo:" + this.hashCode());
		if (tencent != null) {
			Log.i("", "Token:" + tencent.getQQToken().getAccessToken() + " openId:" + tencent.getAppId());
			UserInfo info = new UserInfo(JC2dPluginContext.SharedCentext().getContext(), tencent.getQQToken());
			info.getUserInfo(new IUiListener() {
				
				@Override
				public void onError(UiError arg0) {
					// TODO Auto-generated method stub
					Log.i("", "onError:"+arg0.errorCode);
				}
				
				@Override
				public void onComplete(Object arg0) {
					// TODO Auto-generated method stub
					Log.i("", "onComplete:"+arg0);
					JSONObject json = (JSONObject)arg0;
					try {
						QQC2dPlugin.this.postNotification("Tom", json.getString("figureurl_2"));
					} catch (JSONException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
					
				}
				
				@Override
				public void onCancel() {
					// TODO Auto-generated method stub
					Log.i("", "onCancel");
				}
			});
		}
	}

	private void login() {
		Log.i("", "Login:" + this.hashCode());
		if (tencent == null) {
			String appId = getStringArgv();
			Log.i("", "Log AppId:" + appId);
			tencent = Tencent.createInstance(appId, JC2dPluginContext.SharedCentext().getContext());
			Log.i("", "tencent:" + tencent.toString());
			if (!tencent.isSessionValid()) {
				tencent.login((Activity)JC2dPluginContext.SharedCentext().getContext(), "all", new IUiListener() {
					
					@Override
					public void onError(UiError arg0) {
						// TODO Auto-generated method stub
						Log.i("", "onError");
					}
					
					@Override
					public void onComplete(Object arg0) {
						// TODO Auto-generated method stub
						Log.i("", "onComplete" + arg0);
						Log.i("", "onEvent");
					}
					
					@Override
					public void onCancel() {
						// TODO Auto-generated method stub
						Log.i("", "onCancel");
					}
				});
			}
		}
	}
	
}
