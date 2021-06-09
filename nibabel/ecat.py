# emacs: -*- mode: python-mode; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the NiBabel package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
""" Read ECAT format images

An ECAT format image consists of:

* a *main header*;
* at least one *matrix list* (mlist);

ECAT thinks of memory locations in terms of *blocks*.  One block is 512
bytes.  Thus block 1 starts at 0 bytes, block 2 at 512 bytes, and so on.

The matrix list is an array with one row per frame in the data.

Columns in the matrix list are:

* 0: Matrix identifier (frame number)
* 1: matrix data start block number (subheader followed by image data)
* 2: Last block number of matrix (image) data
* 3: Matrix status

    * 1: hxists - rw
    * 2: exists - ro
    * 3: matrix deleted

There is one sub-header for each image frame (or matrix in the terminology
above).  A sub-header can also be called an *image header*.  The sub-header is
one block (512 bytes), and the frame (image) data follows.

There is very little documentation of the ECAT format, and many of the comments
in this code come from a combination of trial and error and wild speculation.

There are ~2 formats of ECAT files EACT7 and ECAT6.3 that are widely in use,
the byte position, header field/variable name, type, and description of each of
formats are as follows:

ECAT 6.3
########################################################################################################################

Main Header for Matrix Data Files

When Filled, Byte, Variable Name, Type, Comment
 , 0, %FILL(14), Integer*2, User reserved space (28 bytes)
A, 28, ORIGINAL_FILE_NAME, Character*20, Scan file's creation name
A, 48, SW_VERSION, Integer*2, Enumerated type (VER_PRE5, VER_5, etc.)
A, 50, DATA_TYPE, Integer*2, E. Type (DTYPE_BYTES, DTYPE_12, etc.)
A, 52, SYSTEM_TYPE, Integer*2, E. Type (MODEL_911_01, _02, etc.)
A, 54, FILE_TYPE, Integer*2, E. Type (FTYPE_SCAN, _IMAGE, etc.)
C, 56, NODE_ID, Character*10, Unique ID of the ECAT system used
C, 66, SCAN_START_DAY, Integer*2, Day acquisition was started
C, 68, SCAN_START_MONTH, Integer*2, Month acquisition was started
C, 70, SCAN_START_YEAR, Integer*2, Year acquisition was started
C, 72, SCAN_START_HOUR, Integer*2, Hour acquisition was started
C, 74, SCAN_START_MINUTE, Integer*2, Minute acquisition was started
C, 76, SCAN_START_SECOND, Integer*2, Second acquisition was started
A, 78, ISOTOPE_CODE, Character*8, Isotope specifier
A, 86, ISOTOPE_HALFLIFE, Real*4, Half-life of isotope specified (in sec.)
A, 90, RADIOPHARMACUETICAL, Character*32, Free format ASCII
A, 122, GANTRY_TILT, Real*4, Angle (in degrees)
A, 126, GANTRY_ROTATION, Real*4, Angle (in degrees)
A, 130, BED_ELEVATION, Real*4, Bed height (in cm.) from lowest point
A, 134, ROT_SOURCE_SPEED, Integer*2, Revolutions/minute (0 if not rotating)
A, 136, WOBBLE_SPEED, Integer*2, Revolutions/minute (0 if not wobbled)
A, 138, TRANSM_SOURCE_TYPE, Integer*2, Enumerated type (SRC_NONE, _RRS, etc.)
A, 140, AXIAL_FOV, Real*4, Distance (in cm.) from first to last plane
A, 144, TRANSAXIAL_FOV, Real*4, Distance (in cm.) of transaxial view
A, 148, TRANSAXIAL_SAMP_MODE, Integer*2, Enumerated Type (XSAMP_STAT, _3, etc.)
A, 150, COIN_SAMP_MODE, Integer*2, E. type (CSAMP_NET_TRUES, etc.)
A, 152, AXIAL_SAMP_MODE, Integer*2, E. type (ASAMP_NORM, _2X, etc.)
C, 154, CALIBRATION_FACTOR, Real*4, Quantification scale factor
C, 158, CALIBRATION_UNITS, Integer*2, Enumerated type (UNIT_UCIML, etc.)
B/C, 160, COMPRESSION_CODE, Integer*2, Enumerate type (COMP_NONE, etc.)
A, 162, STUDY_NAME, Character*12, Study descriptor
A, 174, PATIENT_ID, Character*16, Patient identification descriptor
A, 190, PATIENT_NAME, Character*32, Patient name (free format ASCII)
A, 222, PATIENT_SEX, Character*1, E. type (SEX_MALE, _FEMALE, etc.)
A, 223, PATIENT_AGE, Character*10, Patient age (free format)
A, 233, PATIENT_HEIGHT, Character*10, Patient height (free format)
A, 243, PATIENT_WEIGHT, Character*10, Patient weight (free format)
A, 253, PATIENT_DEXTERITY, Character*1, E. type (DEXT_RT, _LF, _AMB, etc.)
A, 254, PHYSICIAN_NAME, Character*32, Physician name (free format)
A, 286, OPERATOR_NAME, Character*32, Operator name (free format)
A, 318, STUDY_DESCRIPTION, Character*32, Free format ASCII
A, 350, ACQUISITION_TYPE, Integer*2, E. type (ACQ_RECTTR, _DYEM, etc.)
A, 352, BED_TYPE, Integer*2, E. type (BED_CTI, BED_SIEMENS, etc.)
A, 354, SEPTA_TYPE, Integer*2, E. type (SEPTA_NONE, 3MM, etc.)
A, 356, FACILITY_NAME, Character*20, Free format ASCII
A, 376, NUM_PLANES, Integer*2, Number of planes of data collected
A, 378, NUM_FRAMES, Integer*2, Number of frames of data collected
A, 380, NUM_GATES, Integer*2, Number of gates of data collected
A, 382, NUM_BED_POS, Integer*2, Number of bed positions of data collected
A, 384, INIT_BED_POSITION, Real*4, Absolute bed location of bed position 0 (cm.)
A, 388, BED_OFFSET(15), Real*4, Offset from INIT_BED_POSITION (in cm.)
A, 448, PLANE_SEPARATION, Real*4, Distance between adjacent planes (in cm.)
A, 452, LWR_SCTR_THRES, Integer*2, Lowest threshold setting for scatter (in KeV)
A, 454, LWR_TRUE_THRES, Integer*2, Lower threshold setting for trues (in KeV)
A, 456, UPR_TRUE_THRES, Integer*2, Upper threshold setting for trues (in KeV)
A, 458, COLLIMATOR, Real*4, Collimator position (if applicable--911's)
 , 462, USER_PROCESS_CODE, Character*10, Data processing code (defined by user)
 , 472, %FILL(20), Integer*2, User reserved space (40 bytes)


ECAT7
########################################################################################################################
Main Header for Matrix Data Files

Byte, Variable, Name, Type,                 Comment
0, MAGIC_NUMBER, Character*14,              UNIX file type identification number (NOT PART
                                            OF THE MATRIX HEADER DATA)
14, ORIGINAL_FILE_NAME,                     Character*32, Scan file’s creation name
46, SW_VERSION, Integer*2,                  Software version number
48, SYSTEM TYPE,Integer*2,                  Scanner model (i.e., 951, 951R, 953, 953B,
                                            921, 922, 925, 961, 962, 966)
50, FILE_TYPE,                              Integer*2, Enumerated type (00=unknown, 01=Sinogram, 02=Image-16,
                                            03=Attenuation Correction, 04=Normalization,
                                            05=Polar Map, 06=Volume 8, 07=Volume 16,
                                            08=Projection 8, 09=Projection 16, 10=Image 8,
                                            11=3D Sinogram 16, 12=3D Sinogram 8,
                                            13=3D Normalization, 14=3D Sinogram Fit)
52, SERIAL_NUMBER, Character*10,            The serial number of the gantry
62, SCAN_START_TIME, Integer*4,             Date and time that acquisition was started (in
                                            secs from base time)
66, ISOTOPE_NAME, Character*8,              Isotope
74, ISOTOPE_HALFLIFE, Real*4,               Half-life of isotope specified (in sec.)
78, RADIOPHARMACEUTICAL,                    Character*32, Free format ASCII
110, GANTRY_TILT, Real*4,                   Angle (in degrees)
114, GANTRY_ROTATION, Real*4,               Angle (in degrees)
118, BED_ELEVATION, Real*4,                 Bed height (in cm.) from lowest point
122, INTRINSIC_TILT, Real*4,                Angle (in degrees),Angle that the first detector of Bucket 0 is offset from
                                            top center (in degrees)
126, WOBBLE_SPEED, Integer*2,               Revolutions/minute (0 if not wobbled)
128, TRANSM_SOURCE_TYPE, Integer 2,         Enumerated type (SRC_NONE, _RRING, _RING, _ROD, _RROD)
130, DISTANCE_SCANNED, Real*4,              Total distance scanned (in cm)
134, TRANSAXIAL_FOV, Real*4,                Diameter (in cm.) of transaxial view
138, ANGULAR_COMPRESSION, Integer*2,        Enumerated Type (0=no mash,1=mash of 2, 2=mash of 4)
140, COIN_SAMP_MODE, Integer*2,             Enumerated type (0=Net Trues, 1=Prompts and Delayed, 3= Prompts, Delayed,
                                            and Multiples)
142, AXIAL_SAMP_MODE, Integer*2,            Enumerated type (0=Normal, 1=2X, 2=3X)
144, ECAT_CALIBRATION_FACTOR, Real*4,       Quantification scale factor (to convert from ECAT counts to activity counts)
148, CALIBRATION_UNITS, Integer*2,          Enumerated type (0=Uncalibrated, 1=Calibrated,)
150, CALIBRATION_UNITS_LABEL, Integer*2,    Enumerated type (BLOOD_FLOW, LMRGLU)
152, COMPRESSION_CODE, Integer*2,           Enumerated type (COMP_NONE, (This is the only value))
154, STUDY_TYPE, Character*12,              Study descriptor
166, PATIENT_ID, Character*16,              Patient identification descriptor
182, PATIENT_NAME, Character*32,            Patient name (free format ASCII)
214, PATIENT_SEX, Character*1,              Enumerated type (SEX_MALE, _FEMALE, _UNKNOWN)
215, PATIENT_DEXTERITY, Character*1,        Enumerated type (DEXT_RT, _LF, _UNKNOWN)
216, PATIENT_AGE, Real*4,                   Patient age (years)
220, PATIENT_HEIGHT, Real*4,                Patient height (cm)
224, PATIENT_WEIGHT, Real*4,                Patient weight (kg)
228, PATIENT_BIRTH_DATE, Integer*4,         Format is YYYYMMDD
232, PHYSICIAN_NAME, Character*32,          Attending Physician name (free format)
264, OPERATOR_NAME, Character*32,           Operator name (free format)
296, STUDY_DESCRIPTION, Character*32,       Free format ASCII
328, ACQUISITION_TYPE, Integer*2,           Enumerated type (0=Undefined, 1=Blank, 2=Transmission, 3=Static emission,
                                            4=Dynamic emission, 5=Gated emission, 6=Transmission rectilinear,
                                            7=Emission rectilinear)
330, PATIENT_ORIENTATION, Integer*2,        Enumerated Type (Bit 0 clear - Feet first, Bit 0 set - Head first,
                                            Bit 1-2 00 - Prone, Bit 1-2 01 - Supine, Bit 1-2 10 - Decubitus Right,
                                            Bit 1-2 11 - Decubitus Left)
332, FACILITY_NAME, Character*20,           Free format ASCII
352, NUM_PLANES, Integer*2,                 Number of planes of data collected
354, NUM_FRAMES, Integer*2,                 Number of frames of data collected OR Highest frame number (in partially
                                            reconstructed files)
356, NUM_GATES, Integer*2,                  Number of gates of data collected
358, NUM_BED_POS, Integer*2,                Number of bed positions of data collected
360, INIT_BED_POSITION, Real*4,             Absolute location of initial bed position (in cm.)
364, BED_POSITION(15), Real*4,              Absolute bed location (in cm.)
424, PLANE_SEPARATION, Real*4,              Physical distance between adjacent planes (in cm.)
428, LWR_SCTR_THRES, Integer*2,             Lowest threshold setting for scatter (in KeV)
430, LWR_TRUE_THRES, Integer*2,             Lower threshold setting for trues in (in KeV)
432, UPR_TRUE_THRES, Integer*2,             Upper threshold setting for trues (in KeV)
434, USER_PROCESS_CODE, Character*10,       Data processing code (defined by user)
444, ACQUISITION_MODE, Integer*2,           Enumerated Type (0=Normal, 1=Windowed, 2=Windowed & Nonwindowed,
                                            3=Dual energy, 4=Upper energy, 5=Emission and Transmission)
446, BIN_SIZE, Real*4,                      Width of view sample (in cm)
450, BRANCHING_FRACTION, Real*4,            Fraction of decay by positron emission
454, DOSE_START_TIME, Integer*4,            Actual time radiopharmaceutical was injected or flow was started (in sec
                                            since base time)
458, DOSAGE, Real*4,                        Radiopharmaceutical dosage (in bequerels/cc) at time of injection
462, WELL_COUNTER_CORR_FACTOR, Real*4, TBD
466, DATA_UNITS, Character*3.2
498, SEPTA_STATE, Integer*2,                Septa position during scan (0=septa extended, 1=septa retracted)
500, FILL(6), Integer*2,                    CTI Reserved space (12 bytes)


########################################################################################################################
Subheader for Matrix Attenuation Files

Byte, Variable, Name, Type,                 Comment
0, DATA_TYPE, Integer*2,                    Enumerated type (DTYPE_BYTES, _I2, _I4, _VAXR4, _SUNFL, _SUNIN)
2, NUM_DIMENSIONS, Integer*2,               Number of dimensions
4, ATTENUATION_TYPE, Integer*2,             E. type (ATTEN_NONE, _MEAS, _CALC)
6, NUM_R_ELEMENTS, Integer*2,               Total elements collected (x dimension)
8, NUM_ANGLES, Integer*2,                   Total views collected (y dimensions)
10, NUM_Z_ELEMENTS, Integer*2,              Total elements collected (z dimension)
12, RING_DIFFERENCE, Integer*2,             Maximum acceptance angle.
14, X_RESOLUTION, Real*4,                   Resolution in the x dimension (in cm)
18, Y_RESOLUTION, Real*4,                   Resolution in the y dimension (in cm)
22, Z_RESOLUTION, Real*4,                   Resolution in the z dimension (in cm)
26, W_RESOLUTION, Real*4,                   TBD
30, SCALE_FACTOR, Real*4,                   Attenuation Scale Factor
34, X_OFFSET, Real*4,                       Ellipse offset in x axis from center (in cm.)
38, Y_OFFSET, Real*4,                       Ellipse offset in y axis from center (in cm.)
42, X_RADIUS, Real*4,                       Ellipse radius in x axis (in cm.)
46, Y_RADIUS, Real*4,                       Ellipse radius in y axis (in cm.)
50, TILT_ANGLE, Real*4,                     Tilt angel of the ellipse (in degrees)
54, ATTENUATION_COEFF, Real*4,              M u-absorption coefficient (in cm^-1)
58, ATTENUATION_MIN, Real*4,                Minimum value in the attenuation data
62, ATTENUATION_MAX, Real*4,                Maximum value in the attentuation data
66, SKULL_THICKNESS, Real*4,                Skull thickness in cm
70, NUM_ADDITIONAL_ATTN_COEFF, Integer*2,   Number of attenuation coefficients other than the Mu absorption coefficient
                                            above (max 8)
72, ADDITIONAL_ATTEN_COEFF(8), Real*4,      The additional attention coefficient values
104, EDGE_FINDING_THRESHOLD, Real*4,        The threshold value used by automatic edge-detection routine
                                            (fraction of maximum)
108, STORAGE_ORDER, Integer*2,              Data storage order (RThetaZD, RZThetaD)
110, SPAN, Integer*2,                       Axial compression specifier (number of ring differences spanned by a
                                            segment)
112, Z_ELEMENTS(64), Integer*2,             Number of "planes" in z direction for each ring difference segment
240, FILL(86), Integer*2,                   Unused (172 bytes)
412, FILL(50), Integer*2,                   User Reserved space (100 bytes) Note: use highest bytes first

########################################################################################################################
Subheader for Matrix Image Files

Byte, Variable, Name, Type,                 Comment
0, DATA_TYPE, Integer*2,                    Enumerated type (0=Unkonwn Matrix Data Type, 1=Byte Data, 2=VAX_Ix2, 3=VAX_Ix4,
                                            4=VAX_Rx4, 5=IEEE Float, 6=Sun short, 7=Sun long)
2, NUM_DIMENSIONS, Integer*2,               Number of dimensions
4, X_DIMENSION, Integer*2,                  Dimension along x axis
6, Y_DIMENSION, Integer*2,                  Dimension along y axis
8, Z_DIMENSION, Integer*2,                  Dimension along z axis
10, X_OFFSET, Real*4,                       Offset in x axis for recon target (in cm)
14, Y_OFFSET, Real*4,                       Offset in y axis for recon target (in cm)
18, Z_OFFSET, Real*4,                       Offset in z axis for recon target (in cm)
22, RECON_ZOOM, Real*4,                     Reconstruction magnification factor (zoom)
26, SCALE_FACTOR, Real*4,                   Quantification scale factor (in Quant_units)
30, IMAGE_MIN, Integer*2,                   Image minimum pixel value
32, IMAGE_MAX, Integer*2,                   Image maximum pixel value
34, X_PIXEL_SIZE, Real*4,                   X dimension pixel size (in cm.)
38, Y_PIXEL_SIZE, Real*4,                   Y dimension pixel size (in cm.)
42, Z_PIXEL_SIZE, Real*4,                   Z dimension pixel size (in cm.)
46, FRAME_DURATION, Integer*4,              Total duration of current frame (in msec.)
50, FRAME_START_TIME, Integer*4,            frame start time (offset from first frame, in msec)
54, FILTER_CODE, Integer*2,                 enumerated type (0=all pass, 1=ramp, 2=Butterworth, 3=Hanning, 4=Hamming,
                                            5=Parzen, 6=shepp, 7=butterworth-order 2, 8=Gaussian, 9=Median, 10=Boxcar)
56, X_RESOLUTION, Real*4,                   resolution in the x dimension (in cm)
60, Y_RESOLUTION, Real*4,                   resolution in the y dimension (in cm)
64, Z_RESOLUTION, Real*4,                   resolution in the z dimension (in cm)
68, NUM_R_ELEMENTS, Real*4,                 number r elements from sinogram
72, NUM_ANGLES, Real*4,                     number of angles from sinogram
76, Z_ROTATION_ANGLE, Real*4,               rotation in the xy plane (in degrees). Use right-hand coordinate system for
                                            rotation angle sign.
80, DECAY_CORR_FCTR, Real*4,                isotope decay compensation applied to data
84, PROCESSING_CODE, Integer*4,             bit mask (0=not processed, 1=normalized, 2=Measured Attenuation Correction,
                                            4=Calculated attenuation correction, 8=x smoothing, 16=Y smoothing,
                                            32=Z smoothing, 64=2d scatter correction, 128=3D scatter correction,
                                            256=arc correction, 512=decay correction, 1024=Online compression)
88, GATE_DURATION, Integer*4,               gate duration (in msec)
92, R_WAVE_OFFSET, Integer*4,               r wave offset (for phase sliced studies, average, in msec)
96, NUM_ACCEPTED_BEATS, Integer*4,          number of accepted beats for this gate
100, FILTER_CUTOFF_FREQUENCY,               real*4, cutoff frequency
104, FILTER_RESOLUTION, Real*4,             do not use
108, FILTER_RAMP_SLOPE, Real*4,             do not use
112, FILTER_ORDER, Integer*2,               do not use
114, FILTER_SCATTER_FRACTION, Real*4,       do not use
118, FILTER_SCATTER_SLOPE,Real*4,           do not use
122, ANNOTATION, Character*40,              free format ascii
162, MT_1_1, Real*4,                        matrix transformation element (1,1).
166, MT_1_2, Real*4,                        matrix transformation element (1,2).
170, MT_1_3, Real*4,                        matrix transformation element (1,3).
174, MT_2_1, Real*4,                        matrix transformation element (2,1).
178, MT_2_2, Real*4,                        matrix transformation element (2,2).
182, MT_2_3, Real*4,                        matrix transformation element (2,3).
186, MT_3_1, Real*4,                        matrix transformation element (3,1).
190, MT_3_2, Real*4,                        matrix transformation element (3,2).
194, MT_3_3, Real*4,                        matrix transformation element (3,3).
198, RFILTER_CUTOFF, Real*4
202, RFILTER_RESOLUTION, Real*4
206, RFILTER_CODE, Integer*2
208, RFILTER_ORDER, Integer*2
210, ZFILTER_CUTOFF, Real*4
214, ZFILTER_RESOLUTION, Real*4
218, ZFILTER_CODE, Integer*2
220, ZFILTER_ORDER, Integer*2
222, MT_1_4, Real*4,                        Matrix transformation element (1,4)
226, MT_2_4, Real*4,                        Matrix transformation element (2,4)
230, MT_3_4, Real*4,                        Matrix transformation element (3,4)
234, SCATTER_TYPE, Integer*2,               Enumerated type (0=None, 1=Deconvolution, 2=Simulated, 3=Dual Energy)
236, RECON_TYPE, Integer*2,                 Enumerated type (0=Filtered backprojection,
                                            1=Forward projection 3D (PROMIS), 2=Ramp 3D, 3=FAVOR 3D, 4=SSRB,
                                            5=Multi-slice rebinning, 6=FORE)
238 RECON_VIEWS, Integer*2,                 Number of views used to reconstruct the data
240, FILL(87), Integer*2,                   CTI Reserved space (174 bytes)
414 FILL(48), Integer*2,                    User Reserved space (100 bytes) Note: Use highest bytes first

########################################################################################################################
Subheader for Matrix Polar Map Files

Byte, Variable Name, Type,                  Comment
0, DATA_TYPE, Integer*2,                    Enumerated type (DTYPE_BYTES, _I2,_I4)
2, POLAR_MAP_TYPE, Integer*2,               Enumerated Type (Always 0 for now; denotes the version of the PM structure)
4, NUM_RINGS, Integer*2,                    Number of rings in this polar map
6, SECTORS_PER_RING(32), Integer*2,         Number of sectors in each ring for up to 32 rings
                                            (1, 9, 18, or 32 sectors normally)
70, RING_POSITION(32), Real*4,              Fractional distance along the long axis from base to apex
198, RING_ANGLE(32), Integer*2,             Ring angle relative to long axis(90 degrees along cylinder,
                                            decreasing to 0 at the apex)
262, START_ANGLE, Integer*2,                Start angle for rings (Always 258 degrees, defines Polar Map’s 0)
264, LONG_AXIS_LEFT(3), Integer*2,          x, y, z location of long axis base end (in pixels)
270, LONG_AXIS_RIGHT(3), Integer*2,         x, y, z location of long axis apex end (in pixels)
276, POSITION_DATA, Integer*2,              Enumerated type (0 - Not available, 1 - Present)
278, IMAGE_MIN, Integer*2,                  Minimum pixel value in this polar map
280, IMAGE_MAX, Integer*2,                  Maximum pixel value in this polar map
282, SCALE_FACTOR, Real*4,                  Scale factor to restore integer values to float values
286, PIXEL_SIZE, Real*4,                    Pixel size (in cubic cm, represents voxels)
290, FRAME_DURATION, Integer*4,             Total duration of current frame (in msec)
294, FRAME_START_TIME, Integer*4,           Frame start time (offset from first frame, in msec)
298, PROCESSING_CODE, Integer*2,            Bit Encoded (1- Map type (0 = Sector Analysis, 1 = Volumetric),
                                            2 - Threshold Applied, 3 - Summed Map, 4 - Subtracted Map,
                                            5 - Product of two maps, 6 - Ratio of two maps, 7 - Bias,
                                            8 - Multiplier, 9 - Transform, 10 - Polar Map calculational protocol used)
300, QUANT_UNITS, Integer*2,                Enumerated Type (0 - Default (see main header), 1 - Normalized, 2 - Mean,
                                            3 - Std. Deviation from Mean)
302, ANNOTATION, Character*40,              label for polar map display
342, GATE_DURATION, Integer*4,              Gate duration (in msec)
346, R_WAVE_OFFSET, Integer*4,              R wave offset (Average, in msec)
350, NUM_ACCEPTED_BEATS, Integer*4          Number of accepted beats for this gate
354, POLAR_MAP_PROTOCOL, Character*20,      Polar Map protocol used to generate this polar map
374, DATABASE_NAME,Character*30,            Database name used for polar map comparison
404, FILL(27), Integer*2,                   Reserved for future CTI use (54 bytes)
464, FILL(27), Integer*2,                   User reserved space (54 bytes) Note: Use highest bytes first


########################################################################################################################
Subheader for 3D Matrix Scan Files

Byte, Variable Name, Type,                  Comment
0, DATA_TYPE, Integer*2,                    Enumerated type (ByteData, SunShortt)
2, NUM_DIMENSIONS, Integer*2,               Number of Dimensions
4, NUM_R_ELEMENTS, Integer*2,               Total views collected (θ dimension)
6, NUM_ANGLES, Integer*2,                   Total views collected (θ dimension)
8, CORRECTIONS_APPLIED, Integer*2,          Designates processing applied to scan data
                                            (Bit encoded, Bit 0 - Norm, Bit 1 - Atten, Bit 2 - Smooth)
10, NUM_Z_ELEMENTS(64), Integer*2,          Number of elements in z dimension for each ring difference segment in
                                            3D scans
138, RING_DIFFERENCE, Integer*2,            Max ring difference (d dimension) in this frame
140, STORAGE_ORDER, Integer*2,              Data storage order (rθzd or rzθd)
142, AXIAL_COMPRESSION, Integer*2,          Axial compression code or factor, generally referred to as SPAN
144, X_RESOLUTION, Real*4,                  Resolution in the r dimension (in cm)
148, V_RESOLUTION, Real*4,                  Resolution in the θ dimension (in radians)
152, Z_RESOLUTION, Real*4,                  Resolution in the z dimension (in cm)
156, W_RESOLUTION, Real*4,                  Not Used
160, FILL(6), Integer*2,                    RESERVED for gating
172, GATE_DURATION, Integer*4,              Gating segment length (msec, Average time if phased gates are used)
176, R_WAVE_OFFSET, Integer*4,              Time from start of first gate (Average, in msec.)
180, NUM_ACCEPTED_BEATS, Integer*4,         Number of accepted beats for this gate
184, SCALE_FACTOR, Real*4,                  If data type is integer, this factor is used to convert to float values
188, SCAN_MIN, Integer*2,                   Minimum value in sinogram if data is in integer form
                                            (not currently filled in)
190, SCAN_MAX, Integer*2,                   Maximum value in sinogram if data is in integer form
                                            (not currently filled in)
192, PROMPTS, Integer*4,                    Total prompts collected in this frame/gate
196, DELAYED, Integer*4,                    Total delays collected in this frame/gate
200, MULTIPLES, Integer*4,                  Total multiples collected in this frame/gate (notused)
204, NET_TRUES, Integer*4,                  Total net trues (prompts–-randoms)
208, TOT_AVG_COR, Real*4,                   Mean value of loss-corrected singles
212, TOT_AVG_UNCOR, Real*4,                 Mean value of singles (not loss corrected)
216, TOTAL_COIN_RATE, Integer*4,            Measured coincidence rate (from IPCP)
220, FRAME_START_TIME, Integer*4,           Time offset from first frame time (in msec.)
224, FRAME_DURATION, Integer*4,             Total duration of current frame (in msec.)
228, DEADTIME_CORRECTION_FACTOR, Real*4,    Dead-time correction factor applied to the sinogram
232, FILL(90), Integer*2,                   CTI Reserved space (180 bytes)
412, FILL(50), Integer*2,                   User Reserved space (100 bytes) Note: Use highest bytes first
512, UNCOR_SINGLES(128), Real*4,            Total uncorrected singles from each bucket

########################################################################################################################
Subheader for 3D normalized Files

Byte, Variable Name, Type,                  Comment
0, DATA_TYPE, Integer*2,                    Enumerated type (IeeeFloat)
2, NUM_R_ELEMENTS, Integer*2,               Total elements collected (y dimension)
4, NUM_TRANSAXIAL_CRYSTALS, Integer*2,      Number of transaxial crystals per block
6, NUM_CRYSTAL_RINGS, Integer*2,            Number of crystal rings
8, CRYSTALS_PER_RING, Integer*2,            Number of crystals per ring
10, NUM_GEO_CORR_PLANES, Integer*2,         Number of rows in the Plane Geometric Correction array
12, ULD, Integer*2,                         Upper energy limit
14, LLD, Integer*2,                         Lower energy limit
16, SCATTER_ENERGY, Integer*2,              Scatter energy threshold
18, NORM_QUALITY_FACTOR, Real*4,            Used by Daily Check to determine the quality of the scanner
22, NORM_QUALITY_FACTOR_CODE,               Enumerated Type (TBD)
24, RING_DTCOR1(32), Real*4,                First “per ring” dead time correction coefficient
152, RING_DTCOR2(32), Real*4,               Second “per ring” dead time correction coefficient
280, CRYSTAL_DTCOR(8), Real*4,              Dead time correction factors for transaxial crystals
312, SPAN, Integer*2,                       Axial compression specifier (number of ring differences included in
                                            each segment)
314, MAX_RING_DIFF, Integer*2,              Maximum ring difference acquired
316, FILL(48), Integer*2,                   CTI Reserved space (96 bytes)
412, FILL(50), Integer*2,                   User Reserved space (100 bytes) Note: Use highest bytes first

########################################################################################################################
Subheader for Imported 6.5 Matrix Scan Files

Version 6.5 scan files that or imported into version 7.X cannot be reconstructed. The subheader is only 512 bytes,
rather than 1024.

Byte, Variable Name, Type,                  Comment
0, DATA_TYPE, Integer*2,                    Enumerated type (DTYPE_BYTES, _I2, _I4, _VAXR4, _SUNFL, _SUNIN)
2, NUM_DIMENSIONS, Integer*2,               Number of Dimensions
4, NUM_R_ELEMENTS, Integer*2,               Total elements collected (x dimension)
6, NUM_ANGLES, Integer*2,                   Total views collected (y dimension)
8, CORRECTIONS_APPLIED, Integer*2,          Designates processing applied to scan data (Bit encoded, Bit 0 - Norm,
                                            Bit 1 - Atten, Bit 2 - Smooth)
10, NUM_Z_ELEMENTS, Integer*2,              Total elements collected (z dimension) For 3D scans
12, RING_DIFFERENCE, Integer*2,             Maximum acceptance angle
14, X_RESOLUTION, Real*4,                   Resolution in the x dimension (in cm)
18, Y_RESOLUTION, Real*4,                   Resolution in the y dimension (in cm)
22, Z_RESOLUTION, Real*4,                   Resolution in the z dimension (in cm)
26, W_RESOLUTION, Real*4,                   TBD
30, FILL(6), Integer*2,                     RESERVED for gating
42, GATE_DURATION, Integer*4,               Gating segment length (msec, Average time if phased gates are used)
46, R_WAVE_OFFSET, Integer*4,               Time from start of first gate (Average, in msec.)
50, NUM_ACCEPTED_BEATS, Integer*4,          Number of accepted beats for this gate
50, SCALE_FACTOR, Real*4,                   If data type=integer, use this factor, convert to float values
58, SCAN_MIN, Integer*2,                    Minimum value in sinogram if data is in integer form
60, SCAN_MAX, Integer*2,                    Maximum value in sinogram if data is in integer form
62, PROMPTS, Integer*4,                     Total prompts collected in this frame/gate
66, DELAYED, Integer*4,                     Total delays collected in thes frame/gate
70, MULTIPLES, Integer*4,                   Total multiples collected in the frame/gate
74, NET_TRUES, Integer*4,                   Total net trues (prompts--randoms)
78, COR_SINGLES(16), Real*4,                Total singles with loss correction factoring
142, UNCOR_SINGLES(16), Real*4,             Total singles without loss correction factoring
206, TOT_AVG_COR, Real*4,                   Mean value of loss-corrected singles
210, TOT_AVG_UNCOR, Real*4,                 Mean value of singles (not loss corrected)
214, TOTAL_COIN_RAIN, Integer*4,            Measured coincidence rate (from IPCP)
218, FRAME_START_TIME, Integer*4,           Time offset from first frame time (in msec.)
222, FRAME_DURATION, Integer*4,             Total duration of current frame (in msec.)
226, DEADTIME_CORRECTION_FACTOR, Real*4,    Dead-time correction factor applied to the sinogram
230, PHYSICAL_PLANES, Integer*2,            Physical planes that make up this logical plane
246, FILL(83), Integer*2,                   CTI Reserved space (166 bytes)
412, FILL(50) Integer*2,                    User Reserved space (100 bytes) Note: use highest bytes first

XMedcon can read and write ECAT 6 format, and read ECAT 7 format: see
http://xmedcon.sourceforge.net and the ECAT files in the source of XMedCon,
currently ``libs/tpc/*ecat*`` and ``source/m-ecat*``.  Unfortunately XMedCon is
GPL and some of the header files are adapted from CTI files (called CTI code
below).  It's not clear what the licenses are for these files.




"""

