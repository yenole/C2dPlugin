
#include "C2dPlugins.h"
#include "OC2dPlugin.h"


USING_NS_CC;


va_list argv;

namespace C2dPlugins {

    C2dPlugin::C2dPlugin():m_pObject(NULL)
    {

    }
    
    C2dPlugin::~C2dPlugin()
    {
        if(m_pObject){
            OC2dPlugin* plugin = (OC2dPlugin*)m_pObject;
            [plugin dealloc];
        }
    }


    const char* C2dPlugin::invoke(const char* funcName, ...)
    {
        Class clazz = NSClassFromString([NSString stringWithUTF8String:szPluginName]);
        CCLog("class:%p",clazz);
        if (clazz) {
            if (!m_pObject) {
                
                NSObject* pobject = [[clazz alloc] init];
                if (![pobject isKindOfClass:[OC2dPlugin class]]){
                    [pobject dealloc];
                    return  NULL;
                }
                CCLog("Init OC2dPlugin:%p",pobject);
                m_pObject = pobject;
            }
            OC2dPlugin* plugin = (OC2dPlugin *)m_pObject;
            CCLog("C2dPlugin Call Func:%s by Object:%p", funcName, m_pObject);
            va_start(argv, funcName);
            NSString* result = [plugin invoke:[NSString stringWithUTF8String:funcName]];
            va_end(argv);
            return result?[result UTF8String]:NULL;
        }
        return NULL;
    }


}


@implementation OC2dPlugin

-(NSString *)invoke:(NSString *)funcName
{
    return nil;
}

-(void)postNotification:(NSString *)notify :(NSString *)value
{
    if (notify && value){
        CCString *szvalue = CCString::createWithFormat("%s",[value UTF8String]);
        CCNotificationCenter::sharedNotificationCenter()->postNotification([notify UTF8String],szvalue);
    }
}

-(BOOL)getBoolArgv
{
    return va_arg(argv, int);
}

-(char)getCharArgv
{
    return va_arg(argv, int);
}

-(int)getIntArgv
{
    return va_arg(argv, int);
}

-(long)getLongArgv
{
    return va_arg(argv, long);
}

-(float)getFloatArgv
{
    return va_arg(argv, double);
}

-(double)getDoubleArgv
{
    return va_arg(argv, double);
}

-(NSString *)getStringArgv
{
    const char* val = va_arg(argv, char*);
    return val?[NSString stringWithUTF8String:val]:nil;
}

@end
