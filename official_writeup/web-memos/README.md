# [Web] ICS笑传之查查表

- 命题人：thezzisu
- 题目分值：350 分

## 题目描述

<p>小小北学弟今年选修了 ICS 课程，发现答疑平台居然从 Piazza 升级成了看上去更好看的另一个平台！</p>
<p>一次偶然在食堂自习的时候，小小北学弟惊奇的发现助教学长是这个平台的管理员，他一边在吃电脑，一边在用筷子<strong>在平台上更新期中考的答案。</strong>拿到他，是不是就可以摆烂期中考了？</p>
<p>但是，责任心很强的学弟还是找到你，希望能测试网站是否存在这样的问题，以避免 ICS 期中考也出现 NO*P、C*P、CPH* 等 <del><em>虚构</em></del> 竞赛一样的泄题事故！</p>
<p>请你帮帮他找出问题，获取管理员账户存放的 Flag！</p>
<p><strong>提示：</strong>Flag 在 admin 账号的私有文章中</p>
<div class="well">
<p><strong>第二阶段提示：</strong></p>
<ul>
<li>检查一下Memos的API请求</li>
<li>看看API源码里处理Memo或者User的部分</li>
</ul>
</div>

**【网页链接：访问题目网页】**

## 预期解法

预期解是通过[Memos User Service](https://github.com/usememos/memos/blob/c3cb3770cce4771d74f2e515aa7bc4e4653c002a/server/router/api/v1/user_service.go#L223)中的逻辑缺陷来修改自己的Role为Host，这样即可通过修改密码登录到管理员账号。

然而，最新的Memos源码中，该问题并不会被触发，因为[其ORM实现的另一个问题](https://github.com/usememos/memos/blob/c3cb3770cce4771d74f2e515aa7bc4e4653c002a/store/db/sqlite/user.go#L32)导致Role字段无法更新。本题中，ORM里的设置漏洞被修复，所以上述方法可以成功提权。修改的代码如下：

```diff
func (d *DB) UpdateUser(ctx context.Context, update *store.UpdateUser) (*store.User, error) {
	set, args := []string{}, []any{}
	if v := update.UpdatedTs; v != nil {
		set, args = append(set, "updated_ts = ?"), append(args, *v)
	}
	if v := update.RowStatus; v != nil {
		set, args = append(set, "row_status = ?"), append(args, *v)
	}
	if v := update.Username; v != nil {
		set, args = append(set, "username = ?"), append(args, *v)
	}
	if v := update.Email; v != nil {
		set, args = append(set, "email = ?"), append(args, *v)
	}
	if v := update.Nickname; v != nil {
		set, args = append(set, "nickname = ?"), append(args, *v)
	}
	if v := update.AvatarURL; v != nil {
		set, args = append(set, "avatar_url = ?"), append(args, *v)
	}
	if v := update.PasswordHash; v != nil {
		set, args = append(set, "password_hash = ?"), append(args, *v)
	}
	if v := update.Description; v != nil {
		set, args = append(set, "description = ?"), append(args, *v)
	}
+	if v := update.Role; v != nil {
+		set, args = append(set, "role = ?"), append(args, *v)
+	}
	args = append(args, update.ID)
```

然而，Memos本身对Memo的查询API也存在筛选缺陷，这个在比赛期间就被[修复](https://github.com/usememos/memos/commit/b4d72e334993c372ec1567362b8f1f75a9f77122)。所以，本题的难度大大降低，从快乐源码审计题变为了快乐源码搜索题。

感谢诸位选手为开源社区做出的贡献。