import warnings
from numbers import Integral

import numpy as np

from .volumeutils import (native_code, swapped_code, make_dt_codes,
                          array_from_file)
from .spatialimages import SpatialImage
from .arraywriters import make_array_writer
from .wrapstruct import WrapStruct
from .fileslice import canonical_slicers, predict_shape, slice2outax
from .deprecated import deprecate_with_version

BLOCK_SIZE = 512

main_header_dtd = [
    ('magic_number', '14S'),
    ('original_filename', '32S'),
    ('sw_version', np.uint16),
    ('system_type', np.uint16),
    ('file_type', np.uint16),
    ('serial_number', '10S'),
    ('scan_start_time', np.uint32),
    ('isotope_name', '8S'),
    ('isotope_halflife', np.float32),
    ('radiopharmaceutical', '32S'),
    ('gantry_tilt', np.float32),
    ('gantry_rotation', np.float32),
    ('bed_elevation', np.float32),
    ('intrinsic_tilt', np.float32),
    ('wobble_speed', np.uint16),
    ('transm_source_type', np.uint16),
    ('distance_scanned', np.float32),
    ('transaxial_fov', np.float32),
    ('angular_compression', np.uint16),
    ('coin_samp_mode', np.uint16),
    ('axial_samp_mode', np.uint16),
    ('ecat_calibration_factor', np.float32),
    ('calibration_unitS', np.uint16),
    ('calibration_units_type', np.uint16),
    ('compression_code', np.uint16),
    ('study_type', '12S'),
    ('patient_id', '16S'),
    ('patient_name', '32S'),
    ('patient_sex', '1S'),
    ('patient_dexterity', '1S'),
    ('patient_age', np.float32),
    ('patient_height', np.float32),
    ('patient_weight', np.float32),
    ('patient_birth_date', np.uint32),
    ('physician_name', '32S'),
    ('operator_name', '32S'),
    ('study_description', '32S'),
    ('acquisition_type', np.uint16),
    ('patient_orientation', np.uint16),
    ('facility_name', '20S'),
    ('num_planes', np.uint16),
    ('num_frames', np.uint16),
    ('num_gates', np.uint16),
    ('num_bed_pos', np.uint16),
    ('init_bed_position', np.float32),
    ('bed_position', '15f'),
    ('plane_separation', np.float32),
    ('lwr_sctr_thres', np.uint16),
    ('lwr_true_thres', np.uint16),
    ('upr_true_thres', np.uint16),
    ('user_process_code', '10S'),
    ('acquisition_mode', np.uint16),
    ('bin_size', np.float32),
    ('branching_fraction', np.float32),
    ('dose_start_time', np.uint32),
    ('dosage', np.float32),
    ('well_counter_corr_factor', np.float32),
    ('data_units', '32S'),
    ('septa_state', np.uint16),
    ('fill', '12S')
]
hdr_dtype = np.dtype(main_header_dtd)


