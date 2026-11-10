## MsEdge 便携版, 项目简介

本项目全自动构建，每天定时检查 Microsoft 官方是否有最新 Edge 离线安装包更新，集成 msedge++ 组件并打包为便携版。项目预配置了自定义增强功能，具体配置请查看 `msedge++(example).ini`。

目前项目默认同步构建 Stable  X64版本。

## 快速开始

1. 从 [Releases](https://github.com/yxl0756/portable_msedge/releases/latest) 下载压缩包，解压到任意位置
2. 注意, 如果portable_msedge的配置目录不可写入, 它将禁用便携功能, 但其他特性不受影响
3. 双击Msedge\App\msedge.exe启动, 你也可以手动创建它到桌面的快捷方式

## 安全性

1. 从下载, 注入, 打包, 全程透明, 基于代码仓库内的开源脚本进行, 无暗箱操作
2. 使用到的二进制包msedge++全部基于开源代码, 你可以到[原作者仓库](https://github.com/adonais)获取源代码

## 更新

1. 从 [Releases](https://github.com/yxl0756/portable_msedge/releases/latest) 下载发布的新版本
2. 关闭Edge浏览器, 解压直接覆盖到Msedge目录
3. 默认支持自动更新, 取消更新见 msedge++(example).ini 配置文件说明

## 功能特性

与chrome++相比：

- 删除version.dll劫持代码, Edge不适用并且容易误报病毒
- 删除PAK文件内存修改, 因为在edge上不适用
- 删除一些个人感觉无意义的功能, 见 msedge++(example).ini
- 改写tabs功能, 因为 chrome++ 的标签页功能在edge上不生效
- 改写代码, 自带的示例配置文件不会覆盖用户的配置文件
- 改进代码, 在无写权限的目录忽略data_dir与cache_dir选项
- 注入时静态修改resources.pak, 屏蔽升级错误, 以及默认浏览器选项
- 更多增强功能请查看 msedge++(example).ini

<details>
<summary><b>更改数据目录位置</b></summary>

数据目录的位置由 `msedge++.ini` 里的 `data_dir` 和 `cache_dir` 两行决定，默认值是 `%app%\..\Data` 和 `%app%\..\Cache`（`%app%` 代表 `msedge.exe` 所在目录，.. 代表上级目录）。值支持绝对路径，目录会自动创建。注意这个文件是 **UTF-16 编码**（记事本另存时选「Unicode」）。

## 卸载

删除Msedge目录即可，便携版不写注册表。若之前设置过默认浏览器，先在 Windows 设置中改回原浏览器。



## 致谢

本项目基于以下优秀开源项目构建：

| 项目 | 说明 |
| --- | --- |
| [Adonais/libportable](https://github.com/adonais/libportable) | 提供核心便携化组件（msedge++ / setdll） |
| [Bush2021/edge_installer](https://github.com/Bush2021/edge_installer) | 自动查询与下载代码Fork自此仓库 |
| Microsoft Edge CDP API | Edge 官方版本查询与安装包下载 |

## 许可证

本项目源码遵循 MIT 许可证。

- Microsoft Edge 浏览器版权归 Microsoft 所有

