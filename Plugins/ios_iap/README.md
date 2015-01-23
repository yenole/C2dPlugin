IOS_IAP插件
---------------
#### 1.支持平台:IOS
#### 2.API
```C++
    C2dPlugins::C2dPlugin plugin = new C2dPlugins::C2dPugin();
    plugin->szPluginName = "C2dPluginIAP";
    plugin->invole("init");
    plugin->invoke("buy","com.itspas.point2048");
```