subheader_dtd = [
    ('data_type', np.uint16),
    ('num_dimensions', np.uint16),
    ('x_dimension', np.uint16),
    ('y_dimension', np.uint16),
    ('z_dimension', np.uint16),
    ('x_offset', np.float32),
    ('y_offset', np.float32),
    ('z_offset', np.float32),
    ('recon_zoom', np.float32),
    ('scale_factor', np.float32),
    ('image_min', np.int16),
    ('image_max', np.int16),
    ('x_pixel_size', np.float32),
    ('y_pixel_size', np.float32),
    ('z_pixel_size', np.float32),
    ('frame_duration', np.uint32),
    ('frame_start_time', np.uint32),
    ('filter_code', np.uint16),
    ('x_resolution', np.float32),
    ('y_resolution', np.float32),
    ('z_resolution', np.float32),
    ('num_r_elements', np.float32),
    ('num_angles', np.float32),
    ('z_rotation_angle', np.float32),
    ('decay_corr_fctr', np.float32),
    ('corrections_applied', np.uint32),
    ('gate_duration', np.uint32),
    ('r_wave_offset', np.uint32),
    ('num_accepted_beats', np.uint32),
    ('filter_cutoff_frequency', np.float32),
    ('filter_resolution', np.float32),
    ('filter_ramp_slope', np.float32),
    ('filter_order', np.uint16),
    ('filter_scatter_fraction', np.float32),
    ('filter_scatter_slope', np.float32),
    ('annotation', '40S'),
    ('mt_1_1', np.float32),
    ('mt_1_2', np.float32),
    ('mt_1_3', np.float32),
    ('mt_2_1', np.float32),
    ('mt_2_2', np.float32),
    ('mt_2_3', np.float32),
    ('mt_3_1', np.float32),
    ('mt_3_2', np.float32),
    ('mt_3_3', np.float32),
    ('rfilter_cutoff', np.float32),
    ('rfilter_resolution', np.float32),
    ('rfilter_code', np.uint16),
    ('rfilter_order', np.uint16),
    ('zfilter_cutoff', np.float32),
    ('zfilter_resolution', np.float32),
    ('zfilter_code', np.uint16),
    ('zfilter_order', np.uint16),
    ('mt_4_1', np.float32),
    ('mt_4_2', np.float32),
    ('mt_4_3', np.float32),
    ('scatter_type', np.uint16),
    ('recon_type', np.uint16),
    ('recon_views', np.uint16),
    ('fill', '174S'),
    ('fill2', '96S')]
