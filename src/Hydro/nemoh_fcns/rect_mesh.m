function [] = rect_mesh(projdir,L,W,Draft,depth,wavedir,nbfreq,wmax)
% Creates Mesh of rectangular prism (can be used to approximate OSWEC). 
% INPUTS:
%   projdir     ->  [string]    directory to save meshing results to
%   L,W,Draft   ->  [m]         dimensions of regtangular prism
%   depth       ->  [m]         depth of water
%   wavedir     ->  [deg]       direction of waves, zero = along "W" axis
%   nbfreq      ->  [#]         number of frequencies
%   wmax        ->  [rad/s]     maximum frequency to evaluate
% OUTPUTS:
%   None, but creates files in projdir folder.
%
% Example: rect_mesh('./output',10,20,5,600,0,60,3) % this matches example
% in matlabRoutines/NemohWrapper/getStarted.m from Nemoh repo:
% https://gitlab.com/lheea/Nemoh/-/tree/master?ref_type=heads

% left face
X(1,1,:,:)=[-L/2,0,-Draft;
    -L/2,-W/2,-Draft;
    -L/2,-W/2,0;
    -L/2,0,0] ;
% Bottom face
X(1,2,:,:)=[-L/2,-W/2,-Draft;
    -L/2,0,-Draft
    L/2,0,-Draft;
    L/2,-W/2,-Draft;];
% right face
X(1,3,:,:)=[L/2,0,-Draft;
    L/2,0,0;
    L/2,-W/2,0;
    L/2,-W/2,-Draft] ;
% front face
X(1,4,:,:)=[-L/2,-W/2,-Draft;
    L/2,-W/2,-Draft;
    L/2,-W/2,0;
    -L/2,-W/2,0];

ncoarse=length(X(1,:,1,1));   % number of coarse panels
nBodies=length(X(:,1,1,1));   % 1 body
tX=0;           % 0 no translation applied to the Mesh
xyzCoG=[0,0,0]; % position of gravity centre
nfobj=600;      % target number of panels for Aquaplus mesh
w= linspace(wmax/nbfreq,wmax,nbfreq)'; % min w [rad/s], max w [rad/s], Nw
QTFInput=[0,2];%[Switch,Contrib]
Mesh(nBodies,ncoarse,X,tX,xyzCoG,nfobj,depth,w,wavedir,QTFInput,projdir);
end

