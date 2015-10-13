# 腾讯云CDN API接口调用示例

当前包含的示例有：
* 添加域名
* 通过host获取域名信息
* 通过host id获取域名信息
* 文件刷新
* 修改域名配置

## 接口简述
### 添加加速域名
* AddCdnHost　：新增域名，只包含基本参数
* EAddCdnHost ：这个接口比AddCdnHost支持更多可选参数

### 修改域名配置
* UpdateCdnCache    ：修改缓存设置
* UpdateCdnProjectId：修改所属项目
* UpdateCdnConfig   ： 修改更多配置项，详见demo

### 刷新URL
* RefreshCdnUrl

### 刷新dir
* RefreshCdnDir

### 获取域名信息
* GetHostInfoByHost ： 根据域名获取域名信息
* GetHostInfoById   ： 根据域名id获取域名信息

### 文件预拉热接口（需加白名单，请联系客户经理）
* CdnPusher

### 获取最近一个月的日志下载链接
* GenLogList

## 其他说明
* 当前支持GET和POST方式的参数传递方式
* 使用时把demo里的YOUR_SECRET_ID和YOUR_SECRET_KEY替换成自己的腾讯云secret id和secret_key
* id和key到 https://console.qcloud.com/capi 页面获取
* wiki http://www.qcloud.com/wiki//v2/RefreshCdnUrl