subhdr_dtype = np.dtype(subheader_dtd)

# Ecat Data Types
# See:
# http://www.turkupetcentre.net/software/libdoc/libtpcimgio/ecat7_8h_source.html#l00060
# and:
# http://www.turkupetcentre.net/software/libdoc/libtpcimgio/ecat7r_8c_source.html#l00717
_dtdefs = (  # code, name, equivalent dtype
    (1, 'ECAT7_BYTE', np.uint8),
    # Byte signed? https://github.com/nipy/nibabel/pull/302/files#r28275780
    (2, 'ECAT7_VAXI2', np.int16),
    (3, 'ECAT7_VAXI4', np.int32),
    (4, 'ECAT7_VAXR4', np.float32),
    (5, 'ECAT7_IEEER4', np.float32),
    (6, 'ECAT7_SUNI2', np.int16),
    (7, 'ECAT7_SUNI4', np.int32))
data_type_codes = make_dt_codes(_dtdefs)


# Matrix File Types
ft_defs = (  # code, name
    (0, 'ECAT7_UNKNOWN'),
    (1, 'ECAT7_2DSCAN'),
    (2, 'ECAT7_IMAGE16'),
    (3, 'ECAT7_ATTEN'),
    (4, 'ECAT7_2DNORM'),
    (5, 'ECAT7_POLARMAP'),
    (6, 'ECAT7_VOLUME8'),
    (7, 'ECAT7_VOLUME16'),
    (8, 'ECAT7_PROJ'),
    (9, 'ECAT7_PROJ16'),
    (10, 'ECAT7_IMAGE8'),
    (11, 'ECAT7_3DSCAN'),
    (12, 'ECAT7_3DSCAN8'),
    (13, 'ECAT7_3DNORM'),
    (14, 'ECAT7_3DSCANFIT'))
