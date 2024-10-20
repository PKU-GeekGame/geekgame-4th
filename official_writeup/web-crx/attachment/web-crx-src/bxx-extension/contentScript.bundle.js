var styles = [
    ".index-module__imgSearch_LeftWrapper--FI5NY {\n  position: fixed;\n  top: 0;\n  left: 0;\n  width: 100vw;\n  height: 100vh;\n\n  background-color: rgba(0, 0, 0, 0.6);\n\n  user-select: none;\n  z-index: 9999999;\n}\n\n.index-module__imgSearch_leftLayout--M7lpu {\n  position: fixed;\n  left: 0;\n  top: 0;\n\n  width: 80vw;\n  height: 100vh;\n  min-width: 725px;\n\n  background-color: #fff;\n\n  animation: index-module__leftLayOut_in--iKtHF 0.2s ease-in-out forwards;\n}\n\n.index-module__imgSearch_leftLayout_delete_icon--dOTH_ {\n  width: 15px;\n  height: 15px;\n}\n\n.index-module__imgSearch_leftLayout_iframe--exsY5 {\n  border: none;\n}\n\n.index-module__closeIconWrapper--fA3Su {\n  position: absolute;\n  right: 28px;\n  top: 34px;\n\n  width: 32px;\n  height: 32px;\n\n  display: flex;\n  justify-content: center;\n  align-items: center;\n\n  border-radius: 8px;\n\n  cursor: pointer;\n}\n\n.index-module__closeIconWrapper--fA3Su:hover {\n  background-color: #f5f5f5;\n}\n\n@keyframes index-module__leftLayOut_in--iKtHF {\n  0% {\n    left: -80vw;\n  }\n\n  100% {\n    left: 0;\n  }\n}\n",
    ".index-module__imgSearch_wrapper--GU1Ct {\n  position: absolute;\n  right: 0;\n  top: 0;\n\n  user-select: none;\n\n  cursor: pointer;\n\n  z-index: 9999999;\n}\n\n#index-module__chrome_pc_imgSearch_leftWrapper--qzAdT {\n  z-index: 999999;\n}\n\n#index-module__chrome_pc_imgSearch_hoverWrapper--dLYdy {\n  z-index: 99999;\n}\n\n.index-module__imgSearch_hover_content--c5JEb:hover .index-module__imgSearch_hover_rightWrapper--VZGcY {\n  display: flex;\n}\n\n.index-module__imgSearch_hover_content--c5JEb {\n  box-sizing: border-box;\n\n  transition: width 1s ease-in-out;\n\n  position: absolute;\n  top: 0;\n  right: 0;\n  min-width: 30px;\n  width: fit-content;\n  height: 30px;\n\n  background-color: rgba(0, 0, 0, 0.4);\n  border-radius: 8px;\n\n  display: flex;\n  flex-direction: row;\n  justify-content: flex-start;\n  align-items: center;\n\n  color: #fff;\n\n  padding: 6px;\n\n  display: none;\n\n  cursor: pointer;\n\n  z-index: 999999;\n}\n\n.index-module__imgSearch_hover_rightWrapper--VZGcY {\n  display: none;\n  flex-direction: row;\n  justify-content: center;\n  align-items: center;\n}\n\n.index-module__imgSearch_hover_content_text--WI0by {\n  font-family: PingFang SC;\n  font-size: 14px;\n  font-weight: normal;\n  line-height: 22px;\n  display: flex;\n  align-items: center;\n  letter-spacing: 0em;\n\n  margin-left: 4px;\n  margin-right: 2px;\n\n  white-space: nowrap;\n}\n\n.index-module__imgSearch_hover_content_img--_E1cK {\n  width: 16px;\n  height: 16px;\n\n  margin-left: 1px;\n}\n\n.index-module__imgSearch_hover_arrow_img--iv06Y {\n  width: 8px;\n  height: 8px;\n}\n\n.index-module__closeDivider--Tq8VM {\n  width: 1px;\n  height: 20px;\n  background-color: #fff;\n\n  margin-left: 4px;\n  margin-right: 9px;\n\n  pointer-events: none;\n}\n\n.index-module__close_img--vANVl {\n  margin-right: 4px;\n}\n\n.index-module__close_img--vANVl path {\n  fill: #fff;\n}\n",
].join();

