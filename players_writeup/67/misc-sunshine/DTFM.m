[data,fs] = audioread("DECRYPT_CLIP.wav");
[p,f,t] = pspectrum(data(:,1),fs,'spectrogram',"TimeResolution",0.05,"FrequencyLimits",[0,2048],'Leakage',0.25);
fp = zeros(length(t),2);
for i = 1:length(t)
    [pks,locs] = findpeaks(p(:,i));
    if length(pks) == 2
        fp(i,1) = f(locs(1));
        fp(i,2) = f(locs(2));
        if fp(i,1) > fp(i,2)
            fp(i,1) = f(locs(2));
            fp(i,2) = f(locs(1));
        end
    end
end

pspectrum(data(:,1),fs,'spectrogram',"TimeResolution",0.05,"FrequencyLimits",[0,2048],'Leakage',0.25);
hold on;
yline([697,770,852,941]/1000,"k","LineWidth",1);
yline([1209,1336,1477,1633]/1000,"k","LineWidth",1);
plot(t,fp(:,2)/1000,"r","LineWidth",2);
plot(t,fp(:,1)/1000,"b","LineWidth",4);
xlim([1.4,4]);

% flag{2825628257282931}