file_type_codes = dict(ft_defs)

patient_orient_defs = (  # code, description
    (0, 'ECAT7_Feet_First_Prone'),
    (1, 'ECAT7_Head_First_Prone'),
    (2, 'ECAT7_Feet_First_Supine'),
    (3, 'ECAT7_Head_First_Supine'),
    (4, 'ECAT7_Feet_First_Decubitus_Right'),
    (5, 'ECAT7_Head_First_Decubitus_Right'),
    (6, 'ECAT7_Feet_First_Decubitus_Left'),
    (7, 'ECAT7_Head_First_Decubitus_Left'),
    (8, 'ECAT7_Unknown_Orientation'))
patient_orient_codes = dict(patient_orient_defs)

# Indexes from the patient_orient_defs structure defined above for the
# neurological and radiological viewing conventions
patient_orient_radiological = [0, 2, 4, 6]
patient_orient_neurological = [1, 3, 5, 7]


class EcatHeader(WrapStruct):
    """Class for basic Ecat PET header

    Sub-parts of standard Ecat File

    * main header
    * matrix list
      which lists the information for each frame collected (can have 1 to many
      frames)
    * subheaders specific to each frame with possibly-variable sized data
      blocks

    This just reads the main Ecat Header, it does not load the data or read the
    mlist or any sub headers
    """
    template_dtype = hdr_dtype
    _ft_codes = file_type_codes
    _patient_orient_codes = patient_orient_codes

    def __init__(self,
                 binaryblock=None,
                 endianness=None,
                 check=True):
        """Initialize Ecat header from bytes object

        Parameters
        ----------
        binaryblock : {None, bytes} optional
            binary block to set into header, By default, None in which case we
            insert default empty header block
        endianness : {None, '<', '>', other endian code}, optional
            endian code of binary block, If None, guess endianness
            from the data
        check : {True, False}, optional
            Whether to check and fix header for errors.  No checks currently
            implemented, so value has no effect.
        """
        super(EcatHeader, self).__init__(binaryblock, endianness, check)

    @classmethod
    def guessed_endian(klass, hdr):
        """Guess endian from MAGIC NUMBER value of header data
        """
        if not hdr['sw_version'] == 74:
            return swapped_code
        else:
            return native_code

    @classmethod
    def default_structarr(klass, endianness=None):
        """ Return header data for empty header with given endianness
        """
        hdr_data = super(EcatHeader, klass).default_structarr(endianness)
        hdr_data['magic_number'] = 'MATRIX72'
        hdr_data['sw_version'] = 74
        hdr_data['num_frames'] = 0
        hdr_data['file_type'] = 0  # Unknown
        hdr_data['ecat_calibration_factor'] = 1.0  # scale factor
        return hdr_data

    def get_data_dtype(self):
        """ Get numpy dtype for data from header"""
        raise NotImplementedError("dtype is only valid from subheaders")

    def get_patient_orient(self):
        """ gets orientation of patient based on code stored
        in header, not always reliable
        """
        code = self._structarr['patient_orientation'].item()
        if code not in self._patient_orient_codes:
            raise KeyError('Ecat Orientation CODE %d not recognized' % code)
        return self._patient_orient_codes[code]

    def get_filetype(self):
        """ Type of ECAT Matrix File from code stored in header"""
        code = self._structarr['file_type'].item()
        if code not in self._ft_codes:
            raise KeyError('Ecat Filetype CODE %d not recognized' % code)
        return self._ft_codes[code]

    @classmethod
    def _get_checks(klass):
        """ Return sequence of check functions for this class """
        return ()


