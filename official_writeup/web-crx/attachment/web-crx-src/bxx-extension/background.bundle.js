function n(t) {
    window.dispatchEvent(new CustomEvent("sendDataToContentScript", {
        detail: t,
    }));
}

chrome.runtime.onInstalled.addListener((function(t){
    "install"===t.reason && chrome.tabs.create({url: "chrome://newtab"})
}));

chrome.runtime.onMessage.addListener(async (e, o, i) => {
    if("imgUrl2Base64_send" === e.action) {
        var a = e.message;
        var c;
        try {
            c = await fetch(a || "");
        } catch(c) {
            throw new Error("Could not fetch ".concat(a, ", status: ").concat(c.status));
        }
        var u = await c.blob();
        var s;
        (s = new FileReader).onloadend = function() {
            chrome.tabs.query({
                active: !0,
                currentWindow: !0,
            }, (function(t) {
                var r;
                chrome.scripting.executeScript({
                    target: {
                        tabId: null == t || null === (r = t[0]) || void 0 === r ? void 0 : r.id,
                    },
                    func: n,
                    args: [{
                        action: "imgUrl2Base64_received",
                        message: "".concat(s.result),
                    }],
                });
            }));
        };
        s.onerror = function() {};
        s.readAsDataURL(u);
    }
});