var style = document.createElement('style');
style.textContent = styles;
document.head.append(style);

var Hw = !1, Bw = !1;

var Ww = {
    hoverRef: null,
    leftRef: null,
    setLeftVisibility: null,
    limitWidth: 100,
    limitHeight: 100,
    lastImgDom: null,
};

var zw = function(e, t, n) {
    if(n || 2 === arguments.length)
        for(var r, o = 0, a = t.length; o < a; o++)
            !r && o in t || (r || (r = Array.prototype.slice.call(t, 0, o)),
                r[o] = t[o]);
    return e.concat(r || Array.prototype.slice.call(t))
};

var S = function(e, t) {
    if (t && 0 !== t.length || (t = []),
    e && e.length > 0)
        for (var n = 0; n < e.length; n++)
            t.push(e[n]);
    return t
};

function Kw(e) {
    if(!e)
        return [];
    try {
        for(var t = [], n = 0; n < e.children.length; n++) {
            var r = e.children[n];
            t.push.apply(t, Kw(r)),
            t.push(r)
        }
        return t
    } catch(e) {
        return []
    }
}

function handle_mousemove(e, t) {
    var n, r, o, a, i, l, u, c, s = e;
    if(!(null == s ? void 0 : s.className) || -1 === (null === (r = null === (n = null == s ? void 0 : s.className) || void 0 === n ? void 0 : n.indexOf) || void 0 === r ? void 0 : r.call(n, "imgSearch_hover"))) {
        for(var f, d = [], p = ["script", "iframe", "button", "video"], m = 0, h = zw([], Kw((null == s ? void 0 : s.parentElement) || null) || [], !0); m < h.length; m++) {
            var v = h[m];
            (null == v ? void 0 : v.tagName) && p.includes("".concat(v.tagName).toLowerCase()) || ("img" === v.tagName.toLowerCase() || v.src || (null === (a = null == v ? void 0 : v.style) || void 0 === a ? void 0 : a.backgroundImage) && "none" !== v.style.backgroundImage && -1 !== v.style.backgroundImage.indexOf("url")) && d.push(v)
        }
        if(d = d.filter((function(e) {
                var t, n, r, o;
                return Number("".concat((null === (n = null === (t = null == e ? void 0 : e.getBoundingClientRect) || void 0 === t ? void 0 : t.call(e)) || void 0 === n ? void 0 : n.height) || 0)) > (null == Ww ? void 0 : Ww.limitHeight) && Number("".concat((null === (o = null === (r = null == e ? void 0 : e.getBoundingClientRect) || void 0 === r ? void 0 : r.call(e)) || void 0 === o ? void 0 : o.width) || 0)) > (null == Ww ? void 0 : Ww.limitWidth)
            }
        )),
            d = d.filter((function(e) {
                    return function(e, t) {
                        var n;
                        try {
                            if(!e)
                                return !1;
                            var r = window.getComputedStyle(e);
                            if("none" === r.getPropertyValue("display"))
                                return !1;
                            if("hidden" === r.getPropertyValue("visibility"))
                                return !1;
                            if("0" === r.getPropertyValue("opacity"))
                                return !1;
                            var o = null === (n = null == e ? void 0 : e.getBoundingClientRect) || void 0 === n ? void 0 : n.call(e);
                            return !!o && t.clientX >= o.left && t.clientX <= o.right && t.clientY >= o.top && t.clientY <= o.bottom
                        } catch(e) {
                            return !1
                        }
                    }(e, t)
                }
            )),
        (null == d ? void 0 : d[0]) && (null === (i = null == Ww ? void 0 : Ww.hoverRef) || void 0 === i ? void 0 : i.current)) {
            Ww.lastImgDom = null == d ? void 0 : d[0];
            var g = null === (l = null == d ? void 0 : d[0]) || void 0 === l ? void 0 : l.getBoundingClientRect()
                , y = null === (u = null == Ww ? void 0 : Ww.hoverRef) || void 0 === u ? void 0 : u.current;
            if(!g || !y)
                return;
            var b = window.innerWidth - (g.left + window.scrollX + g.width + (f = 4,
                devicePixelRatio ? f * devicePixelRatio : f)) || 0;
            y.style.right = "".concat(b && b > 0 ? b : 0, "px"),
                y.style.top = "".concat(g.top + window.scrollY + 8, "px"),
                y.style.display = "flex"
        } else {
            (y = null === (c = null == Ww ? void 0 : Ww.hoverRef) || void 0 === c ? void 0 : c.current) && (y.style.display = "none")
        }
        return d
    }
    (null === (o = null == Ww ? void 0 : Ww.hoverRef) || void 0 === o ? void 0 : o.current) && (Ww.hoverRef.current.style.display = "flex")
}