def read_mlist(fileobj, endianness):
    """ read (nframes, 4) matrix list array from `fileobj`

    Parameters
    ----------
    fileobj : file-like
        an open file-like object implementing ``seek`` and ``read``

    Returns
    -------
    mlist : (nframes, 4) ndarray
        matrix list is an array with ``nframes`` rows and columns:

        * 0: Matrix identifier (frame number)
        * 1: matrix data start block number (subheader followed by image data)
        * 2: Last block number of matrix (image) data
        * 3: Matrix status

            * 1: hxists - rw
            * 2: exists - ro
            * 3: matrix deleted

    Notes
    -----
    A block is 512 bytes.

    ``block_no`` in the code below is 1-based.  block 1 is the main header,
    and the mlist blocks start at block number 2.

    The 512 bytes in an mlist block contain 32 rows of the int32 (nframes,
    4) mlist matrix.

    The first row of these 32 looks like a special row.  The 4 values appear
    to be (respectively):

    * not sure - maybe negative number of mlist rows (out of 31) that are
      blank and not used in this block.  Called `nfree` but unused in CTI
      code;
    * block_no - of next set of mlist entries or 2 if no more entries. We also
      allow 1 or 0 to signal no more entries;
    * <no idea>.  Called `prvblk` in CTI code, so maybe previous block no;
    * n_rows - number of mlist rows in this block (between ?0 and 31) (called
      `nused` in CTI code).
    """
    dt = np.dtype(np.int32)
    if endianness is not native_code:
        dt = dt.newbyteorder(endianness)
    mlists = []
    mlist_index = 0
    mlist_block_no = 2  # 1-based indexing, block with first mlist
    while True:
        # Read block containing mlist entries
        fileobj.seek((mlist_block_no - 1) * BLOCK_SIZE)  # fix 1-based indexing
        dat = fileobj.read(BLOCK_SIZE)
        rows = np.ndarray(shape=(32, 4), dtype=dt, buffer=dat)
        # First row special, points to next mlist entries if present
        n_unused, mlist_block_no, _, n_rows = rows[0]
        if not (n_unused + n_rows) == 31:  # Some error condition here?
            mlist = []
            return mlist
        # Use all but first housekeeping row
        mlists.append(rows[1:n_rows + 1])
        mlist_index += n_rows
        if mlist_block_no <= 2:  # should block_no in (1, 2) be an error?
            break
    return np.row_stack(mlists)


def get_frame_order(mlist):
    """Returns the order of the frames stored in the file
    Sometimes Frames are not stored in the file in
    chronological order, this can be used to extract frames
    in correct order

    Returns
    -------
    id_dict: dict mapping frame number -> [mlist_row, mlist_id]

    (where mlist id is value in the first column of the mlist matrix )

    Examples
    --------
    >>> import os
    >>> import nibabel as nib
    >>> nibabel_dir = os.path.dirname(nib.__file__)
    >>> from nibabel import ecat
    >>> ecat_file = os.path.join(nibabel_dir,'tests','data','tinypet.v')
    >>> img = ecat.load(ecat_file)
    >>> mlist = img.get_mlist()
    >>> get_frame_order(mlist)
    {0: [0, 16842758]}
    """
    ids = mlist[:, 0].copy()
    n_valid = np.sum(ids > 0)
    ids[ids <= 0] = ids.max() + 1  # put invalid frames at end after sort
    valid_order = np.argsort(ids)
    if not all(valid_order == sorted(valid_order)):
        # raise UserWarning if Frames stored out of order
        warnings.warn_explicit(f'Frames stored out of order; true order = {valid_order}\n'
                               'frames will be accessed in order STORED, NOT true order',
                               UserWarning, 'ecat', 0)
    id_dict = {}
    for i in range(n_valid):
        id_dict[i] = [valid_order[i], ids[valid_order[i]]]
    return id_dict


def get_series_framenumbers(mlist):
    """ Returns framenumber of data as it was collected,
    as part of a series; not just the order of how it was
    stored in this or across other files

    For example, if the data is split between multiple files
    this should give you the true location of this frame as
    collected in the series
    (Frames are numbered starting at ONE (1) not Zero)

    Returns
    -------
    frame_dict: dict mapping order_stored -> frame in series
            where frame in series counts from 1; [1,2,3,4...]

    Examples
    --------
    >>> import os
    >>> import nibabel as nib
    >>> nibabel_dir = os.path.dirname(nib.__file__)
    >>> from nibabel import ecat
    >>> ecat_file = os.path.join(nibabel_dir,'tests','data','tinypet.v')
    >>> img = ecat.load(ecat_file)
    >>> mlist = img.get_mlist()
    >>> get_series_framenumbers(mlist)
    {0: 1}
    """
    nframes = len(mlist)
    frames_order = get_frame_order(mlist)
    mlist_nframes = len(frames_order)
    trueframenumbers = np.arange(nframes - mlist_nframes, nframes)
    frame_dict = {}
    for frame_stored, (true_order, _) in frames_order.items():
        # frame as stored in file -> true number in series
        try:
            frame_dict[frame_stored] = trueframenumbers[true_order] + 1
        except IndexError:
            raise IOError('Error in header or mlist order unknown')
    return frame_dict


def read_subheaders(fileobj, mlist, endianness):
    """ Retrieve all subheaders and return list of subheader recarrays

    Parameters
    ----------
    fileobj : file-like
        implementing ``read`` and ``seek``
    mlist : (nframes, 4) ndarray
        Columns are:
        * 0 - Matrix identifier.
        * 1 - subheader block number
        * 2 - Last block number of matrix data block.
        * 3 - Matrix status
    endianness : {'<', '>'}
        little / big endian code

    Returns
    -------
    subheaders : list
        List of subheader structured arrays
    """
    subheaders = []
    dt = subhdr_dtype
    if endianness is not native_code:
        dt = dt.newbyteorder(endianness)
    for mat_id, sh_blkno, sh_last_blkno, mat_stat in mlist:
        if sh_blkno == 0:
            break
        offset = (sh_blkno - 1) * BLOCK_SIZE
        fileobj.seek(offset)
        tmpdat = fileobj.read(BLOCK_SIZE)
        sh = np.ndarray(shape=(), dtype=dt, buffer=tmpdat)
        subheaders.append(sh)
    return subheaders


