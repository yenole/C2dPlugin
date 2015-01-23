IOS_IAP插件
---------------
#### 1.支持平台:IOS

　
#### 1.IAP
    Code:
    C2dPlugins::C2dPlugin plugin;
    plugin.szPluginName = "C2dPluginIAP";
    plugin.inovke('init');
    plugin.invoke('buy','com.itspas.point2045');
    