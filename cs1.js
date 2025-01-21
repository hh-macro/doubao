Java.perform(function() {
    var X509TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    var SSLContext = Java.use('javax.net.ssl.SSLContext');

    X509TrustManager.prototype.checkServerTrusted = function(chain, authType) {
        // 直接返回，不进行证书校验
        console.log('checkServerTrusted绕过');
    };

    X509TrustManager.prototype.checkClientTrusted = function(chain, authType) {
        // 直接返回，不进行证书校验
        console.log('checkClientTrusted绕过');
    };

    SSLContext.getInstance.overload('java.lang.String').implementation = function(protocol) {
        var context = this.getInstance(protocol);
        var trustManagers = [Java.cast(X509TrustManager.$new(), X509TrustManager)];
        context.init(null, trustManagers, null);
        return context;
    };
});