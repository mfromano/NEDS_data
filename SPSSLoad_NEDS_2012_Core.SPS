/*****************************************************************************/
/* SPSSload_NEDS_2012_Core.SPS                                          */
/* This program will load the 2012 NEDS csv Core File into SPSS.         */
/*****************************************************************************/

/* Read data elements from the csv file */
get data /type = txt
    /file = "NEDS_2012_Core.csv"
    /delimiters = ',' 
    /variables = 
    AGE                      F3.0
    AMONTH                   F2.0
    AWEEKEND                 F2.0
    CHRON1                   F3.0
    CHRON2                   F3.0
    CHRON3                   F3.0
    CHRON4                   F3.0
    CHRON5                   F3.0
    CHRON6                   F3.0
    CHRON7                   F3.0
    CHRON8                   F3.0
    CHRON9                   F3.0
    CHRON10                  F3.0
    CHRON11                  F3.0
    CHRON12                  F3.0
    CHRON13                  F3.0
    CHRON14                  F3.0
    CHRON15                  F3.0
    DIED_VISIT               F2.0
    DISCWT                   F11.7
    DISP_ED                  F2.0
    DQTR                     F2.0
    DX1                      A5
    DX2                      A5
    DX3                      A5
    DX4                      A5
    DX5                      A5
    DX6                      A5
    DX7                      A5
    DX8                      A5
    DX9                      A5
    DX10                     A5
    DX11                     A5
    DX12                     A5
    DX13                     A5
    DX14                     A5
    DX15                     A5
    DXCCS1                   F3.0
    DXCCS2                   F3.0
    DXCCS3                   F3.0
    DXCCS4                   F3.0
    DXCCS5                   F3.0
    DXCCS6                   F3.0
    DXCCS7                   F3.0
    DXCCS8                   F3.0
    DXCCS9                   F3.0
    DXCCS10                  F3.0
    DXCCS11                  F3.0
    DXCCS12                  F3.0
    DXCCS13                  F3.0
    DXCCS14                  F3.0
    DXCCS15                  F3.0
    ECODE1                   A5
    ECODE2                   A5
    ECODE3                   A5
    ECODE4                   A5
    EDEVENT                  F2.0
    E_CCS1                   F4.0
    E_CCS2                   F4.0
    E_CCS3                   F4.0
    E_CCS4                   F4.0
    FEMALE                   F2.0
    HCUPFILE                 A4
    HOSP_ED                  F5.0
    INJURY                   F2.0
    INJURY_CUT               F2.0
    INJURY_DROWN             F2.0
    INJURY_FALL              F2.0
    INJURY_FIRE              F2.0
    INJURY_FIREARM           F2.0
    INJURY_MACHINERY         F2.0
    INJURY_MVT               F2.0
    INJURY_NATURE            F2.0
    INJURY_POISON            F2.0
    INJURY_SEVERITY          F2.0
    INJURY_STRUCK            F2.0
    INJURY_SUFFOCATION       F2.0
    INTENT_ASSAULT           F2.0
    INTENT_SELF_HARM         F2.0
    INTENT_UNINTENTIONAL     F2.0
    KEY_ED                   F16.0
    MULTINJURY               F2.0
    NDX                      F3.0
    NECODE                   F3.0
    NEDS_STRATUM             F5.0
    PAY1                     F2.0
    PAY2                     F2.0
    PL_NCHS2006              F3.0
    TOTCHG_ED                F12.2
    YEAR                     F4.0
    ZIPINC_QRTL              F2.0
.

