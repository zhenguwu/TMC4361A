See S-shaped Ramping.png for a diagram

Equation Naming:

<img src="/tex/2103f85b8b1477f430fc407cad462224.svg?invert_in_darkmode&sanitize=true" align=middle width=8.55596444999999pt height=22.831056599999986pt/> = Displacement, Change in position<br />
<img src="/tex/6c4adbc36120d62b98deef2a20d5d303.svg?invert_in_darkmode&sanitize=true" align=middle width=8.55786029999999pt height=14.15524440000002pt/> - Final velocity<br />
<img src="/tex/ae5d2b8055caea8d4ee5dce2aff72c2c.svg?invert_in_darkmode&sanitize=true" align=middle width=16.77705149999999pt height=21.18721440000001pt/> - Initial velocity<br />
<img src="/tex/44bc9d542a92714cac84e01cbbb7fd61.svg?invert_in_darkmode&sanitize=true" align=middle width=8.68915409999999pt height=14.15524440000002pt/> = Final acceleration<br />
<img src="/tex/bc437d770056a8290a36f089fd92b5a9.svg?invert_in_darkmode&sanitize=true" align=middle width=16.908363449999992pt height=21.18721440000001pt/> = Initial acceleration<br />
<img src="/tex/36b5afebdba34564d884d347484ac0c7.svg?invert_in_darkmode&sanitize=true" align=middle width=7.710416999999989pt height=21.68300969999999pt/> = jerk<br />
<img src="/tex/4f4f4e395762a3af4575de74c019ebb5.svg?invert_in_darkmode&sanitize=true" align=middle width=5.936097749999991pt height=20.221802699999984pt/> = time

Equations:
1) <img src="/tex/b7a667808aa6edbebc41af7a589d43b0.svg?invert_in_darkmode&sanitize=true" align=middle width=80.53444079999998pt height=20.221802699999984pt/>
2) <img src="/tex/720d887aadd7d459717582ba229f23d8.svg?invert_in_darkmode&sanitize=true" align=middle width=104.35796909999999pt height=27.77565449999998pt/>
3) <img src="/tex/ade6d1df67e8b51b1e41bfbe43cebb03.svg?invert_in_darkmode&sanitize=true" align=middle width=99.33775169999998pt height=26.76175259999998pt/>
4) <img src="/tex/720946709182e4072c855fdbe28f4b23.svg?invert_in_darkmode&sanitize=true" align=middle width=80.40810524999999pt height=21.68300969999999pt/>
5) <img src="/tex/e225177103b17f458179108945d4ba11.svg?invert_in_darkmode&sanitize=true" align=middle width=138.69689129999998pt height=27.77565449999998pt/>
6) <img src="/tex/d0a5b4a99ce9c93fccc34eedb975e7c4.svg?invert_in_darkmode&sanitize=true" align=middle width=162.50330909999997pt height=27.77565449999998pt/>

Configurable:<br />
aMax (Max acceleration)<br />
j1, j2, j3, j4 (Jerk)