function render_hover_element(root) {
    root.innerHTML = '<div class="index-module__imgSearch_hover_content--c5JEb" style="display: none;"><svg class="index-module__imgSearch_hover_content_img--_E1cK" xmlns="http://www.w3.org/2000/svg" fill="#FFFFFF" version="1.1" width="11.07000732421875" height="11.070037841796875" viewBox="0 0 11.07000732421875 11.070037841796875"><g><g><path d="M6.39323,-0.000003230701660156248Q6.56807,-0.000003230701660156248,6.63304,0.004581083298339844Q7.59821,0.07268939329833984,8.09077,0.9055101932983398Q8.12393,0.9615741932983398,8.20212,1.1179571932983399L8.35363,1.4209871932983398Q8.56041,1.4241671932983397,8.64865,1.4331271932983398Q9.60102,1.5298471932983397,10.2802,2.20902719329834Q10.9594,2.88819719329834,11.0561,3.8405771932983397Q11.07,3.97747719329834,11.07,4.39960719329834L11.07,6.85908719329834C11.07,7.09422719329834,10.8794,7.28485719329834,10.6442,7.28485719329834C10.4091,7.28485719329834,10.2185,7.09422719329834,10.2185,6.85908719329834L10.2185,4.39960719329834Q10.2185,4.0205971932983395,10.2089,3.9266071932983397Q10.1428,3.2759171932983397,9.67807,2.8111571932983397Q9.21331,2.3463971932983396,8.56262,2.2803071932983396Q8.46863,2.2707671932983398,8.08961,2.2707671932983398C7.92835,2.2707671932983398,7.78092,2.1796471932983397,7.7088,2.0354071932983397L7.44048,1.4987771932983398Q7.37571,1.3692271932983398,7.35782,1.3389971932983398Q7.09267,0.8906711932983399,6.5731,0.8540071932983399Q6.53807,0.8515351932983398,6.39323,0.8515351932983398L4.67677,0.8515351932983398Q4.53193,0.8515351932983398,4.4969,0.8540071932983399Q3.97733,0.8906711932983399,3.71217,1.3389971932983398Q3.69429,1.3692271932983398,3.62952,1.4987771932983398L3.3612,2.0354071932983397C3.28908,2.1796471932983397,3.14165,2.2707671932983398,2.98038,2.2707671932983398Q2.60137,2.2707671932983398,2.50738,2.2803071932983396Q1.85669,2.3463971932983396,1.39193,2.8111571932983397Q0.927165,3.2759171932983397,0.861083,3.9266071932983397Q0.851538,4.0205971932983395,0.851538,4.39960719329834L0.851538,8.08961719329834Q0.851538,8.46862719329834,0.861083,8.56261719329834Q0.927165,9.21330719329834,1.39193,9.67806719329834Q1.85669,10.14283719329834,2.50738,10.20893719329834Q2.60137,10.21843719329834,2.98038,10.21843719329834L6.89406,10.21843719329834C7.1292,10.21843719329834,7.31983,10.40903719329834,7.31983,10.64423719329834C7.31983,10.87933719329834,7.1292,11.07003719329834,6.89406,11.07003719329834L2.98038,11.07003719329834Q2.55825,11.07003719329834,2.42135,11.05613719329834Q1.46897,10.95933719329834,0.789798,10.28023719329834Q0.110621,9.60101719329834,0.0139025,8.64864719329834Q0,8.51175719329834,0,8.08961719329834L0,4.39960719329834Q0,3.97746719329834,0.0139022,3.8405771932983397Q0.110621,2.88819719329834,0.789798,2.20902719329834Q1.46897,1.5298471932983397,2.42135,1.4331271932983398Q2.50959,1.4241671932983397,2.71637,1.4209871932983398L2.86788,1.1179571932983399Q2.94607,0.9615661932983398,2.97923,0.9055081932983399Q3.47179,0.07268919329833984,4.43696,0.004581193298339844Q4.50193,-0.000003230701660156248,4.67677,-0.000003230701660156248L6.39323,-0.000003230701660156248ZM7.24108,7.52484719329834Q7.94774,6.81818719329834,7.94774,5.81881719329834Q7.94774,4.81944719329834,7.24108,4.11278719329834Q6.53441,3.4061271932983397,5.53505,3.4061271932983397Q4.53568,3.4061271932983397,3.82901,4.11278719329834Q3.12235,4.81944719329834,3.12235,5.81881719329834Q3.12235,6.81818719329834,3.82901,7.52484719329834Q4.53568,8.23150719329834,5.53505,8.23150719329834Q6.53441,8.23150719329834,7.24108,7.52484719329834ZM6.63895,4.71491719329834Q7.0962,5.17216719329834,7.0962,5.81881719329834Q7.0962,6.465467193298339,6.63895,6.92271719329834Q6.1817,7.37997719329834,5.53505,7.37997719329834Q4.88839,7.37997719329834,4.43114,6.92271719329834Q3.97389,6.465467193298339,3.97389,5.81881719329834Q3.97389,5.17216719329834,4.43114,4.71491719329834Q4.88839,4.25766719329834,5.53505,4.25766719329834Q6.1817,4.25766719329834,6.63895,4.71491719329834Z" fill-rule="evenodd" fill="#FFFFFF" fill-opacity="1"></path></g><g><path d="M9.674183976135254,10.006227403259278Q9.486503976135253,10.153287403259277,9.261133976135254,10.231067403259278Q9.035753976135254,10.308857403259278,8.797343976135254,10.308857403259278Q8.727493976135253,10.308857403259278,8.657983976135254,10.302007403259278Q8.588463976135253,10.295157403259278,8.519953976135254,10.281527403259277Q8.451443976135254,10.267897403259276,8.384603976135255,10.247617403259277Q8.317754976135253,10.227327403259277,8.253219976135254,10.200587403259277Q8.188684976135255,10.173857403259277,8.127080976135254,10.140917403259277Q8.065476976135255,10.107977403259277,8.007396976135254,10.069167403259277Q7.949316976135254,10.030347403259277,7.895319976135254,9.986017403259277Q7.841323976135254,9.941697403259278,7.791930976135254,9.892287403259278Q7.742537976135254,9.842887403259278,7.698223976135254,9.788877403259278Q7.653910976135254,9.734867403259278,7.615102976135254,9.676767403259277Q7.576294976135254,9.618677403259277,7.543366976135254,9.557057403259277Q7.510438976135254,9.495437403259277,7.483707976135254,9.430877403259277Q7.456976376135254,9.366327403259277,7.436699376135254,9.299467403259278Q7.416422376135254,9.232607403259276,7.402794876135254,9.164077403259277Q7.389167376135254,9.095557403259278,7.3823206861352535,9.026017403259278Q7.375473976135254,8.956487403259278,7.375473976135254,8.886617403259278Q7.375473976135254,8.816747403259278,7.3823206861352535,8.747207403259278Q7.389167376135254,8.677677403259278,7.402794876135254,8.609147403259277Q7.416422376135254,8.540627403259277,7.436699376135254,8.473757403259278Q7.456976376135254,8.406900403259277,7.483707976135254,8.342348403259278Q7.510438976135254,8.277797403259278,7.543366976135254,8.216177403259277Q7.576294976135254,8.154557403259277,7.615102976135254,8.096462403259277Q7.653910976135254,8.038367403259278,7.698223976135254,7.984357403259278Q7.742537976135254,7.930346403259278,7.791930976135254,7.8809414032592775Q7.841323976135254,7.831535403259277,7.895319976135254,7.7872104032592775Q7.949316976135254,7.742885403259278,8.007396976135254,7.704067403259278Q8.065476976135255,7.665250403259277,8.127080976135254,7.632313403259277Q8.188684976135255,7.599377403259277,8.253219976135254,7.572638403259277Q8.317754976135253,7.545900703259277,8.384603976135255,7.5256185032592775Q8.451443976135254,7.505336303259277,8.519953976135254,7.491705303259278Q8.588463976135253,7.478074303259278,8.657983976135254,7.471225863259277Q8.727493976135253,7.464377403259277,8.797343976135254,7.464377403259277Q8.867203976135254,7.464377403259277,8.936713976135254,7.471225863259277Q9.006233976135254,7.478074303259278,9.074743976135254,7.491705303259278Q9.143253976135254,7.505336303259277,9.210093976135253,7.5256185032592775Q9.276933976135254,7.545900703259277,9.341473976135253,7.572638403259277Q9.406013976135254,7.599377403259277,9.467613976135254,7.632313403259277Q9.529213976135253,7.665250403259277,9.587293976135253,7.704067403259278Q9.645373976135254,7.742885403259278,9.699373976135254,7.7872104032592775Q9.753373976135254,7.831535403259277,9.802763976135253,7.8809414032592775Q9.852153976135254,7.930346403259278,9.896473976135255,7.984357403259278Q9.940783976135254,8.038367403259278,9.979593976135254,8.096462403259277Q10.018393976135254,8.154557403259277,10.051323976135254,8.216177403259277Q10.084253976135255,8.277797403259278,10.110983976135254,8.342348403259278Q10.137713976135254,8.406900403259277,10.157993976135254,8.473757403259278Q10.178273976135253,8.540627403259277,10.191893976135255,8.609147403259277Q10.205523976135254,8.677677403259278,10.212373976135254,8.747207403259278Q10.219223976135254,8.816747403259278,10.219223976135254,8.886617403259278Q10.219223976135254,9.085697403259278,10.164573976135253,9.277127403259277Q10.109923976135253,9.468557403259277,10.004823976135254,9.637617403259277C10.018013976135254,9.646497403259277,10.030553976135254,9.656777403259277,10.042213976135255,9.668447403259277L10.886653976135253,10.513097403259277C10.984263976135253,10.610737403259277,10.984263976135253,10.769047403259277,10.886653976135253,10.866687403259277C10.789033976135254,10.964337403259277,10.630763976135254,10.964337403259277,10.533143976135253,10.866687403259277L9.688713976135254,10.022047403259277C9.683603976135254,10.016927403259277,9.678753976135255,10.011657403259278,9.674183976135254,10.006227403259278ZM9.619223976135254,8.886617403259278Q9.619223976135254,8.545987403259277,9.378443976135253,8.305151403259277Q9.137733976135253,8.064377403259277,8.797343976135254,8.064377403259277Q8.456963976135254,8.064377403259277,8.216248976135255,8.305151403259277Q7.9754739761352536,8.545987403259277,7.9754739761352536,8.886617403259278Q7.9754739761352536,9.227247403259277,8.216248976135255,9.468077403259278Q8.456963976135254,9.708857403259277,8.797343976135254,9.708857403259277Q9.137733976135253,9.708857403259277,9.378443976135253,9.468077403259278Q9.619223976135254,9.227247403259277,9.619223976135254,8.886617403259278Z" fill-rule="evenodd" fill="#FFFFFF" fill-opacity="1"></path></g></g></svg><div class="index-module__imgSearch_hover_rightWrapper--VZGcY"><div class="index-module__imgSearch_hover_content_text--WI0by">并夕夕同款</div><svg class="index-module__imgSearch_hover_arrow_img--iv06Y" xmlns="http://www.w3.org/2000/svg" fill="#FFFFFF" version="1.1" width="8" height="8" viewBox="0 0 8 8"><g><g><path d="M3.353613,0.646506L6.35355,3.64645Q6.4238800000000005,3.71677,6.46194,3.80866Q6.5,3.90054,6.5,4Q6.5,4.0994600000000005,6.46194,4.19134Q6.4238800000000005,4.28323,6.35355,4.35355L3.353741,7.35337L3.353553,7.35355Q3.283227,7.42388,3.191342,7.46194Q3.0994562,7.5,3,7.5Q2.9507543,7.5,2.9024549,7.49039Q2.854155,7.48078,2.808658,7.46194Q2.763161,7.44309,2.722215,7.41573Q2.681269,7.38837,2.646447,7.35355Q2.611625,7.31873,2.584265,7.27778Q2.556906,7.23684,2.5380599999999998,7.19134Q2.519215,7.14584,2.509607,7.09755Q2.5,7.04925,2.5,7Q2.5,6.90054,2.5380599999999998,6.80866Q2.57612,6.71677,2.646447,6.64645L2.646634,6.64626L5.29289,4L2.646506,1.353613L2.646447,1.353553Q2.57612,1.2832270000000001,2.5380599999999998,1.1913420000000001Q2.5,1.0994562,2.5,1Q2.5,0.9507543,2.509607,0.9024549Q2.519215,0.854155,2.5380599999999998,0.808658Q2.556906,0.763161,2.584265,0.722215Q2.611625,0.681269,2.646447,0.646447Q2.681269,0.611625,2.722215,0.584265Q2.763161,0.556906,2.808658,0.53806Q2.854155,0.519215,2.9024549,0.5096069999999999Q2.9507543,0.5,3,0.5Q3.0994562,0.5,3.191342,0.53806Q3.283227,0.57612,3.353553,0.646447L3.353613,0.646506Z" fill-rule="evenodd" fill="#FFFFFF" fill-opacity="1"></path></g></g></svg><div class="index-module__closeDivider--Tq8VM"></div><svg class="index-module__close_img--vANVl" xmlns="http://www.w3.org/2000/svg" fill="#11192D" version="1.1" width="12" height="12" viewBox="0 0 15.21435546875 15.2142333984375"><g><path d="M7.60714,8.6678L13.934,14.9946C14.0746,15.1353,14.2654,15.2143,14.4643,15.2143C14.4763,15.2143,14.4883,15.214,14.5003,15.2134C14.6866,15.2045,14.8628,15.1265,14.9946,14.9946C15.1353,14.854,15.2143,14.6632,15.2143,14.4643C15.2143,14.2654,15.1353,14.0746,14.9946,13.934L8.6678,7.60714L14.9946,1.28033C15.1353,1.13968,15.2143,0.948912,15.2143,0.75C15.2143,0.551088,15.1353,0.360322,14.9946,0.21967C14.854,0.0790178,14.6632,0,14.4643,0C14.4513,0,14.4384,0.000334995,14.4255,0.00100463C14.2402,0.0106023,14.0651,0.0885066,13.9336,0.220021L7.60714,6.54648L1.28033,0.21967C1.13968,0.0790176,0.948912,0,0.75,0C0.551088,0,0.360322,0.0790176,0.21967,0.21967C0.0790176,0.360322,0,0.551088,0,0.75C0,0.948912,0.0790176,1.13968,0.21967,1.28033L6.54648,7.60714L0.21967,13.934C0.0790176,14.0746,0,14.2654,0,14.4643C0,14.6632,0.0790176,14.854,0.21967,14.9946C0.360322,15.1353,0.551088,15.2143,0.75,15.2143C0.948912,15.2143,1.13968,15.1353,1.28033,14.9946L7.60714,8.6678Z" fill-rule="evenodd" fill="#11192D" fill-opacity="1"></path></g></svg></div></div>';
    Ww.hoverRef = {current: root.querySelector('.index-module__imgSearch_hover_content--c5JEb')};
    Ww.hoverRef.current.onclick = ()=>{
        Bw || Hw || (Ww.setLeftVisibility && (null == Ww || Ww.setLeftVisibility(!0)));
    };
    root.querySelector('.index-module__close_img--vANVl').onclick = ()=>{
        var e;
        Bw = !0;
        var t = null === (e = null == Ww ? void 0 : Ww.hoverRef) || void 0 === e ? void 0 : e.current;
        t && (t.style.display = "none")
    };
}