/*  Assign labels to the data elements */
VARIABLE LABELS 
    AGE                      "Age in years at admission"
    AMONTH                   "Admission month"
    AWEEKEND                 "Admission day is a weekend"
    CHRON1                   "Chronic condition indicator 1"
    CHRON2                   "Chronic condition indicator 2"
    CHRON3                   "Chronic condition indicator 3"
    CHRON4                   "Chronic condition indicator 4"
    CHRON5                   "Chronic condition indicator 5"
    CHRON6                   "Chronic condition indicator 6"
    CHRON7                   "Chronic condition indicator 7"
    CHRON8                   "Chronic condition indicator 8"
    CHRON9                   "Chronic condition indicator 9"
    CHRON10                  "Chronic condition indicator 10"
    CHRON11                  "Chronic condition indicator 11"
    CHRON12                  "Chronic condition indicator 12"
    CHRON13                  "Chronic condition indicator 13"
    CHRON14                  "Chronic condition indicator 14"
    CHRON15                  "Chronic condition indicator 15"
    DIED_VISIT               "Died in the ED (1), Died in the hospital (2), did not die (0)"
    DISCWT                   "Weight to ED Visits in AHA universe"
    DISP_ED                  "Disposition of patient (uniform) from ED"
    DQTR                     "Discharge quarter"
    DX1                      "Diagnosis 1"
    DX2                      "Diagnosis 2"
    DX3                      "Diagnosis 3"
    DX4                      "Diagnosis 4"
    DX5                      "Diagnosis 5"
    DX6                      "Diagnosis 6"
    DX7                      "Diagnosis 7"
    DX8                      "Diagnosis 8"
    DX9                      "Diagnosis 9"
    DX10                     "Diagnosis 10"
    DX11                     "Diagnosis 11"
    DX12                     "Diagnosis 12"
    DX13                     "Diagnosis 13"
    DX14                     "Diagnosis 14"
    DX15                     "Diagnosis 15"
    DXCCS1                   "CCS: diagnosis 1"
    DXCCS2                   "CCS: diagnosis 2"
    DXCCS3                   "CCS: diagnosis 3"
    DXCCS4                   "CCS: diagnosis 4"
    DXCCS5                   "CCS: diagnosis 5"
    DXCCS6                   "CCS: diagnosis 6"
    DXCCS7                   "CCS: diagnosis 7"
    DXCCS8                   "CCS: diagnosis 8"
    DXCCS9                   "CCS: diagnosis 9"
    DXCCS10                  "CCS: diagnosis 10"
    DXCCS11                  "CCS: diagnosis 11"
    DXCCS12                  "CCS: diagnosis 12"
    DXCCS13                  "CCS: diagnosis 13"
    DXCCS14                  "CCS: diagnosis 14"
    DXCCS15                  "CCS: diagnosis 15"
    ECODE1                   "E code 1"
    ECODE2                   "E code 2"
    ECODE3                   "E code 3"
    ECODE4                   "E code 4"
    EDEVENT                  "Type of ED Event"
    E_CCS1                   "CCS: E Code 1"
    E_CCS2                   "CCS: E Code 2"
    E_CCS3                   "CCS: E Code 3"
    E_CCS4                   "CCS: E Code 4"
    FEMALE                   "Indicator of sex"
    HCUPFILE                 "Source of HCUP Record (SID or SEDD)"
    HOSP_ED                  "HCUP ED hospital identifier"
    INJURY                   "Injury diagnosis reported on record (1:DX1 is an injury; 2:DX2+ is an injury; 0:No injury)"
    INJURY_CUT               "Injury by cutting or piercing (by E codes)"
    INJURY_DROWN             "Injury by drowning or submersion (by E codes)"
    INJURY_FALL              "Injury by falling (by E codes)"
    INJURY_FIRE              "Injury by fire, flame or hot object (by E codes)"
    INJURY_FIREARM           "Injury by firearm (by E codes)"
    INJURY_MACHINERY         "Injury by machinery (by E codes)"
    INJURY_MVT               "Injury involving motor vehicle traffic (by E codes)"
    INJURY_NATURE            "Injury involving nature or environmental factors (by E codes)"
    INJURY_POISON            "Injury by poison (by E codes)"
    INJURY_SEVERITY          "Injury severity score assigned by ICDPIC Stata program"
    INJURY_STRUCK            "Injury from being struck by or against (by E codes)"
    INJURY_SUFFOCATION       "Injury by suffocation (by E codes)"
    INTENT_ASSAULT           "Injury by assault indicated on the record (by E codes)"
    INTENT_SELF_HARM         "Intentional self harm indicated on the record (by diagnosis and/or E codes)"
    INTENT_UNINTENTIONAL     "Unintentional injury indicated on the record (by E codes)"
    KEY_ED                   "HCUP NEDS record identifier"
    MULTINJURY               "More than one injury diagnosis reported on record"
    NDX                      "Number of diagnoses on this record"
    NECODE                   "Number of E codes on this record"
    NEDS_STRATUM             "Stratum used to sample hospital"
    PAY1                     "Primary expected payer (uniform)"
    PAY2                     "Secondary expected payer (uniform)"
    PL_NCHS2006              "Patient Location: NCHS Urban-Rural Code (V2006)"
    TOTCHG_ED                "Total charge for ED services"
    YEAR                     "Calendar year"
    ZIPINC_QRTL              "Median household income national quartile for patient ZIP Code" .