Given(renaming for convenience):<br />
vStart = start_v (These values are passed into set_junction's parameter)<br />
vMax = cruise_v<br />
vFinal = end_v<br />
aChange = accel_r (Calculated from GRBL cornering alg) <br />
a = aMax * accel_r<br />
d = total_distance(Needs to be confirmed)

Sent to motion controller:<br />
XTARGET = d <br />
ASTART = vStart<br />
VMAX = vMax<br />
DFINAL = vFinal<br />
AMAX = a<br />
DMAX = a<br />
BOW1 = j1<br />
BOW2 = j2<br />
BOW3 = j3<br />
BOW4 = j4

To keep equations clean: Phase B1 = 1, B12 = 2, B2 = 3, B23 = 4, B3 = 5, B34 = 6, B4 = 7

Following equations apply when vStart = 0:

PhaseB1(1):<br />
<img src="/tex/5b809e1e808a17451e0f4e404e69a8a9.svg?invert_in_darkmode&sanitize=true" align=middle width=49.055961899999986pt height=22.853275500000024pt/><br />
<img src="/tex/24bc5f3374e089f650fa2aae406f3dbf.svg?invert_in_darkmode&sanitize=true" align=middle width=74.39042984999999pt height=27.77565449999998pt/><br />
<img src="/tex/9e86a4f95e51fa714c9320b6f21b8513.svg?invert_in_darkmode&sanitize=true" align=middle width=74.9783265pt height=27.77565449999998pt/>

PhaseB12(2) - (Calculated from PhaseB1 and PhaseB2):<br />
<img src="/tex/670209ebf51c450f870bcf7efa0addeb.svg?invert_in_darkmode&sanitize=true" align=middle width=73.45679714999999pt height=27.7259796pt/><br />
<img src="/tex/9661c29a50f3d7c3c988489cc9d79aff.svg?invert_in_darkmode&sanitize=true" align=middle width=118.26786509999998pt height=27.77565449999998pt/>

PhaseB2(3):<br />
<img src="/tex/80dfb8056c2407d31f3e2c653d8a3c2a.svg?invert_in_darkmode&sanitize=true" align=middle width=49.055961899999986pt height=22.853275500000024pt/><br />
<img src="/tex/a2dfd77816b6e4a60d677aabdcda2055.svg?invert_in_darkmode&sanitize=true" align=middle width=180.9542229pt height=27.77565449999998pt/> <br />
<img src="/tex/60d32b523a322b03caadafa84862b94c.svg?invert_in_darkmode&sanitize=true" align=middle width=176.31124169999998pt height=27.77565449999998pt/>

If vStart =/= 0, PhaseB1 is skipped and goes directly to B12 with <img src="/tex/25a24c32caf24a99d3c697cd285cf31a.svg?invert_in_darkmode&sanitize=true" align=middle width=85.27968569999999pt height=22.465723500000017pt/>


Following equations apply when vFinal = 0:

PhaseB3(5):<br />
<img src="/tex/c31c1df65f597f3305016fbcc54653a4.svg?invert_in_darkmode&sanitize=true" align=middle width=49.055961899999986pt height=22.853275500000024pt/><br />
<img src="/tex/a4cf951d5c1b3b355f35180342dc7359.svg?invert_in_darkmode&sanitize=true" align=middle width=138.8633202pt height=27.77565449999998pt/><br />
<img src="/tex/3f4350c40af2e48f32bd8d200503fc61.svg?invert_in_darkmode&sanitize=true" align=middle width=165.54720764999996pt height=27.77565449999998pt/>

PhaseB34(6) - (Calculated from PhaseB3 and PhaseB4):<br />
<img src="/tex/3837bdd77e19fcdcc2f3e480e254b97f.svg?invert_in_darkmode&sanitize=true" align=middle width=73.45679714999999pt height=27.7259796pt/><br />
<img src="/tex/558599a8729fa3548a7e39ee7c40fd54.svg?invert_in_darkmode&sanitize=true" align=middle width=118.26786509999998pt height=27.77565449999998pt/>

PhaseB4(7):<br />
<img src="/tex/e32928b3852db1b64561c37513951975.svg?invert_in_darkmode&sanitize=true" align=middle width=49.055961899999986pt height=22.853275500000024pt/><br />
<img src="/tex/86d3584858020c16acc5371afebf62b3.svg?invert_in_darkmode&sanitize=true" align=middle width=116.48133254999999pt height=27.77565449999998pt/> <br />
<img src="/tex/33c49d1a632b2f53e7796b2cb7b23a7a.svg?invert_in_darkmode&sanitize=true" align=middle width=176.31124169999998pt height=27.77565449999998pt/>

If vFinal =/= 0, PhaseB4 is skipped and PhaseB34 is solved with <img src="/tex/b2fad38132a280ec360d882485304c10.svg?invert_in_darkmode&sanitize=true" align=middle width=88.11952874999999pt height=22.831056599999986pt/>


PhaseB23(4) - (Calculated after all other phases):<br />
<img src="/tex/caa0b3b6e90ec71714197dc855e51734.svg?invert_in_darkmode&sanitize=true" align=middle width=72.54323504999999pt height=29.46111299999998pt/><br />
<img src="/tex/1536e2e59ef13e4a610847a2e254332f.svg?invert_in_darkmode&sanitize=true" align=middle width=261.71179155pt height=22.831056599999986pt/> 
