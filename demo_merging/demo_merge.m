%% HiPEDS Group Project 2018
% A naive script for reading ply files, denoise and merge
%
% TODO : PARAMETRIZATION 
%
%
% 11/10/18
%

%% CLEAR ALL

clear all;
close all; clc;
fprintf('\n *** Starting %s ... ***  \n', mfilename);
addpath('input_data/');
addpath('output_data/');
addpath('Power-Crust-MATLAB-master/');

addpath('./');
addpath('.');

%% READ PLY FILES
tic
fprintf('\n *** Reading ply file .');

% Model names as of Intel Real Sense camera
model0 = '40_0';
model1 = '40_1';
model2 = '40_2';
model3 = '40_3';

model_filename0 = strcat(model0, '.ply');
[~, PTS, ~, ~] = plyread(model_filename0, 'face');
pc0 = pointCloud(PTS);
figure
pcshow(pc0);
fprintf('*** Reading ply file \n');

model_filename1 = strcat(model1, '.ply');
[~, PTS, ~, ~] = plyread(model_filename1, 'face');
pc1 = pointCloud(PTS);
figure
pcshow(pc1);
fprintf(' *** Reading ply file \n');

model_filename2 = strcat(model2, '.ply');
[~, PTS, ~, ~] = plyread(model_filename2, 'face');
pc2 = pointCloud(PTS);
figure
pcshow(pc2);
fprintf(' *** Reading ply file \n');

model_filename3 = strcat(model3, '.ply');
[~, PTS, ~, ~] = plyread(model_filename3, 'face');
pc3 = pointCloud(PTS);
figure
pcshow(pc3);
fprintf(' *** Reading ply file \n');

%% Point cloud denoising
close all;
nn = 30;
thres = 0.5;
fprintf('\n *** Denoising...');

XYZ = pc0.Location;
XYZ((XYZ(:,1)< -0.5),:) = [];
XYZ((XYZ(:,2)< -0.7),:) = [];
XYZ((XYZ(:,3)> 2.5),:) = [];
pc0 = pointCloud(XYZ);


XYZ = pc1.Location;
XYZ((XYZ(:,1)< -0.5),:) = [];
XYZ((XYZ(:,2)< -0.7),:) = [];
XYZ((XYZ(:,3)> 2.5),:) = [];
pc1 = pointCloud(XYZ);

XYZ = pc2.Location;
XYZ((XYZ(:,1)< -0.5),:) = [];
XYZ((XYZ(:,2)< -0.7),:) = [];
XYZ((XYZ(:,3)> 2.5),:) = [];
pc2 = pointCloud(XYZ);

XYZ = pc3.Location;
XYZ((XYZ(:,1)< -0.5),:) = [];
XYZ((XYZ(:,2)< -0.7),:) = [];
XYZ((XYZ(:,3)> 2.5),:) = [];
pc3 = pointCloud(XYZ);
%pc1 = pcdenoise(pc1, 'NumNeighbors', nn, 'Threshold', thres);
%pc1 = pcdenoise(pc1, 'NumNeighbors', nn, 'Threshold', thres);
%pc2 = pcdenoise(pc2, 'NumNeighbors', nn, 'Threshold', thres);
%pc3 = pcdenoise(pc3, 'NumNeighbors', nn, 'Threshold', thres);

figure
pcshow(pc0);
figure
pcshow(pc1);
figure
pcshow(pc2);
figure
pcshow(pc3);





fprintf(' ...DONE*** \n');

%% Merging

gridSize = 0.01;
mergeSize = 0.015;

% Merge 0-1
fprintf('\n *** Merging 1...');

fixed = pcdownsample(pc0, 'gridAverage', gridSize);
moving = pcdownsample(pc1, 'gridAverage', gridSize);
tform = pcregrigid(moving, fixed, 'Metric', 'pointToPlane', 'Extrapolate', true);
ptCloudAligned = pctransform(pc1, tform);

ptCloudScene01 = pcmerge(pc0, ptCloudAligned, mergeSize);
fprintf(' ...DONE*** \n');

fprintf('\n *** Merging 2...');

% Merge 2-3
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
XYZ = ptCloudScene0123.Location;
XYZ((XYZ(:,1)< -0.6),:) = [];
XYZ((XYZ(:,2)< -0.75),:) = [];
XYZ((XYZ(:,3)> 2.5),:) = [];

ptCloudScene0123 = pointCloud(XYZ);
%ptCloudScene0123.Location(ptCloudScene0123.Location(:,1)<0.5)=[];
%ptCloudScene0123 = pcdenoise(ptCloudScene0123, 'NumNeighbors', 30, 'Threshold', 2*thres);
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

DATA.vertex.x = ptCloudScene0123.Location(:, 1); % coordinate of normal, [Nx1] real array%
DATA.vertex.y = ptCloudScene0123.Location(:, 2); %coordinate of normal, [Nx1] real array
DATA.vertex.z = ptCloudScene0123.Location(:, 3);
x = DATA.vertex.x;
y = DATA.vertex.y;
z = DATA.vertex.z;

%%
fprintf('\n *** Writing ply file .');

ply_write(DATA, 'output_data/merged.ply', 'binary_big_endian');
fprintf(' ... DONE \n');

%% Reconstruct surface

%pt_sampled = pcdownsample(ptCloudScene0123, 'gridAverage', 0.1)
%

%[t]=MyCrustOpen(pt_sampled.Location);

%figure
%trisurf(t,pt_sampled.Location(:,1),pt_sampled.Location(:,2),pt_sampled.Location(:,3)); hold on;

%%

%[volume,area] = triangulationVolume(t,pt_sampled.Location(:,1),pt_sampled.Location(:,2),pt_sampled.Location(:,3));
%[TriIdx, V] = convhull(pt_sampled.Location(:,1),pt_sampled.Location(:,2),pt_sampled.Location(:,3),'simplify', true)
%trisurf(TriIdx, pt_sampled.Location(:,1),pt_sampled.Location(:,2),pt_sampled.Location(:,3));hold on;
%tic;[rotmat,cornerpoints,volume,surface] = minboundbox(pt_sampled.Location(:,1),pt_sampled.Location(:,2),pt_sampled.Location(:,3),'v',3);toc
%plotminbox(cornerpoints,'b');

xadj = x - min(x);
yadj = y - min(y);
zadj = z - min(z);

%f = fit([x, y], zadj, 'linearinterp');
%q2 = quad2d(f,-0.55,0.55,0.3,2.1,'AbsTol',0.001)

F2 = scatteredInterpolant(x, y, zadj);
q1 = quad2d(@(x, y) F2(x, y), min(x), max(x), min(y), max(y), 'AbsTol', 0.1);
toc;
%%
fprintf('\n Free space is: %f', q1);
fprintf('\n Occupied space is: %f', 2- q1);

fprintf('\n End of execution \n');

