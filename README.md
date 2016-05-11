##腾讯云CDN API 概览
## 消耗及统计量查询

| API                                      | 功能说明                                     |
| ---------------------------------------- | ---------------------------------------- |
| [DescribeCdnHostInfo](https://www.qcloud.com/doc/api/231/查询CDN汇总数据) | 查询流量、带宽、请求数、IP访问数、命中率等总统计信息              |
| [DescribeCdnHostDetailedInfo](https://www.qcloud.com/doc/api/231/查询CDN详细数据) | 查询流量、带宽、请求数、IP访问数、命中率等统计明细信息，1-3日时间粒度为5分钟，3-7日明细粒度为1小时，7-30日明细粒度为1天 |
| [GetCdnStatusCode](https://www.qcloud.com/doc/api/231/查询返回码统计) | 查询返回码 200、206、304、404、416、500 统计明细       |
| [GetCdnStatTop](https://www.qcloud.com/doc/api/231/查询排名) | 查询省份、运营商、URL的流量/带宽排名情况，TOP100            |



## 域名查询

| API                                      | 功能说明                             |
| ---------------------------------------- | -------------------------------- |
| [DescribeCdnHosts](https:www.qcloud.com/doc/api/231/查询全部域名详情) | 查询所有域名详细信息，包括配置信息，支持分页查询         |
| [GetHostInfoByHost](https://www.qcloud.com/doc/api/231/根据域名查询域名详情) | 根据域名查询域名详细信息，包括配置信息，支持多个域名查询     |
| [GetHostInfoById](https://www.qcloud.com/doc/api/231/根据ID查询域名详情) | 根据域名ID查询域名详细信息，包括配置信息，支持多个域名ID查询 |



## 域名管理

| API                                      | 功能说明                     |
| ---------------------------------------- | ------------------------ |
| [AddCdnHost](https://www.qcloud.com/doc/api/231/%E6%96%B0%E5%A2%9E%E5%8A%A0%E9%80%9F%E5%9F%9F%E5%90%8D)| 接入域名至腾讯云CDN              |
| [OnlineHost](https://www.qcloud.com/doc/api/231/上线CDN域名) | 上线指定CDN域名                |
| [OfflineHost](https://www.qcloud.com/doc/api/231/下线CDN域名) | 下线指定CDN域名                |
| [DeleteCdnHost](https://www.qcloud.com/doc/api/231/删除域名) | 删除指定CDN域名                |
| [UpdateCdnHost](https://www.qcloud.com/doc/api/231/修改源站信息) | 修改域名源站设置                 |
| [UpdateCdnProject](https://www.qcloud.com/doc/api/231/修改域名所属项目) | 修改域名所属项目                 |
| [UpdateCache](https://www.qcloud.com/doc/api/231/修改缓存规则) | 修改域名对应的缓存规则配置            |
| [UpdateCdnConfig](https://www.qcloud.com/doc/api/231/修改域名配置信息) | 对指定域名的缓存、防盗链、回源等各项信息进行设置 |



## 域名刷新

| API                                      | 功能说明                |
| ---------------------------------------- | ------------------- |
| [GetCdnRefreshLog](https://www.qcloud.com/doc/api/231/查询刷新纪录) | 查询指定时间区间内，刷新日志、刷新次数 |
| [RefreshCdnUrl](https://www.qcloud.com/doc/api/231/刷新URL) | 刷新URL               |
| [RefreshCdnDir](https://www.qcloud.com/doc/api/231/刷新目录) | 刷新目录                |

 

## 日志查询

| API                                      | 功能说明     |
| ---------------------------------------- | -------- |
| [GenerateLogList](https://www.qcloud.com/doc/api/231/查询日志下载链接) | 查询日志下载链接 |



## 辅助工具

| API                                      | 功能说明         |
| ---------------------------------------- | ------------ |
| [GetCdnMiddleSourceList](https://www.qcloud.com/doc/api/231/查询CDN中间源IP列表) | 查询CDN中间源IP列表 |

