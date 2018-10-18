function [ pc ] = loop_read(model_name)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

model_filename = strcat(model_name, '.ply');
[~, PTS, ~, ~] = plyread(model_filename, 'face');
pc = pointCloud(PTS);
figure
pcshow(pc);
fprintf('*** Reading ply file \n');

end

