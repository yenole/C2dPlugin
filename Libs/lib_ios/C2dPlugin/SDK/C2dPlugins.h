//
//  C2dPlugins.h
//  c2dplugin
//
//  Created by apple on 15/1/17.
//
//

#ifndef __c2dplugin__C2dPlugins__
#define __c2dplugin__C2dPlugins__

#include <stdio.h>
#include "cocos2d.h"


namespace C2dPlugins {
    
    class C2dPlugin
    {
    public:
        C2dPlugin();
        
        ~C2dPlugin();

        const char* invoke(const char* funcName,...);

    public:
        const char*         szPluginName;

    private:
        void*				m_pObject;
    };
}

#endif /* defined(__c2dplugin__C2dPlugins__) */
