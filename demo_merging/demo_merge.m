%% HiPEDS Group Project 2018
% A naive script for reading ply files, denoise and merge
% Purpose of this script is the volume calculation of 3d area
% scanned from an IntelReal Sense Camera
% TODO : PARAMETRIZATION 
%
% 
% Last upd 18/10/18
%

%% CLEAR ALL

clear; close all; clc;
fprintf('\n *** Starting %s ... ***  \n', mfilename);

rmpath(genpath('input_data')); % Remove Path of pic plys
addpath('input_data/10/10_1/10_1_2'); % Add only experiment path
addpath('output_data/');
addpath('./');
addpath('.');


display = 1; % Boolean for display images of plys

%% READ PLY FILES

fprintf('\n *** Reading ply file .');

% Model names as of Intel Real Sense camera
model0 = 'pic_0';
model1 = 'pic_1';
model2 = 'pic_2';
model3 = 'pic_3';


[pc0]=loop_read(model0);
[pc1]=loop_read(model1);
[pc2]=loop_read(model2);
[pc3]=loop_read(model3);

%% Point cloud denoising
close all;
%nn = 30;
%thres = 0.5;
fprintf('\n *** Denoising...');

[ pc0 ] = hard_denoise( pc0 );
[ pc1 ] = hard_denoise( pc1 );
[ pc2 ] = hard_denoise( pc2 );
[ pc3 ] = hard_denoise( pc3 );

if(display)
figure
pcshow(pc0);
figure
pcshow(pc1);
figure
pcshow(pc2);
figure
pcshow(pc3);
end

fprintf(' ...DONE*** \n');

%% Merging

gridSize = 0.01;
mergeSize = 0.015;

fprintf('\n *** Merging 1...');% Merge 0-1

fixed = pcdownsample(pc0, 'gridAverage', gridSize);
moving = pcdownsample(pc1, 'gridAverage', gridSize);
tform = pcregrigid(moving, fixed, 'Metric', 'pointToPlane', 'Extrapolate', true);
ptCloudAligned = pctransform(pc1, tform);

ptCloudScene01 = pcmerge(pc0, ptCloudAligned, mergeSize);
fprintf(' ...DONE*** \n');

fprintf('\n *** Merging 2...'); % Merge 2-3
fixed = pcdownsample(pc2, 'gridAverage', gridSize);
moving = pcdownsample(pc3, 'gridAverage', gridSize);
tform = pcregrigid(moving, fixed, 'Metric', 'pointToPlane', 'Extrapolate', true);
ptCloudAligned = pctransform(pc3, tform);

ptCloudScene23 = pcmerge(pc2, ptCloudAligned, mergeSize);
fprintf(' ...DONE*** \n');

%% Merge 01 - 23
close all;
drawnow;

fprintf('\n *** Merging 3...');
fixed = pcdownsample(ptCloudScene01, 'gridAverage', gridSize);
moving = pcdownsample(ptCloudScene23, 'gridAverage', gridSize);
tform = pcregrigid(moving, fixed, 'Metric', 'pointToPlane', 'Extrapolate', true);
ptCloudAligned = pctransform(ptCloudScene23, tform);

ptCloudScene0123 = pcmerge(ptCloudScene01, ptCloudAligned, mergeSize);
fprintf(' ...DONE*** \n');

%% 
fprintf('\n *** Denoise final .ply ...');
[ ptCloudScene0123 ] = hard_denoise( ptCloudScene0123);
fprintf(' ...DONE*** \n');

%% Visualize the input images.
figure
subplot(2, 2, 1)
pcshow(ptCloudScene01);
title('First input point cloud')
drawnow

subplot(2, 2, 3)
pcshow(ptCloudScene23);
title('Second input point cloud')
drawnow

% Visualize the world scene.
subplot(2, 2, [2, 4])
pcshow(ptCloudScene0123, 'VerticalAxis', 'Y', 'VerticalAxisDir', 'Down')
title('Merged point cloud scene')
xlabel('X (m)')
ylabel('Y (m)')
zlabel('Z (m)')
drawnow

DATA.vertex.x = ptCloudScene0123.Location(:, 1); % coordinate of normal, [Nx1] real array - x
DATA.vertex.y = ptCloudScene0123.Location(:, 2); % coordinate of normal, [Nx1] real array - y
DATA.vertex.z = ptCloudScene0123.Location(:, 3); % coordinate of normal, [Nx1] real array - z
x = DATA.vertex.x;
y = DATA.vertex.y;
z = DATA.vertex.z;

%% Export to ply
% fprintf('\n *** Writing ply file .');
% ply_write(DATA, 'output_data/merged.ply', 'binary_big_endian');
% fprintf(' ... DONE \n');

%% Normalize 
xadj = x - min(x);
yadj = y - min(y);
zadj = z - min(z);

F2 = scatteredInterpolant(x, y, zadj); % Interpolate
q1 = quad2d(@(x, y) F2(x, y), min(x), max(x), min(y), max(y), 'AbsTol', 0.01); % Integrate
toc;
%%
tv = 2.; % Total Volume
%fprintf('\n Free space is: %f', q1);
fprintf('\n Occupied space is (percentage) : %f', (tv-q1)/tv );

fprintf('\n End of execution \n');



%% Imperial College London
% HiPEDS PhD students
% October 2018
% In partnership with Royal Mail