function render_iframe_element(l) {
    let i = Ww;
    var s = {current: l.current};
    var c = function(e) {
        var t = (null == e ? void 0 : e.detail) || {};
        "imgUrl2Base64_received" === t.action && t.message && l.current && l.current.postMessage({img: t.message}, '*');
    };

    var f = function() {
        var e, t, n, o, a, l, u, c, s, f, d, p, m, h;
        try {
            if (!(e = null == i ? void 0 : i.lastImgDom))
                return;
            t = "",
            (null == e ? void 0 : e.srcset) ? (n = null == e ? void 0 : e.srcset,
            t = null === (u = null === (l = null === (a = null == n ? void 0 : n.split(",")) || void 0 === a ? void 0 : a[0]) || void 0 === l ? void 0 : l.split(" ")) || void 0 === u ? void 0 : u[0]) : (null == e ? void 0 : e.src) ? t = null == e ? void 0 : e.src : (o = null === (f = null === (s = null === (c = null === window || void 0 === window ? void 0 : window.getComputedStyle) || void 0 === c ? void 0 : c.call(window, e)) || void 0 === s ? void 0 : s.getPropertyValue) || void 0 === f ? void 0 : f.call(s, "background-image")) && (t = (null === (h = null === (m = null === (p = null === (d = null == o ? void 0 : o.match) || void 0 === d ? void 0 : d.call(o, /url\((.*?)\)/)) || void 0 === p ? void 0 : p[1]) || void 0 === m ? void 0 : m.replace) || void 0 === h ? void 0 : h.call(m, /['"]/g, "")) || ""),
            window._element = e,
            t.replace(/[&quot;|&apos;|\'|\"]/g, ""),
            (null == t ? void 0 : t.startsWith) && t.startsWith("//") && (t = "https:".concat(t)),
            function(e) {
                try {
                    chrome.runtime.sendMessage({
                        action: "imgUrl2Base64_send",
                        message: e
                    })
                } catch (e) {}
            }(t)
        } catch (e) {}
    };

    var d = function(e) {
        var t, n, r, o;
        (t = null === (n = null == s ? void 0 : s.current) || void 0 === n ? void 0 : n.contentWindow) ? chrome.runtime.getURL('/').startsWith(e.origin) ? (l.current = t, f()) : null : null;
    };

    window.addEventListener("sendDataToContentScript", c);
    window.addEventListener("message", d);

    l.current.src = chrome.runtime.getURL("iframe.html");

    return ()=>{ // iframe_cleanup
        window.removeEventListener("sendDataToContentScript", c);
        window.removeEventListener("message", d);
    };
}

function render_left_element(root, n) {
    var iframe_cleanup = null;
    Ww.setLeftVisibility = (new_state)=>{
        n = new_state;
        render_left_element(root, n);
        if(!new_state && iframe_cleanup)
            iframe_cleanup();
    };
    Hw = n;
    if(n) {
        root.innerHTML = '<div class="index-module__imgSearch_LeftWrapper--FI5NY" style="display: block;"><div class="index-module__imgSearch_leftLayout--M7lpu"><div class="index-module__closeIconWrapper--fA3Su"><svg class="index-module__imgSearch_leftLayout_delete_icon--dOTH_" xmlns="http://www.w3.org/2000/svg" fill="#11192D" version="1.1" width="15.21435546875" height="15.21435546875" viewBox="0 0 15.21435546875 15.2142333984375"><g><path d="M7.60714,8.6678L13.934,14.9946C14.0746,15.1353,14.2654,15.2143,14.4643,15.2143C14.4763,15.2143,14.4883,15.214,14.5003,15.2134C14.6866,15.2045,14.8628,15.1265,14.9946,14.9946C15.1353,14.854,15.2143,14.6632,15.2143,14.4643C15.2143,14.2654,15.1353,14.0746,14.9946,13.934L8.6678,7.60714L14.9946,1.28033C15.1353,1.13968,15.2143,0.948912,15.2143,0.75C15.2143,0.551088,15.1353,0.360322,14.9946,0.21967C14.854,0.0790178,14.6632,0,14.4643,0C14.4513,0,14.4384,0.000334995,14.4255,0.00100463C14.2402,0.0106023,14.0651,0.0885066,13.9336,0.220021L7.60714,6.54648L1.28033,0.21967C1.13968,0.0790176,0.948912,0,0.75,0C0.551088,0,0.360322,0.0790176,0.21967,0.21967C0.0790176,0.360322,0,0.551088,0,0.75C0,0.948912,0.0790176,1.13968,0.21967,1.28033L6.54648,7.60714L0.21967,13.934C0.0790176,14.0746,0,14.2654,0,14.4643C0,14.6632,0.0790176,14.854,0.21967,14.9946C0.360322,15.1353,0.551088,15.2143,0.75,15.2143C0.948912,15.2143,1.13968,15.1353,1.28033,14.9946L7.60714,8.6678Z" fill-rule="evenodd" fill="#11192D" fill-opacity="1"></path></g></svg></div><iframe class="index-module__imgSearch_leftLayout_iframe--exsY5" title="imgSearch_mini" width="100%" height="100%"></iframe></div></div>';
        Ww.leftRef = {current: root.querySelector('.index-module__imgSearch_leftLayout--M7lpu')};
        root.querySelector('.index-module__closeIconWrapper--fA3Su').onclick = ()=>{
            var e, t;
            (null === (t = null === (e = Ww.leftRef) || void 0 === e ? void 0 : e.current) || void 0 === t ? void 0 : t.parentNode) && Ww.setLeftVisibility && (null == Ww || Ww.setLeftVisibility(!1))
        };
        iframe_cleanup = render_iframe_element({current: root.querySelector('iframe')});
    } else {
        root.innerHTML = '';
    }
}

function main() {
    var t;
    try {
        t = document.createElement("div");
        t.className = "index-module__imgSearch_wrapper--GU1Ct",
        t.id = "chrome_pc_imgSearch_hoverWrapper",
        document.body.appendChild(t),
        render_hover_element(t);
    } catch(e) {}
    try {
        t = document.createElement("div");
        t.id = "chrome_pc_imgSearch_leftWrapper",
        document.body.appendChild(t),
        render_left_element(t, !1);
    } catch(e) {}
    document.addEventListener("mousemove", (e) => {
        if ((null == e ? void 0 : e.target) && !Hw && !Bw) {
            try {
                handle_mousemove(null == e ? void 0 : e.target, e)
            } catch(e) {
                console.log("handleMouseMove", e)
            }
        }
    });
}

main();
console.log('BXX HELPER: content script running');