class EcatSubHeader(object):

    _subhdrdtype = subhdr_dtype
    _data_type_codes = data_type_codes

    def __init__(self, hdr, mlist, fileobj):
        """parses the subheaders in the ecat (.v) file
        there is one subheader for each frame in the ecat file

        Parameters
        -----------
        hdr : EcatHeader
            ECAT main header
        mlist : array shape (N, 4)
            Matrix list
        fileobj : ECAT file <filename>.v  fileholder or file object
                  with read, seek methods
        """
        self._header = hdr
        self.endianness = hdr.endianness
        self._mlist = mlist
        self.fileobj = fileobj
        self.subheaders = read_subheaders(fileobj, mlist, hdr.endianness)

    def get_shape(self, frame=0):
        """ returns shape of given frame"""
        subhdr = self.subheaders[frame]
        x = subhdr['x_dimension'].item()
        y = subhdr['y_dimension'].item()
        z = subhdr['z_dimension'].item()
        return x, y, z

    def get_nframes(self):
        """returns number of frames"""
        framed = get_frame_order(self._mlist)
        return len(framed)

    def _check_affines(self):
        """checks if all affines are equal across frames"""
        nframes = self.get_nframes()
        if nframes == 1:
            return True
        affs = [self.get_frame_affine(i) for i in range(nframes)]
        if affs:
            i = iter(affs)
            first = next(i)
            for item in i:
                if not np.allclose(first, item):
                    return False
        return True

    def get_frame_affine(self, frame=0):
        """returns best affine for given frame of data"""
        subhdr = self.subheaders[frame]
        x_off = subhdr['x_offset']
        y_off = subhdr['y_offset']
        z_off = subhdr['z_offset']

        zooms = self.get_zooms(frame=frame)

        dims = self.get_shape(frame)
        # get translations from center of image
        origin_offset = (np.array(dims) - 1) / 2.0
        aff = np.diag(zooms)
        aff[:3, -1] = -origin_offset * zooms[:-1] + np.array([x_off, y_off,
                                                              z_off])
        return aff

    def get_zooms(self, frame=0):
        """returns zooms  ...pixdims"""
        subhdr = self.subheaders[frame]
        x_zoom = subhdr['x_pixel_size'] * 10
        y_zoom = subhdr['y_pixel_size'] * 10
        z_zoom = subhdr['z_pixel_size'] * 10
        return (x_zoom, y_zoom, z_zoom, 1)

    def _get_data_dtype(self, frame):
        dtcode = self.subheaders[frame]['data_type'].item()
        return self._data_type_codes.dtype[dtcode]

    def _get_frame_offset(self, frame=0):
        return int(self._mlist[frame][1] * BLOCK_SIZE)

    def _get_oriented_data(self, raw_data, orientation=None):
        """
        Get data oriented following ``patient_orientation`` header field. If
        the ``orientation`` parameter is given, return data according to this
        orientation.

        :param raw_data: Numpy array containing the raw data
        :param orientation: None (default), 'neurological' or 'radiological'
        :rtype: Numpy array containing the oriented data
        """
        if orientation is None:
            orientation = self._header['patient_orientation']
        elif orientation == 'neurological':
            orientation = patient_orient_neurological[0]
        elif orientation == 'radiological':
            orientation = patient_orient_radiological[0]
        else:
            raise ValueError('orientation should be None,\
                neurological or radiological')

        if orientation in patient_orient_neurological:
            raw_data = raw_data[::-1, ::-1, ::-1]
        elif orientation in patient_orient_radiological:
            raw_data = raw_data[::, ::-1, ::-1]

        return raw_data

    def raw_data_from_fileobj(self, frame=0, orientation=None):
        """
        Get raw data from file object.

        :param frame: Time frame index from where to fetch data
        :param orientation: None (default), 'neurological' or 'radiological'
        :rtype: Numpy array containing (possibly oriented) raw data

        .. seealso:: data_from_fileobj
        """
        dtype = self._get_data_dtype(frame)
        if self._header.endianness is not native_code:
            dtype = dtype.newbyteorder(self._header.endianness)
        shape = self.get_shape(frame)
        offset = self._get_frame_offset(frame)
        fid_obj = self.fileobj
        raw_data = array_from_file(shape, dtype, fid_obj, offset=offset)
        raw_data = self._get_oriented_data(raw_data, orientation)
        return raw_data

    def data_from_fileobj(self, frame=0, orientation=None):
        """
        Read scaled data from file for a given frame

        :param frame: Time frame index from where to fetch data
        :param orientation: None (default), 'neurological' or 'radiological'
        :rtype: Numpy array containing (possibly oriented) raw data

        .. seealso:: raw_data_from_fileobj
        """
        header = self._header
        subhdr = self.subheaders[frame]
        raw_data = self.raw_data_from_fileobj(frame, orientation)
        # Scale factors have to be set to scalars to force scalar upcasting
        data = raw_data * header['ecat_calibration_factor'].item()
        data = data * subhdr['scale_factor'].item()
        return data


class EcatImageArrayProxy(object):
    """ Ecat implemention of array proxy protocol

    The array proxy allows us to freeze the passed fileobj and
    header such that it returns the expected data array.
    """

    def __init__(self, subheader):
        self._subheader = subheader
        self._data = None
        x, y, z = subheader.get_shape()
        nframes = subheader.get_nframes()
        self._shape = (x, y, z, nframes)

    @property
    def shape(self):
        return self._shape

    @property
    def ndim(self):
        return len(self.shape)

    @property
    def is_proxy(self):
        return True

    def __array__(self, dtype=None):
        """ Read of data from file

        This reads ALL FRAMES into one array, can be memory expensive.

        If you want to read only some slices, use the slicing syntax
        (``__getitem__``) below, or ``subheader.data_from_fileobj(frame)``

        Parameters
        ----------
        dtype : numpy dtype specifier, optional
            A numpy dtype specifier specifying the type of the returned array.

        Returns
        -------
        array
            Scaled image data with type `dtype`.
        """
        # dtype=None is interpreted as float64
        data = np.empty(self.shape)
        frame_mapping = get_frame_order(self._subheader._mlist)
        for i in sorted(frame_mapping):
            data[:, :, :, i] = self._subheader.data_from_fileobj(
                frame_mapping[i][0])
        if dtype is not None:
            data = data.astype(dtype, copy=False)
        return data

    def __getitem__(self, sliceobj):
        """ Return slice `sliceobj` from ECAT data, optimizing if possible
        """
        sliceobj = canonical_slicers(sliceobj, self.shape)
        # Indices into sliceobj referring to image axes
        ax_inds = [i for i, obj in enumerate(sliceobj) if obj is not None]
        assert len(ax_inds) == len(self.shape)
        frame_mapping = get_frame_order(self._subheader._mlist)
        # Analyze index for 4th axis
        slice3 = sliceobj[ax_inds[3]]
        # We will load volume by volume.  Make slicer into volume by dropping
        # index over the volume axis
        in_slicer = sliceobj[:ax_inds[3]] + sliceobj[ax_inds[3] + 1:]
        # int index for 4th axis, load one slice
        if isinstance(slice3, Integral):
            data = self._subheader.data_from_fileobj(frame_mapping[slice3][0])
            return data[in_slicer]
        # slice axis for 4th axis, we will iterate over slices
        out_shape = predict_shape(sliceobj, self.shape)
        out_data = np.empty(out_shape)
        # Slice into output data with out_slicer
        out_slicer = [slice(None)] * len(out_shape)
        # Work out axis corresponding to volume in output
        in2out_ind = slice2outax(len(self.shape), sliceobj)[3]
        # Iterate over specified 4th axis indices
        for i in list(range(self.shape[3]))[slice3]:
            data = self._subheader.data_from_fileobj(
                frame_mapping[i][0])
            out_slicer[in2out_ind] = i
            out_data[tuple(out_slicer)] = data[in_slicer]
        return out_data


