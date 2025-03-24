function [xt,yt] = evaldiff_python(x,y)
    mat1 = load('struct.mat');
    mapper1 = mat1.map.map;
    ansloc = evaldiff(mapper1,x+y*1i);
    xt = real(ansloc);
    yt = imag(ansloc);
end