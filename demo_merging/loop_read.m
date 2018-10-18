function [ pc ] = loop_read(model_name)
% Input : model_name , string
% Output: Point Cloud object

fprintf(' \n *** Reading ply file...');
model_filename = strcat(model_name, '.ply');
[~, PTS, ~, ~] = plyread(model_filename, 'face');
pc = pointCloud(PTS);
figure
pcshow(pc);
fprintf('...DONE\n');

end

