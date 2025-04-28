# AiXue

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
#### 针对ZJ跳过SSL证书验证

`byteDance.js`

```javascript
function patch(address) {
    Memory.protect(address, 4, 'rwx');
    Memory.writeByteArray(address, [0x00, 0x00, 0x80, 0x52]);
}

// function onLoad(name, callback) {
//     var Runtime = Java.use('java.lang.Runtime');
//     var System = Java.use('java.lang.System');
//     var VMStack = Java.use('dalvik.system.VMStack');
//     var VERSION = Java.use('android.os.Build$VERSION');
//     System.loadLibrary.overload('java.lang.String').implementation = function (libName) {
//         if (VERSION.SDK_INT.value >= 29) {
//             Runtime.getRuntime().loadLibrary0(Java.use('sun.reflect.Reflection').getCallerClass(), libName);
//         } else if (VERSION.SDK_INT.value >= 24) {
//             Runtime.getRuntime().loadLibrary0(VMStack.getCallingClassLoader(), libName);
//         } else {
//             Runtime.getRuntime().loadLibrary(libName, VMStack.getCallingClassLoader());
//         }
//         if (libName.includes(name)) {
//             callback();//无法执行到这里
//         }
//     };
// }

//参考: https://www.jianshu.com/p/4291ee42c412
function onLoad(name, callback) {
    //void* android_dlopen_ext(const char* filename, int flag, const android_dlextinfo* extinfo);//原型
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
        //28.4.0
        const soName = 'libsscronet.so';
        //方法1, 内存搜索
        // onLoad(soName, function () {
        //     let libsscronet = Process.getModuleByName(soName);
        //     const verifyCertMatches = Memory.scanSync(libsscronet.base, libsscronet.size, "E0 E3 00 91 C1 14 80 12");
        //     verifyCertMatches.forEach(function (result) {
        //         let verifyCert = result.address.add(0xC);
        //         if (Instruction.parse(verifyCert).toString() === "mov w0, #1") {
        //             // 设置可读可写可执行
        //             Memory.protect(verifyCert, 4, 'rwx');
        //             // 修改为 mov w0, #0
        //             Memory.writeByteArray(verifyCert, [0x00, 0x00, 0x80, 0x52]);
        //         }
        //
        //         let handleVerifyInstruction = Instruction.parse(result.address.add(0x1A4));
        //         if (Instruction.parse(result.address.add(0x1A0)).toString() === "mov x0, x19" && handleVerifyInstruction.mnemonic === "bl") {
        //             let handleVerifyResult = new NativePointer(handleVerifyInstruction.opStr.replace('#', ''));
        //             Interceptor.attach(handleVerifyResult, {
        //                 onLeave: function (retval) {
        //                     if (retval > 0x0) retval.replace(0x0);
        //                 }
        //             });
        //         }
        //     });
        // });

        //方法2, 直接patch
        // onLoad(soName, function () {
        //     let libsscronet = Module.getBaseAddress(soName);
        //     let verifyCert = libsscronet.add(0x3700F0);
        //     let handleVerifyResult1 = libsscronet.add(0x370448);
        //     let handleVerifyResult2 = libsscronet.add(0x370494);
        //     console.log("修改前: " + Instruction.parse(verifyCert), Instruction.parse(handleVerifyResult1), Instruction.parse(handleVerifyResult2));
        //     patch(verifyCert);
        //     patch(handleVerifyResult1);
        //     patch(handleVerifyResult2);
        //     console.log("修改后: " + Instruction.parse(verifyCert), Instruction.parse(handleVerifyResult1), Instruction.parse(handleVerifyResult2));
        // })


        //方法3, hook SSL_CTX_set_custom_verify, 基本通杀
        onLoad(soName, () => {
            // void SSL_CTX_set_custom_verify(SSL_CTX *ctx, int mode, enum ssl_verify_result_t (*callback)(SSL *ssl, uint8_t *out_alert)) {
            //     ctx->verify_mode = mode;
            //     ctx->custom_verify_callback = callback;
            // }//原型
            let SSL_CTX_set_custom_verify = Module.getExportByName(soName, 'SSL_CTX_set_custom_verify');
            if (SSL_CTX_set_custom_verify != null) {
                Interceptor.attach(SSL_CTX_set_custom_verify, {
                    onEnter: function (args) {
                        Interceptor.attach(args[2], {
                            onLeave: function (retval) {
                                // enum ssl_verify_result_t BORINGSSL_ENUM_INT {
                                //     ssl_verify_ok,
                                //     ssl_verify_invalid,
                                //     ssl_verify_retry,
                                // };
                                //全部替换成 ssl_verify_ok
                                if (retval > 0x0) retval.replace(0x0);
                            }
                        });
                    }
                });
            }
        });

        //只需要选择其中一种即可, 推荐使用方法3
    });
}

setImmediate(main);
// setTimeout(main, 10000);
// frida -U -f com.ss.android.ugc.aweme -l Android/byteDance.js
```