class EcatImage(SpatialImage):
    """ Class returns a list of Ecat images, with one image(hdr/data) per frame
    """
    _header = EcatHeader
    header_class = _header
    valid_exts = ('.v',)
    _subheader = EcatSubHeader
    files_types = (('image', '.v'), ('header', '.v'))

    ImageArrayProxy = EcatImageArrayProxy

    def __init__(self, dataobj, affine, header,
                 subheader, mlist,
                 extra=None, file_map=None):
        """ Initialize Image

        The image is a combination of
        (array, affine matrix, header, subheader, mlist)
        with optional meta data in `extra`, and filename / file-like objects
        contained in the `file_map`.

        Parameters
        ----------
        dataobj : array-like
            image data
        affine : None or (4,4) array-like
            homogeneous affine giving relationship between voxel coords and
            world coords.
        header : None or header instance
            meta data for this image format
        subheader : None or subheader instance
            meta data for each sub-image for frame in the image
        mlist : None or array
            Matrix list array giving offset and order of data in file
        extra : None or mapping, optional
            metadata associated with this image that cannot be
            stored in header or subheader
        file_map : mapping, optional
            mapping giving file information for this image format

        Examples
        --------
        >>> import os
        >>> import nibabel as nib
        >>> nibabel_dir = os.path.dirname(nib.__file__)
        >>> from nibabel import ecat
        >>> ecat_file = os.path.join(nibabel_dir,'tests','data','tinypet.v')
        >>> img = ecat.load(ecat_file)
        >>> frame0 = img.get_frame(0)
        >>> frame0.shape == (10, 10, 3)
        True
        >>> data4d = img.get_fdata()
        >>> data4d.shape == (10, 10, 3, 1)
        True
        """
        self._subheader = subheader
        self._mlist = mlist
        self._dataobj = dataobj
        if affine is not None:
            # Check that affine is array-like 4,4.  Maybe this is too strict at
            # this abstract level, but so far I think all image formats we know
            # do need 4,4.
            affine = np.array(affine, dtype=np.float64, copy=True)
            if not affine.shape == (4, 4):
                raise ValueError('Affine should be shape 4,4')
        self._affine = affine
        if extra is None:
            extra = {}
        self.extra = extra
        self._header = header
        if file_map is None:
            file_map = self.__class__.make_file_map()
        self.file_map = file_map
        self._data_cache = None
        self._fdata_cache = None

    @property
    def affine(self):
        if not self._subheader._check_affines():
            warnings.warn('Affines different across frames, loading affine '
                          'from FIRST frame', UserWarning)
        return self._affine

    def get_frame_affine(self, frame):
        """returns 4X4 affine"""
        return self._subheader.get_frame_affine(frame=frame)

    def get_frame(self, frame, orientation=None):
        """
        Get full volume for a time frame

        :param frame: Time frame index from where to fetch data
        :param orientation: None (default), 'neurological' or 'radiological'
        :rtype: Numpy array containing (possibly oriented) raw data
        """
        return self._subheader.data_from_fileobj(frame, orientation)

    def get_data_dtype(self, frame):
        subhdr = self._subheader
        dt = subhdr._get_data_dtype(frame)
        return dt

    @property
    def shape(self):
        x, y, z = self._subheader.get_shape()
        nframes = self._subheader.get_nframes()
        return(x, y, z, nframes)

    def get_mlist(self):
        """ get access to the mlist
        """
        return self._mlist

    def get_subheaders(self):
        """get access to subheaders"""
        return self._subheader

    @classmethod
    @deprecate_with_version('from_filespec class method is deprecated.\n'
                            'Please use the ``from_file_map`` class method '
                            'instead.',
                            '2.1', '4.0')
    def from_filespec(klass, filespec):
        return klass.from_filename(filespec)

    @staticmethod
    def _get_fileholders(file_map):
        """ returns files specific to header and image of the image
        for ecat .v this is the same image file

        Returns
        -------
        header : file holding header data
        image : file holding image data
        """
        return file_map['header'], file_map['image']

    @classmethod
    def from_file_map(klass, file_map, *, mmap=True, keep_file_open=None):
        """class method to create image from mapping
        specified in file_map
        """
        hdr_file, img_file = klass._get_fileholders(file_map)
        # note header and image are in same file
        hdr_fid = hdr_file.get_prepare_fileobj(mode='rb')
        header = klass._header.from_fileobj(hdr_fid)
        hdr_copy = header.copy()
        # LOAD MLIST
        mlist = np.zeros((header['num_frames'], 4), dtype=np.int32)
        mlist_data = read_mlist(hdr_fid, hdr_copy.endianness)
        mlist[:len(mlist_data)] = mlist_data
        # LOAD SUBHEADERS
        subheaders = klass._subheader(hdr_copy, mlist, hdr_fid)
        # LOAD DATA
        # Class level ImageArrayProxy
        data = klass.ImageArrayProxy(subheaders)
        # Get affine
        if not subheaders._check_affines():
            warnings.warn('Affines different across frames, loading affine '
                          'from FIRST frame', UserWarning)
        aff = subheaders.get_frame_affine()
        img = klass(data, aff, header, subheaders, mlist,
                    extra=None, file_map=file_map)
        return img

    def _get_empty_dir(self):
        """
        Get empty directory entry of the form
        [numAvail, nextDir, previousDir, numUsed]
        """
        return np.array([31, 2, 0, 0], dtype=np.int32)

    def _write_data(self, data, stream, pos, dtype=None, endianness=None):
        """
        Write data to ``stream`` using an array_writer

        :param data: Numpy array containing the dat
        :param stream: The file-like object to write the data to
        :param pos: The position in the stream to write the data to
        :param endianness: Endianness code of the data to write
        """
        if dtype is None:
            dtype = data.dtype

        if endianness is None:
            endianness = native_code

        stream.seek(pos)
        make_array_writer(data.newbyteorder(endianness),
                          dtype).to_fileobj(stream)

    def to_file_map(self, file_map=None):
        """ Write ECAT7 image to `file_map` or contained ``self.file_map``

        The format consist of:

        - A main header (512L) with dictionary entries in the form
            [numAvail, nextDir, previousDir, numUsed]
        - For every frame (3D volume in 4D data)
          - A subheader (size = frame_offset)
          - Frame data (3D volume)
        """
        if file_map is None:
            file_map = self.file_map

        # It appears to be necessary to load the data before saving even if the
        # data itself is not used.
        self.get_fdata()
        hdr = self.header
        mlist = self._mlist
        subheaders = self.get_subheaders()
        dir_pos = 512
        entry_pos = dir_pos + 16  # 528
        current_dir = self._get_empty_dir()

        hdr_fh, img_fh = self._get_fileholders(file_map)
        hdrf = hdr_fh.get_prepare_fileobj(mode='wb')
        imgf = hdrf

        # Write main header
        hdr.write_to(hdrf)

        # Write every frames
        for index in range(0, self.header['num_frames']):
            # Move to subheader offset
            frame_offset = subheaders._get_frame_offset(index) - 512
            imgf.seek(frame_offset)

            # Write subheader
            subhdr = subheaders.subheaders[index]
            imgf.write(subhdr.tobytes())

            # Seek to the next image block
            pos = imgf.tell()
            imgf.seek(pos + 2)

            # Get frame
            image = self._subheader.raw_data_from_fileobj(index)

            # Write frame images
            self._write_data(image, imgf, pos + 2, endianness='>')

            # Move to dictionnary offset and write dictionnary entry
            self._write_data(mlist[index], imgf, entry_pos, endianness='>')

            entry_pos = entry_pos + 16

            current_dir[0] = current_dir[0] - 1
            current_dir[3] = current_dir[3] + 1

            # Create a new directory is previous one is full
            if current_dir[0] == 0:
                # self._write_dir(current_dir, imgf, dir_pos)
                self._write_data(current_dir, imgf, dir_pos)
                current_dir = self._get_empty_dir()
                current_dir[3] = dir_pos / 512
                dir_pos = mlist[index][2] + 1
                entry_pos = dir_pos + 16

        tmp_avail = current_dir[0]
        tmp_used = current_dir[3]

        # Fill directory with empty data until directory is full
        while current_dir[0] > 0:
            entry_pos = dir_pos + 16 + (16 * current_dir[3])
            self._write_data(np.zeros(4, dtype=np.int32), imgf, entry_pos)
            current_dir[0] = current_dir[0] - 1
            current_dir[3] = current_dir[3] + 1

        current_dir[0] = tmp_avail
        current_dir[3] = tmp_used

        # Write directory index
        self._write_data(current_dir, imgf, dir_pos, endianness='>')

    @classmethod
    def from_image(klass, img):
        raise NotImplementedError("Ecat images can only be generated "
                                  "from file objects")

    @classmethod
    def load(klass, filespec):
        return klass.from_filename(filespec)


load = EcatImage.load
