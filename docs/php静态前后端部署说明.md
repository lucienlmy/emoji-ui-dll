# PHP 静态前后端部署说明

## 1. 项目结构
这套后台采用“静态前端 + PHP 接口”的方式部署。

- `php/public/index.html`
  门户首页，展示统计数据、趋势和广告位预览
- `php/public/admin.html`
  后台管理页，登录后管理广告位
- `php/public/assets/css/app.css`
  本地样式文件
- `php/public/assets/js/*.js`
  本地脚本文件，不依赖外部 CDN
- `php/api/*.php`
  前台公开接口
- `php/api/admin/*.php`
  后台管理接口
- `php/includes/config.php`
  数据库配置
- `php/includes/db.php`
  PDO 数据库连接
- `php/includes/auth.php`
  后台登录与会话校验
- `php/database/schema.sql`
  数据库表结构和演示数据

## 2. 环境要求
- PHP 8.1 及以上
- MySQL 5.7 及以上，建议 MySQL 8.x
- Apache 或 Nginx
- 浏览器能正常访问同站点下的 `php/public` 和 `php/api`

## 3. 部署前准备
### 3.1 上传目录
把 `php` 目录完整上传到服务器。

### 3.2 建议站点根目录
建议把 Web 根目录指向：

`php/public`

这样浏览器直接访问的就是：

- `/index.html`
- `/admin.html`

同时接口路径通过相对地址访问：

- `../api/stats.php`
- `../api/ads.php`
- `../api/admin/*.php`

如果你的站点不能直接把根目录指到 `php/public`，也可以把整个 `php` 目录放在网站目录下，然后通过：

- `/php/public/index.html`
- `/php/public/admin.html`

进行访问。

## 4. 数据库初始化
### 4.1 创建数据库和表
执行：

`php/database/schema.sql`

这个 SQL 会完成以下内容：

- 创建数据库 `ad_portal`
- 创建管理员表 `admin_users`
- 创建广告位表 `ads`
- 创建统计表 `daily_stats`
- 插入默认管理员账号
- 插入演示广告位和演示统计数据

### 4.2 默认管理员账号
初始化 SQL 已写入默认账号：

- 账号：`admin`
- 密码：`admin123456`

上线后建议第一时间改成你自己的密码哈希。

## 5. 修改数据库配置
编辑文件：

`php/includes/config.php`

默认配置如下：

```php
const DB_HOST = '127.0.0.1';
const DB_PORT = 3306;
const DB_NAME = 'ad_portal';
const DB_USER = 'root';
const DB_PASSWORD = '123456';
const DB_CHARSET = 'utf8mb4';
```

你需要把它改成服务器的真实数据库信息。

## 6. 访问方式
### 6.1 前台门户
访问：

- `index.html`

用途：

- 查看日活量
- 查看软件打开次数
- 查看使用人数
- 查看趋势图
- 查看前台广告位预览

### 6.2 后台管理
访问：

- `admin.html`

用途：

- 登录后台
- 添加广告位
- 编辑广告位
- 删除广告位
- 启用或停用广告位
- 修改排序值并保存

## 7. Apache 部署要点
如果你用 Apache，确保启用：

- `mod_php` 或 PHP-FPM
- `session` 功能正常

只要 PHP 能执行，且 `php/public` 与 `php/api` 在同一站点可访问，一般即可直接运行。

## 8. Nginx 部署要点
如果你用 Nginx，确保：

- 静态文件能正常访问
- `.php` 请求已经转发到 PHP-FPM
- `php/public` 与 `php/api` 保持同站点路径关系

典型思路：

- 静态页面从 `php/public` 提供
- 接口请求访问 `php/api/*.php`
- `Set-Cookie` 不被代理层拦截

## 9. Session 登录说明
后台登录使用 PHP Session。

这意味着：

- `admin/login.php` 登录成功后会写入 Session
- 后续后台接口依赖浏览器自动携带 Cookie
- 如果后台总是提示“请先登录后台”，通常是 Session 或 Cookie 路径不对

建议检查：

- 前端页面和 PHP 接口是否属于同一站点
- 浏览器是否拦截 Cookie
- 反向代理是否改写了 Cookie

## 10. 常见问题
### 10.1 页面打开但数据不显示
请检查：

- `php/api/stats.php` 能否直接访问
- `php/api/ads.php` 能否直接访问
- 数据库是否已导入 `schema.sql`
- `php/includes/config.php` 是否正确

### 10.2 后台登录成功后又提示未登录
通常是以下原因：

- Session 没有正常保存
- 页面与接口不在同站点
- 代理层导致 Cookie 丢失

### 10.3 接口返回 500
请重点检查：

- PHP 版本是否过低
- MySQL 是否可连接
- 数据库表是否已创建
- `config.php` 的数据库账号密码是否正确

### 10.4 静态资源 404
请检查以下文件是否存在：

- `php/public/assets/css/app.css`
- `php/public/assets/js/index.js`
- `php/public/assets/js/admin.js`
- `php/public/assets/js/chart.js`
- `php/public/assets/js/http.js`

## 11. 上线前建议
- 修改默认管理员账号密码
- 删掉演示统计数据和演示广告位
- 用真实数据库账号替换 `root`
- 确认 `php/public` 对外可访问
- 确认 `php/includes` 和 `php/database` 不暴露给公网下载
- 在正式域名下验证前台与后台登录流程

## 12. 最简部署流程
1. 上传 `php` 目录到服务器。
2. 导入 `php/database/schema.sql`。
3. 修改 `php/includes/config.php`。
4. 配置站点可访问 `php/public/index.html` 和 `php/public/admin.html`。
5. 确认 `php/api/*.php` 可以执行。
6. 打开前台和后台页面进行联调。
