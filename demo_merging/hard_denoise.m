function [ pc ] = hard_denoise( pc )

xl = -0.5;
xh = 0.6;
yl = -0.7;
yh = 0.25;
zl = 0;
zh = 2.5;

XYZ = pc.Location;
XYZ((XYZ(:,1)< xl),:) = [];
XYZ((XYZ(:,1)> xh),:) = [];
XYZ((XYZ(:,2)< yl),:) = [];
XYZ((XYZ(:,2)> yh),:) = [];
XYZ((XYZ(:,3)> zh),:) = [];
pc = pointCloud(XYZ);

end

