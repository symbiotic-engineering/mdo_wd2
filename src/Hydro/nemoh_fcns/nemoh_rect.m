function [] = nemoh_rect(L,W,Draft,depth,wavedir,nbfreq,wmax)
% Calls NEMOH to solve hydrondymaics for rectangular prism.
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
% Example: nemoh_rect(10,20,5,600,0,60,3) % this matches example
% in matlabRoutines/NemohWrapper/getStarted.m from Nemoh repo:
% https://gitlab.com/lheea/Nemoh/-/tree/master?ref_type=heads

projdir = './output';
rect_mesh(projdir,L,W,Draft,depth,wavedir,nbfreq,wmax);
[Idw,w,A,B,Fe]=Nemoh(projdir,0,0); % Call the function Nemoh.m
end

