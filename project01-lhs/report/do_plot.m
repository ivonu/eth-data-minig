%% get rid of some stuff

clear all;
close all;

%% parameters
s = [0:0.001:1];
r = 16;
b = 16;

y = 1 - (1 - s.^r).^b;

%% plots

plot(s,y); 
hold on; 
line([0.85,0.85],[1,0]);
