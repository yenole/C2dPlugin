
#include "C2dPlugins.h"
#include <jni.h>
#include "platform/android/jni/JniHelper.h"


USING_NS_CC;

va_list argv;

namespace C2dPlugins {

	static bool getEnv(JNIEnv **env)
	{
	   bool bRet = false;

	   switch(JniHelper::getJavaVM()->GetEnv((void**)env, JNI_VERSION_1_4))
	   {
	   case JNI_OK:
		   bRet = true;
		   break;
	   default:
		   break;
	   }

	   return bRet;
	}

	C2dPlugin::C2dPlugin():m_pObject(NULL)
	{

	}

	C2dPlugin::~C2dPlugin()
	{
		JNIEnv *env;
		if (m_pObject && getEnv(&env)) {
			env->DeleteGlobalRef((jobject)(m_pObject));
		}
	}


	const char* C2dPlugin::invoke(const char* funcName, ...)
	{
		JNIEnv* env;
		if (getEnv(&env)) {
			jclass classId = env->FindClass(szPluginName);
			if (!m_pObject) {
				jmethodID initMethod = env->GetMethodID(classId, "<init>", "()V");
				if (!initMethod)
					return NULL;
				jobject object = env->NewObject(classId, initMethod);
				m_pObject = env->NewGlobalRef(object);
			}
			jmethodID invokeMethod = env->GetMethodID(classId, "invoke","(Ljava/lang/String;)Ljava/lang/String;");
			if (invokeMethod) {
				CCLog("C2dPlugin Call Func:%s by Object:%p", funcName, m_pObject);
				va_start(argv, funcName);
				jstring result = (jstring)env->CallObjectMethod((jobject) m_pObject, invokeMethod,env->NewStringUTF(funcName));
				va_end (argv);
				return result?env->GetStringUTFChars(result,NULL):NULL;
			}
		}
		return NULL;
	}



}

extern "C" {

	JNIEXPORT void JNICALL Java_com_itspas_c2dplugin_JC2dPlugin_postNotification(JNIEnv* env,jobject thiz,jstring notify,jstring value) {
		if(notify && value){
			cocos2d::CCString *pstr = cocos2d::CCString::createWithFormat("%s",env->GetStringUTFChars(value,NULL));
			cocos2d::CCNotificationCenter::sharedNotificationCenter()->postNotification(env->GetStringUTFChars(notify,NULL),pstr);
		}
	}

    JNIEXPORT jboolean JNICALL Java_com_itspas_c2dplugin_JC2dPlugin_getBooleanArgv(JNIEnv* env,jobject thiz) {
    	return va_arg(argv,int);
    }

    JNIEXPORT jchar JNICALL Java_com_itspas_c2dplugin_JC2dPlugin_getCharArgv(JNIEnv* env,jobject thiz) {
    	return va_arg(argv,int);
    }

    JNIEXPORT jint JNICALL Java_com_itspas_c2dplugin_JC2dPlugin_getIntArgv(JNIEnv* env,jobject thiz) {
    	return va_arg(argv,int);
    }

    JNIEXPORT jlong JNICALL Java_com_itspas_c2dplugin_JC2dPlugin_getLongArgv(JNIEnv* env,jobject thiz) {
    	return va_arg(argv,long);
    }

    JNIEXPORT jfloat JNICALL Java_com_itspas_c2dplugin_JC2dPlugin_getFloatArgv(JNIEnv* env,jobject thiz) {
    	return va_arg(argv,double);
    }

    JNIEXPORT jdouble JNICALL Java_com_itspas_c2dplugin_JC2dPlugin_getDoubleArgv(JNIEnv* env,jobject thiz) {
    	return va_arg(argv,double);
    }

    JNIEXPORT jstring JNICALL Java_com_itspas_c2dplugin_JC2dPlugin_getStringArgv(JNIEnv* env,jobject thiz) {
    	const char* val = va_arg(argv,char*);
    	return env->NewStringUTF(val);
    }
}