/* Convert special values to system missing values */
RECODE AGE                      (-99 -88 -66=SYSMIS).
RECODE AMONTH                   (-9 -8 -6 -5=SYSMIS).
RECODE AWEEKEND                 (-9 -8 -6 -5=SYSMIS).
RECODE CHRON1                   (-99 -88 -66=SYSMIS).
RECODE CHRON2                   (-99 -88 -66=SYSMIS).
RECODE CHRON3                   (-99 -88 -66=SYSMIS).
RECODE CHRON4                   (-99 -88 -66=SYSMIS).
RECODE CHRON5                   (-99 -88 -66=SYSMIS).
RECODE CHRON6                   (-99 -88 -66=SYSMIS).
RECODE CHRON7                   (-99 -88 -66=SYSMIS).
RECODE CHRON8                   (-99 -88 -66=SYSMIS).
RECODE CHRON9                   (-99 -88 -66=SYSMIS).
RECODE CHRON10                  (-99 -88 -66=SYSMIS).
RECODE CHRON11                  (-99 -88 -66=SYSMIS).
RECODE CHRON12                  (-99 -88 -66=SYSMIS).
RECODE CHRON13                  (-99 -88 -66=SYSMIS).
RECODE CHRON14                  (-99 -88 -66=SYSMIS).
RECODE CHRON15                  (-99 -88 -66=SYSMIS).
RECODE DIED_VISIT               (-9 -8 -6 -5=SYSMIS).
RECODE DISCWT                   (-99.9999999 -88.8888888 -66.6666666=SYSMIS).
RECODE DISP_ED                  (-9 -8 -6 -5=SYSMIS).
RECODE DQTR                     (-9 -8 -6 -5=SYSMIS).
RECODE DXCCS1                   (-99 -88 -66=SYSMIS).
RECODE DXCCS2                   (-99 -88 -66=SYSMIS).
RECODE DXCCS3                   (-99 -88 -66=SYSMIS).
RECODE DXCCS4                   (-99 -88 -66=SYSMIS).
RECODE DXCCS5                   (-99 -88 -66=SYSMIS).
RECODE DXCCS6                   (-99 -88 -66=SYSMIS).
RECODE DXCCS7                   (-99 -88 -66=SYSMIS).
RECODE DXCCS8                   (-99 -88 -66=SYSMIS).
RECODE DXCCS9                   (-99 -88 -66=SYSMIS).
RECODE DXCCS10                  (-99 -88 -66=SYSMIS).
RECODE DXCCS11                  (-99 -88 -66=SYSMIS).
RECODE DXCCS12                  (-99 -88 -66=SYSMIS).
RECODE DXCCS13                  (-99 -88 -66=SYSMIS).
RECODE DXCCS14                  (-99 -88 -66=SYSMIS).
RECODE DXCCS15                  (-99 -88 -66=SYSMIS).
RECODE EDEVENT                  (-9 -8 -6 -5=SYSMIS).
RECODE E_CCS1                   (-999 -888 -666=SYSMIS).
RECODE E_CCS2                   (-999 -888 -666=SYSMIS).
RECODE E_CCS3                   (-999 -888 -666=SYSMIS).
RECODE E_CCS4                   (-999 -888 -666=SYSMIS).
RECODE FEMALE                   (-9 -8 -6 -5=SYSMIS).
RECODE HOSP_ED                  (-9999 -8888 -6666=SYSMIS).
RECODE INJURY                   (-9 -8 -6 -5=SYSMIS).
RECODE INJURY_CUT               (-9 -8 -6 -5=SYSMIS).
RECODE INJURY_DROWN             (-9 -8 -6 -5=SYSMIS).
RECODE INJURY_FALL              (-9 -8 -6 -5=SYSMIS).
RECODE INJURY_FIRE              (-9 -8 -6 -5=SYSMIS).
RECODE INJURY_FIREARM           (-9 -8 -6 -5=SYSMIS).
RECODE INJURY_MACHINERY         (-9 -8 -6 -5=SYSMIS).
RECODE INJURY_MVT               (-9 -8 -6 -5=SYSMIS).
RECODE INJURY_NATURE            (-9 -8 -6 -5=SYSMIS).
RECODE INJURY_POISON            (-9 -8 -6 -5=SYSMIS).
RECODE INJURY_SEVERITY          (-9 -8 -6 -5=SYSMIS).
RECODE INJURY_STRUCK            (-9 -8 -6 -5=SYSMIS).
RECODE INJURY_SUFFOCATION       (-9 -8 -6 -5=SYSMIS).
RECODE INTENT_ASSAULT           (-9 -8 -6 -5=SYSMIS).
RECODE INTENT_SELF_HARM         (-9 -8 -6 -5=SYSMIS).
RECODE INTENT_UNINTENTIONAL     (-9 -8 -6 -5=SYSMIS).
RECODE KEY_ED                   (-999999999999999 -888888888888888 -666666666666666=SYSMIS).
RECODE MULTINJURY               (-9 -8 -6 -5=SYSMIS).
RECODE NDX                      (-99 -88 -66=SYSMIS).
RECODE NECODE                   (-99 -88 -66=SYSMIS).
RECODE NEDS_STRATUM             (-9999 -8888 -6666=SYSMIS).
RECODE PAY1                     (-9 -8 -6 -5=SYSMIS).
RECODE PAY2                     (-9 -8 -6 -5=SYSMIS).
RECODE PL_NCHS2006              (-99 -88 -66=SYSMIS).
RECODE TOTCHG_ED                (-99999999.99 -88888888.88 -66666666.66=SYSMIS).
RECODE YEAR                     (-999 -888 -666=SYSMIS).
RECODE ZIPINC_QRTL              (-9 -8 -6 -5=SYSMIS).

SAVE OUTFILE = 'NEDS_2012_Core.SAV' / COMPRESSED.