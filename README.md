# AiXue
https://github.com/hh-macro
https://github.com/frida/frida/releases

### 启动说明 

##### 一、pip下载依赖 -->点击 `pip.bat` 如果无效请手动下载  (已下载请忽略)

```
pip install -r requirements.txt
```

##### 二、检查adb 是否正常连接

```
adb devices
```

##### 三、在cmd使用 `ipconfig` 获取ip4地址, 并在手机电脑连接同网络下。在网络详情中加上手动代理-->主机名为 ip4  端口`8080` (已设置好的设备忽略)

##### 四、修改项目地址 --> 将启动`main.bat` 中的 `set PYTHONPATH= ` 后面改为当前项目路径 （已修改或路径正确请忽略）

##### 五、首先启动 `启动hook.bat`  文件，等待当前脚本正常启动

##### 六、然后启动 `启动main.bat` 文件。等待脚本正常运行就是启动成功啦

注意：`启动数据处理.bat`  此处理程序请勿随意运行，可能会将 步骤五 获取到的数据覆盖清空！

提醒：配置文件在`apps/conf.yaml` 中，可自定义修改配置。

### firda-hook

##### 一、推送frida-server

```
db push frida-server-16.5.9-android-arm64 /data/local/tmp/
```

设置可执行权限

```
adb shell "chmod 755 /data/local/tmp/frida-server-16.5.9-android-arm64"
```

##### 二、开启frida服务

```shell
adb shell
cd data/local/tmp
./frida-server-16.5.9-android-arm64
```

##### 三、hook注入

```shell
frida -U -f com.aitutor.hippo -l byteDance.js
```



### adb 常用

##### 查找模拟器或者手机的CPU类型

```shell
adb shell getprop ro.product.cpu.abi
```

##### 运行应用后再附加脚本，避免过早注入

```
frida -U -n com.aitutor.hippo -l byteDance.js
```

##### 更换端口启动frida

```
./fri666 -l 0.0.0.0:1234
```

##### 查看frida-server是否启动
```
adb shell "ps -A | grep frida-server"
```
##### 关闭服务
```
db shell "pkill -f frida-server"  # 强制终止设备上所有与 Frida Server 相关的进程
adb shell "su -c 'kill -9 20048'"  
```
#### 

`byteDance.js`

```javascript
function patch(address) {
    Memory.protect(address, 4, 'rwx');
    Memory.writeByteArray(address, [0x00, 0x00, 0x80, 0x52]);
}

function onLoad(name, callback) {
    //void* android_dlopen_ext(const char* filename, int flag, const android_dlextinfo* extinfo);
    const android_dlopen_ext = Module.findExportByName(null, "android_dlopen_ext");
    if (android_dlopen_ext != null) {
        Interceptor.attach(android_dlopen_ext, {
            onEnter: function (args) {
                if (args[0].readCString().indexOf(name) !== -1) {
                    this.hook = true;
                }
            }, onLeave: function (retval) {
                if (this.hook) {
                    callback();
                }
            }
        });
    }
}

function main() {
    Java.perform(function () {
        const soName = 'libsscronet.so';
        onLoad(soName, () => {
            let SSL_CTX_set_custom_verify = Module.getExportByName(soName, 'SSL_CTX_set_custom_verify');
            if (SSL_CTX_set_custom_verify != null) {
                Interceptor.attach(SSL_CTX_set_custom_verify, {
                    onEnter: function (args) {
                        Interceptor.attach(args[2], {
                            onLeave: function (retval) {
         
                                if (retval > 0x0) retval.replace(0x0);
                            }
                        });
                    }
                });
            }
        });
    });
}

setImmediate(main);
// setTimeout(main, 10000);
// frida -U -f com.ss.android.ugc.aweme -l Android/byteDance.js
```

