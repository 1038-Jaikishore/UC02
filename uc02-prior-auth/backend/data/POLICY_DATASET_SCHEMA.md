# Medical Policy Dataset Schema

This document profiles all discovered medical policy PDF documents in the system repository, establishing document structure, page counts, CPT/HCPCS codes, and parsing viability for downstream RAG extraction.

## Dataset Summary

- **Anthem policies**: 13
- **UHC policies**: 16
- **Total policies**: 29
- **Total pages**: 268

## Policy Inventory Table

| Payer | Filename | Relative Path | Pages | Policy Title | Policy ID | Effective Date | CPT Codes | HCPCS Codes | Sections | Extraction Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Anthem | ADMIN.00006 Review of Services for Benefit Determinations in the Absence of a Company Applicable Medical Policy or Clinical Utilization Management (UM) Guideline.pdf | anthem/ADMIN.00006 Review of Services for Benefit Determinations in the Absence of a Company Applicable Medical Policy or Clinical Utilization Management (UM) Guideline.pdf | 9 | Medical Policy | ADMIN.00006 | unknown | none | none | Definitions, Description, Exclusions, Medical Necessity... | SUCCESS |
| Anthem | CG-DME-21 External Infusion Pumps for the Administration of Drugs in the Home or Residential Care Settings.pdf | anthem/CG-DME-21 External Infusion Pumps for the Administration of Drugs in the Home or Residential Care Settings.pdf | 4 | Clinical UM Guideline | CG-DME-21 | unknown | none | A4221, A4222, E0776, E0779, E0780... | Clinical Indications, Coding Section, Definitions, Description... | SUCCESS |
| Anthem | CG-MED-57 Cardiac Stress Testing with Electrocardiogram.pdf | anthem/CG-MED-57 Cardiac Stress Testing with Electrocardiogram.pdf | 11 | Clinical UM Guideline | CG-MED-57 | unknown | 05158, 93015, 93016, 93017, 93018 | none | Clinical Indications, Coding Section, Definitions, Description... | SUCCESS |
| Anthem | CG-MED-62 Resting Electrocardiogram Screening in Adults.pdf | anthem/CG-MED-62 Resting Electrocardiogram Screening in Adults.pdf | 4 | Clinical UM Guideline | CG-MED-62 | unknown | 93000, 93005, 93010 | G0403, G0404, G0405 | Clinical Indications, Coding Section, Definitions, Description... | SUCCESS |
| Anthem | CG-RAD-31 Three-Dimensional (3-D) Rendering of Imaging Studies.pdf | anthem/CG-RAD-31 Three-Dimensional (3-D) Rendering of Imaging Studies.pdf | 8 | Clinical UM Guideline | CG-RAD-31 | unknown | 00038, 76376, 76377 | none | Clinical Indications, Definitions, Description, Medical Necessity... | SUCCESS |
| Anthem | CG-SURG-25 Injection Treatment for Morton Neuroma.pdf | anthem/CG-SURG-25 Injection Treatment for Morton Neuroma.pdf | 7 | Clinical UM Guideline | CG-SURG-25 | unknown | 64455, 64632 | S2135 | Clinical Indications, Coding Section, Description, Medical Necessity... | SUCCESS |
| Anthem | CG-SURG-83 Bariatric Surgery and Other Treatments for Clinically Severe Obesity.pdf | anthem/CG-SURG-83 Bariatric Surgery and Other Treatments for Clinically Severe Obesity.pdf | 33 | Clinical UM Guideline | CG-SURG-83 | unknown | 00024, 00797, 01434, 10178, 10350, 10505, 37242, 43290... | C9784, C9785, E1332, E1340, S0016 | Clinical Indications, Coding Section, Definitions, Description... | SUCCESS |
| Anthem | RAD.00057 Near-Infrared Coronary Imaging and Near-Infrared Intravascular Ultrasound Coronary Imaging.pdf | anthem/RAD.00057 Near-Infrared Coronary Imaging and Near-Infrared Intravascular Ultrasound Coronary Imaging.pdf | 7 | Medical Policy | RAD.00057 | unknown | 00057, 10209, 93799 | none | Coding Section, Definitions, Description, Exclusions... | SUCCESS |
| Anthem | SURG.00071 Percutaneous Spinal Surgery.pdf | anthem/SURG.00071 Percutaneous Spinal Surgery.pdf | 15 | Medical Policy | SURG.00071 | unknown | 00052, 00071, 00073, 00111, 00134, 22899, 62287, 62330... | C2614, C9729, S2348 | Coding Section, Definitions, Description, Exclusions... | SUCCESS |
| Anthem | SURG.00111 Axial Lumbar Interbody Fusion.pdf | anthem/SURG.00111 Axial Lumbar Interbody Fusion.pdf | 6 | Medical Policy | SURG.00111 | unknown | 00071, 00111, 22586, 22899 | E1296, E1301 | Coding Section, Definitions, Description, Exclusions... | SUCCESS |
| Anthem | SURG.00132 Drug-Eluting Devices for Maintaining Sinus Ostial Patency.pdf | anthem/SURG.00132 Drug-Eluting Devices for Maintaining Sinus Ostial Patency.pdf | 12 | Medical Policy | SURG.00132 | unknown | 00089, 00132, 31299 | C1874, C2625, C9122, J3490, J7401... | Coding Section, Definitions, Description, Exclusions... | SUCCESS |
| Anthem | SURG.00139 Intraoperative Assessment of Surgical Margins During Breast-Conserving Surgery with Radiofrequency Spectroscopy or Optical Coherence Tomography.pdf | anthem/SURG.00139 Intraoperative Assessment of Surgical Margins During Breast-Conserving Surgery with Radiofrequency Spectroscopy or Optical Coherence Tomography.pdf | 8 | Medical Policy | SURG.00139 | unknown | 00023, 00139 | none | Coding Section, Definitions, Description, Exclusions... | SUCCESS |
| Anthem | SURG.00153 Cardiac Contractility Modulation Therapy.pdf | anthem/SURG.00153 Cardiac Contractility Modulation Therapy.pdf | 8 | Medical Policy | SURG.00153 | unknown | 00153 | C1824, K1030 | Coding Section, Definitions, Description, Exclusions... | SUCCESS |
| Uhc | antiemetics-oncology.pdf | uhc/antiemetics-oncology.pdf | 10 | Antiemetics for Oncology | unknown | October 1, 2025 | none | J0185, J1434, J1453, J1454, J1456... | Definitions, Description, Medical Necessity, References | SUCCESS |
| Uhc | cardiology-procedures-evicore-ohp.pdf | uhc/cardiology-procedures-evicore-ohp.pdf | 8 | Outpatient Cardiology Procedures for EviCore Arrangement (for Oxford Only) | unknown | April 1, 2026 | 75557, 75559, 75561, 75563, 75571, 75572, 75573, 75574... | none | Description, Medical Necessity | SUCCESS |
| Uhc | dme-equipment-orthotics-ostomy-medical-supplies-repairs-replacements.pdf | uhc/dme-equipment-orthotics-ostomy-medical-supplies-repairs-replacements.pdf | 21 | Durable Medical Equipment, Orthotics, Medical Supplies, and Repairs/Replacements | MP.009 | February 1, 2026 | 10182, 33803 | A8000, A8004, E0465, E0466, E0470... | Coverage Guidelines, Definitions, Description, Exclusions... | SUCCESS |
| Uhc | mri-ct-scan-site-of-service.pdf | uhc/mri-ct-scan-site-of-service.pdf | 7 | Magnetic Resonance Imaging (MRI) and Computed Tomography (CT) Scan – Site of Service | MP.13 | January 1, 2026 | 70336, 70450, 70460, 70470, 70480, 70481, 70482, 70486... | S8037 | Description, References | SUCCESS |
| Uhc | noncontact-warming-therapy-ultrasound-therapy-wounds.pdf | uhc/noncontact-warming-therapy-ultrasound-therapy-wounds.pdf | 14 | Noncontact Warming Therapy, Ultrasound Therapy, and Fluorescence Imaging for Wounds | unknown | August 1, 2026 | 97610 | A6000, E0231, E0232 | Description, References | SUCCESS |
| Uhc | provider-administered-preferred-products (1).pdf | uhc/provider-administered-preferred-products (1).pdf | 3 | Provider Administered Drugs – Preferred Products | unknown | July 1, 2026 | 00703, 00781, 43598, 66302 | J3285 | Coverage Guidelines, Description, Medical Necessity | SUCCESS |
| Uhc | provider-administered-preferred-products.pdf | uhc/provider-administered-preferred-products.pdf | 3 | Provider Administered Drugs – Preferred Products | unknown | July 1, 2026 | 00703, 00781, 43598, 66302 | J3285 | Coverage Guidelines, Description, Medical Necessity | SUCCESS |
| Uhc | radiology-procedures-evicore-ohp.pdf | uhc/radiology-procedures-evicore-ohp.pdf | 9 | Outpatient Radiology Procedures for EviCore Arrangement (for Oxford Only) | unknown | April 1, 2026 | 70336, 70450, 70460, 70470, 70472, 70473, 70480, 70481... | C8937, G0235, G0252, S8037, S8080 | Description | SUCCESS |
| Uhc | sleep-studies.pdf | uhc/sleep-studies.pdf | 18 | Sleep Studies | unknown | July 1, 2026 | 55426, 95782, 95783, 95800, 95801, 95803, 95805, 95806... | G0398, G0399, G0400 | Definitions, Description, Medical Necessity, References | SUCCESS |
| Uhc | surgery-ankle.pdf | uhc/surgery-ankle.pdf | 5 | Surgery of the Ankle | unknown | July 1, 2026 | 27685, 27702, 28446, 29891, 29892, 29894, 29895, 29897... | none | Description, Medical Necessity, References | SUCCESS |
| Uhc | surgery-elbow.pdf | uhc/surgery-elbow.pdf | 3 | Surgery of the Elbow | unknown | August 1, 2026 | 24360, 24361, 24362, 24363, 24365, 24366, 24370, 24371... | none | Description, Medical Necessity | SUCCESS |
| Uhc | surgery-foot.pdf | uhc/surgery-foot.pdf | 7 | Surgery of the Foot | unknown | January 1, 2026 | 28285, 28289, 28291, 28292, 28295, 28296, 28297, 28298... | none | Definitions, Description, Medical Necessity, References | SUCCESS |
| Uhc | surgery-hand-wrist.pdf | uhc/surgery-hand-wrist.pdf | 3 | Surgery of the Wrist or Thumb | unknown | August 1, 2026 | 25441, 25442, 25443, 25444, 25445, 25446, 25449, 26530... | none | Description, Medical Necessity | SUCCESS |
| Uhc | surgery-hip.pdf | uhc/surgery-hip.pdf | 9 | Surgery of the Hip | unknown | March 1, 2026 | 27120, 27125, 27130, 27132, 27134, 27137, 27138, 27299... | S2118 | Definitions, Description, Medical Necessity, References | SUCCESS |
| Uhc | surgery-knee.pdf | uhc/surgery-knee.pdf | 10 | Surgery of the Knee | unknown | June 1, 2026 | 27412, 27415, 27416, 27418, 27437, 27438, 27440, 27441... | G0428, J7330, S2112 | Definitions, Description, Medical Necessity, References | SUCCESS |
| Uhc | surgery-shoulder.pdf | uhc/surgery-shoulder.pdf | 6 | Surgery of the Shoulder | unknown | January 1, 2026 | 00392, 23470, 23472, 23473, 23474, 29805, 29806, 29807... | S1058 | Description, Medical Necessity, References | SUCCESS |

## Document Metadata Details

### Anthem: ADMIN.00006 Review of Services for Benefit Determinations in the Absence of a Company Applicable Medical Policy or Clinical Utilization Management (UM) Guideline.pdf

- **Relative Path**: `anthem/ADMIN.00006 Review of Services for Benefit Determinations in the Absence of a Company Applicable Medical Policy or Clinical Utilization Management (UM) Guideline.pdf`
- **Page Count**: 9
- **Policy Title**: Medical Policy
- **Policy ID**: ADMIN.00006
- **Effective Date**: unknown
- **Revision Date**: 08/07/2025
- **CPT Reference Codes**: `[]`
- **HCPCS Reference Codes**: `[]`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Definitions', 'Description', 'Exclusions', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Anthem: CG-DME-21 External Infusion Pumps for the Administration of Drugs in the Home or Residential Care Settings.pdf

- **Relative Path**: `anthem/CG-DME-21 External Infusion Pumps for the Administration of Drugs in the Home or Residential Care Settings.pdf`
- **Page Count**: 4
- **Policy Title**: Clinical UM Guideline
- **Policy ID**: CG-DME-21
- **Effective Date**: unknown
- **Revision Date**: 11/06/2025
- **CPT Reference Codes**: `[]`
- **HCPCS Reference Codes**: `['A4221', 'A4222', 'E0776', 'E0779', 'E0780', 'E0781', 'E0791', 'K0552', 'K0601', 'K0605']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Clinical Indications', 'Coding Section', 'Definitions', 'Description', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Anthem: CG-MED-57 Cardiac Stress Testing with Electrocardiogram.pdf

- **Relative Path**: `anthem/CG-MED-57 Cardiac Stress Testing with Electrocardiogram.pdf`
- **Page Count**: 11
- **Policy Title**: Clinical UM Guideline
- **Policy ID**: CG-MED-57
- **Effective Date**: unknown
- **Revision Date**: 05/14/2026
- **CPT Reference Codes**: `['05158', '93015', '93016', '93017', '93018']`
- **HCPCS Reference Codes**: `[]`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Clinical Indications', 'Coding Section', 'Definitions', 'Description', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Anthem: CG-MED-62 Resting Electrocardiogram Screening in Adults.pdf

- **Relative Path**: `anthem/CG-MED-62 Resting Electrocardiogram Screening in Adults.pdf`
- **Page Count**: 4
- **Policy Title**: Clinical UM Guideline
- **Policy ID**: CG-MED-62
- **Effective Date**: unknown
- **Revision Date**: 08/07/2025
- **CPT Reference Codes**: `['93000', '93005', '93010']`
- **HCPCS Reference Codes**: `['G0403', 'G0404', 'G0405']`
- **ICD Reference Codes**: `['Z00.00']`
- **Sections Detected**: ['Clinical Indications', 'Coding Section', 'Definitions', 'Description', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Anthem: CG-RAD-31 Three-Dimensional (3-D) Rendering of Imaging Studies.pdf

- **Relative Path**: `anthem/CG-RAD-31 Three-Dimensional (3-D) Rendering of Imaging Studies.pdf`
- **Page Count**: 8
- **Policy Title**: Clinical UM Guideline
- **Policy ID**: CG-RAD-31
- **Effective Date**: unknown
- **Revision Date**: 08/07/2025
- **CPT Reference Codes**: `['00038', '76376', '76377']`
- **HCPCS Reference Codes**: `[]`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Clinical Indications', 'Definitions', 'Description', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Anthem: CG-SURG-25 Injection Treatment for Morton Neuroma.pdf

- **Relative Path**: `anthem/CG-SURG-25 Injection Treatment for Morton Neuroma.pdf`
- **Page Count**: 7
- **Policy Title**: Clinical UM Guideline
- **Policy ID**: CG-SURG-25
- **Effective Date**: unknown
- **Revision Date**: 05/14/2026
- **CPT Reference Codes**: `['64455', '64632']`
- **HCPCS Reference Codes**: `['S2135']`
- **ICD Reference Codes**: `['G57.60', 'G57.61', 'G57.62', 'G57.63']`
- **Sections Detected**: ['Clinical Indications', 'Coding Section', 'Description', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Anthem: CG-SURG-83 Bariatric Surgery and Other Treatments for Clinically Severe Obesity.pdf

- **Relative Path**: `anthem/CG-SURG-83 Bariatric Surgery and Other Treatments for Clinically Severe Obesity.pdf`
- **Page Count**: 33
- **Policy Title**: Clinical UM Guideline
- **Policy ID**: CG-SURG-83
- **Effective Date**: unknown
- **Revision Date**: 11/06/2025
- **CPT Reference Codes**: `['00024', '00797', '01434', '10178', '10350', '10505', '37242', '43290', '43291', '43632', '43633', '43644', '43645', '43659', '43770', '43771', '43772', '43773', '43774', '43775', '43842', '43843', '43845', '43846', '43847', '43848', '43886', '43887', '43888', '43889', '43999', '44238', '64999']`
- **HCPCS Reference Codes**: `['C9784', 'C9785', 'E1332', 'E1340', 'S0016']`
- **ICD Reference Codes**: `['E66.01', 'E66.09', 'E66.1', 'E66.2', 'E66.3', 'E66.8', 'E66.89', 'E66.9', 'E88.82', 'Z46.51', 'Z68.20', 'Z68.29', 'Z68.30', 'Z68.34', 'Z68.35', 'Z68.39', 'Z68.41', 'Z68.45', 'Z68.51', 'Z68.56', 'Z98.84']`
- **Sections Detected**: ['Clinical Indications', 'Coding Section', 'Definitions', 'Description', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Anthem: RAD.00057 Near-Infrared Coronary Imaging and Near-Infrared Intravascular Ultrasound Coronary Imaging.pdf

- **Relative Path**: `anthem/RAD.00057 Near-Infrared Coronary Imaging and Near-Infrared Intravascular Ultrasound Coronary Imaging.pdf`
- **Page Count**: 7
- **Policy Title**: Medical Policy
- **Policy ID**: RAD.00057
- **Effective Date**: unknown
- **Revision Date**: 08/07/2025
- **CPT Reference Codes**: `['00057', '10209', '93799']`
- **HCPCS Reference Codes**: `[]`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Coding Section', 'Definitions', 'Description', 'Exclusions', 'References']
- **Extraction Status**: `SUCCESS`

---

### Anthem: SURG.00071 Percutaneous Spinal Surgery.pdf

- **Relative Path**: `anthem/SURG.00071 Percutaneous Spinal Surgery.pdf`
- **Page Count**: 15
- **Policy Title**: Medical Policy
- **Policy ID**: SURG.00071
- **Effective Date**: unknown
- **Revision Date**: 05/14/2026
- **CPT Reference Codes**: `['00052', '00071', '00073', '00111', '00134', '22899', '62287', '62330', '62331', '62380', '64999']`
- **HCPCS Reference Codes**: `['C2614', 'C9729', 'S2348']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Coding Section', 'Definitions', 'Description', 'Exclusions', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Anthem: SURG.00111 Axial Lumbar Interbody Fusion.pdf

- **Relative Path**: `anthem/SURG.00111 Axial Lumbar Interbody Fusion.pdf`
- **Page Count**: 6
- **Policy Title**: Medical Policy
- **Policy ID**: SURG.00111
- **Effective Date**: unknown
- **Revision Date**: 05/14/2026
- **CPT Reference Codes**: `['00071', '00111', '22586', '22899']`
- **HCPCS Reference Codes**: `['E1296', 'E1301']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Coding Section', 'Definitions', 'Description', 'Exclusions', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Anthem: SURG.00132 Drug-Eluting Devices for Maintaining Sinus Ostial Patency.pdf

- **Relative Path**: `anthem/SURG.00132 Drug-Eluting Devices for Maintaining Sinus Ostial Patency.pdf`
- **Page Count**: 12
- **Policy Title**: Medical Policy
- **Policy ID**: SURG.00132
- **Effective Date**: unknown
- **Revision Date**: 02/19/2026
- **CPT Reference Codes**: `['00089', '00132', '31299']`
- **HCPCS Reference Codes**: `['C1874', 'C2625', 'C9122', 'J3490', 'J7401', 'J7402', 'L8699', 'S1090', 'S1091']`
- **ICD Reference Codes**: `['J33.0', 'J33.9']`
- **Sections Detected**: ['Coding Section', 'Definitions', 'Description', 'Exclusions', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Anthem: SURG.00139 Intraoperative Assessment of Surgical Margins During Breast-Conserving Surgery with Radiofrequency Spectroscopy or Optical Coherence Tomography.pdf

- **Relative Path**: `anthem/SURG.00139 Intraoperative Assessment of Surgical Margins During Breast-Conserving Surgery with Radiofrequency Spectroscopy or Optical Coherence Tomography.pdf`
- **Page Count**: 8
- **Policy Title**: Medical Policy
- **Policy ID**: SURG.00139
- **Effective Date**: unknown
- **Revision Date**: 02/19/2026
- **CPT Reference Codes**: `['00023', '00139']`
- **HCPCS Reference Codes**: `[]`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Coding Section', 'Definitions', 'Description', 'Exclusions', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Anthem: SURG.00153 Cardiac Contractility Modulation Therapy.pdf

- **Relative Path**: `anthem/SURG.00153 Cardiac Contractility Modulation Therapy.pdf`
- **Page Count**: 8
- **Policy Title**: Medical Policy
- **Policy ID**: SURG.00153
- **Effective Date**: unknown
- **Revision Date**: 08/07/2025
- **CPT Reference Codes**: `['00153']`
- **HCPCS Reference Codes**: `['C1824', 'K1030']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Coding Section', 'Definitions', 'Description', 'Exclusions', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Uhc: antiemetics-oncology.pdf

- **Relative Path**: `uhc/antiemetics-oncology.pdf`
- **Page Count**: 10
- **Policy Title**: Antiemetics for Oncology
- **Policy ID**: unknown
- **Effective Date**: October 1, 2025
- **Revision Date**: unknown
- **CPT Reference Codes**: `[]`
- **HCPCS Reference Codes**: `['J0185', 'J1434', 'J1453', 'J1454', 'J1456', 'J1626', 'J1627', 'J2405', 'J2468', 'J2469', 'J8501', 'J8655', 'J8670', 'Q0162', 'Q0166']`
- **ICD Reference Codes**: `['R11.0', 'R11.10', 'R11.16', 'R11.2', 'Z51.11']`
- **Sections Detected**: ['Definitions', 'Description', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Uhc: cardiology-procedures-evicore-ohp.pdf

- **Relative Path**: `uhc/cardiology-procedures-evicore-ohp.pdf`
- **Page Count**: 8
- **Policy Title**: Outpatient Cardiology Procedures for EviCore Arrangement (for Oxford Only)
- **Policy ID**: unknown
- **Effective Date**: April 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['75557', '75559', '75561', '75563', '75571', '75572', '75573', '75574', '75580', '78451', '78452', '78453', '78454', '78459', '78491', '78492', '93350', '93351', '93451', '93452', '93453', '93454', '93455', '93456', '93457', '93458', '93459', '93460', '93461']`
- **HCPCS Reference Codes**: `[]`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Description', 'Medical Necessity']
- **Extraction Status**: `SUCCESS`

---

### Uhc: dme-equipment-orthotics-ostomy-medical-supplies-repairs-replacements.pdf

- **Relative Path**: `uhc/dme-equipment-orthotics-ostomy-medical-supplies-repairs-replacements.pdf`
- **Page Count**: 21
- **Policy Title**: Durable Medical Equipment, Orthotics, Medical Supplies, and Repairs/Replacements
- **Policy ID**: MP.009
- **Effective Date**: February 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['10182', '33803']`
- **HCPCS Reference Codes**: `['A8000', 'A8004', 'E0465', 'E0466', 'E0470', 'E0471', 'S1040']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Coverage Guidelines', 'Definitions', 'Description', 'Exclusions', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Uhc: mri-ct-scan-site-of-service.pdf

- **Relative Path**: `uhc/mri-ct-scan-site-of-service.pdf`
- **Page Count**: 7
- **Policy Title**: Magnetic Resonance Imaging (MRI) and Computed Tomography (CT) Scan – Site of Service
- **Policy ID**: MP.13
- **Effective Date**: January 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['70336', '70450', '70460', '70470', '70480', '70481', '70482', '70486', '70487', '70488', '70490', '70491', '70492', '70496', '70498', '70540', '70542', '70543', '70544', '70545', '70546', '70547', '70548', '70549', '70551', '70552', '70553', '70554', '70555', '71250', '71260', '71270', '71271', '71275', '71550', '71551', '71552', '71555', '72125', '72126', '72127', '72128', '72129', '72130', '72131', '72132', '72133', '72141', '72142', '72146', '72147', '72148', '72149', '72156', '72157', '72158', '72159', '72191', '72192', '72193', '72194', '72195', '72196', '72197', '72198', '73200', '73201', '73202', '73206', '73218', '73219', '73220', '73221', '73222', '73223', '73225', '73700', '73701', '73702', '73706', '73718', '73719', '73720', '73721', '73722', '73723', '73725', '74150', '74160', '74170', '74174', '74175', '74176', '74177', '74178', '74181', '74182', '74183', '74185', '74261', '74262', '74263', '75557', '75559', '75561', '75563', '75571', '75572', '75573', '75574', '75635', '76380', '76390', '76497', '76498', '77046', '77047', '77048', '77049', '77084']`
- **HCPCS Reference Codes**: `['S8037']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Description', 'References']
- **Extraction Status**: `SUCCESS`

---

### Uhc: noncontact-warming-therapy-ultrasound-therapy-wounds.pdf

- **Relative Path**: `uhc/noncontact-warming-therapy-ultrasound-therapy-wounds.pdf`
- **Page Count**: 14
- **Policy Title**: Noncontact Warming Therapy, Ultrasound Therapy, and Fluorescence Imaging for Wounds
- **Policy ID**: unknown
- **Effective Date**: August 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['97610']`
- **HCPCS Reference Codes**: `['A6000', 'E0231', 'E0232']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Description', 'References']
- **Extraction Status**: `SUCCESS`

---

### Uhc: provider-administered-preferred-products (1).pdf

- **Relative Path**: `uhc/provider-administered-preferred-products (1).pdf`
- **Page Count**: 3
- **Policy Title**: Provider Administered Drugs – Preferred Products
- **Policy ID**: unknown
- **Effective Date**: July 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['00703', '00781', '43598', '66302']`
- **HCPCS Reference Codes**: `['J3285']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Coverage Guidelines', 'Description', 'Medical Necessity']
- **Extraction Status**: `SUCCESS`

---

### Uhc: provider-administered-preferred-products.pdf

- **Relative Path**: `uhc/provider-administered-preferred-products.pdf`
- **Page Count**: 3
- **Policy Title**: Provider Administered Drugs – Preferred Products
- **Policy ID**: unknown
- **Effective Date**: July 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['00703', '00781', '43598', '66302']`
- **HCPCS Reference Codes**: `['J3285']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Coverage Guidelines', 'Description', 'Medical Necessity']
- **Extraction Status**: `SUCCESS`

---

### Uhc: radiology-procedures-evicore-ohp.pdf

- **Relative Path**: `uhc/radiology-procedures-evicore-ohp.pdf`
- **Page Count**: 9
- **Policy Title**: Outpatient Radiology Procedures for EviCore Arrangement (for Oxford Only)
- **Policy ID**: unknown
- **Effective Date**: April 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['70336', '70450', '70460', '70470', '70472', '70473', '70480', '70481', '70482', '70486', '70487', '70488', '70490', '70491', '70492', '70496', '70498', '70540', '70542', '70543', '70544', '70545', '70546', '70547', '70548', '70549', '70551', '70552', '70553', '70554', '70555', '71250', '71260', '71270', '71271', '71275', '71550', '71551', '71552', '71555', '72125', '72126', '72127', '72128', '72129', '72130', '72131', '72132', '72133', '72141', '72142', '72146', '72147', '72148', '72149', '72156', '72157', '72158', '72159', '72191', '72192', '72193', '72194', '72195', '72196', '72197', '72198', '73200', '73201', '73202', '73206', '73218', '73219', '73220', '73221', '73222', '73223', '73225', '73700', '73701', '73702', '73706', '73718', '73719', '73720', '73721', '73722', '73723', '73725', '74150', '74160', '74170', '74174', '74175', '74176', '74177', '74178', '74181', '74182', '74183', '74185', '74261', '74262', '74263', '75635', '76376', '76377', '76380', '76390', '76391', '76497', '76498', '76499', '76975', '77021', '77046', '77047', '77048', '77049', '77084', '78429', '78430', '78431', '78432', '78433', '78466', '78468', '78469', '78472', '78473', '78481', '78483', '78494', '78496', '78499', '78579', '78608', '78609', '78811', '78812', '78813', '78814', '78815', '78816', '78830']`
- **HCPCS Reference Codes**: `['C8937', 'G0235', 'G0252', 'S8037', 'S8080']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Description']
- **Extraction Status**: `SUCCESS`

---

### Uhc: sleep-studies.pdf

- **Relative Path**: `uhc/sleep-studies.pdf`
- **Page Count**: 18
- **Policy Title**: Sleep Studies
- **Policy ID**: unknown
- **Effective Date**: July 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['55426', '95782', '95783', '95800', '95801', '95803', '95805', '95806', '95807', '95808', '95810', '95811']`
- **HCPCS Reference Codes**: `['G0398', 'G0399', 'G0400']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Definitions', 'Description', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Uhc: surgery-ankle.pdf

- **Relative Path**: `uhc/surgery-ankle.pdf`
- **Page Count**: 5
- **Policy Title**: Surgery of the Ankle
- **Policy ID**: unknown
- **Effective Date**: July 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['27685', '27702', '28446', '29891', '29892', '29894', '29895', '29897', '29898', '29899']`
- **HCPCS Reference Codes**: `[]`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Description', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Uhc: surgery-elbow.pdf

- **Relative Path**: `uhc/surgery-elbow.pdf`
- **Page Count**: 3
- **Policy Title**: Surgery of the Elbow
- **Policy ID**: unknown
- **Effective Date**: August 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['24360', '24361', '24362', '24363', '24365', '24366', '24370', '24371', '29830', '29834', '29835', '29836', '29837', '29838']`
- **HCPCS Reference Codes**: `[]`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Description', 'Medical Necessity']
- **Extraction Status**: `SUCCESS`

---

### Uhc: surgery-foot.pdf

- **Relative Path**: `uhc/surgery-foot.pdf`
- **Page Count**: 7
- **Policy Title**: Surgery of the Foot
- **Policy ID**: unknown
- **Effective Date**: January 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['28285', '28289', '28291', '28292', '28295', '28296', '28297', '28298', '28299', '28899', '29893']`
- **HCPCS Reference Codes**: `[]`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Definitions', 'Description', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Uhc: surgery-hand-wrist.pdf

- **Relative Path**: `uhc/surgery-hand-wrist.pdf`
- **Page Count**: 3
- **Policy Title**: Surgery of the Wrist or Thumb
- **Policy ID**: unknown
- **Effective Date**: August 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['25441', '25442', '25443', '25444', '25445', '25446', '25449', '26530', '26531', '26535', '26536', '29840', '29843', '29844', '29845', '29846', '29847']`
- **HCPCS Reference Codes**: `[]`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Description', 'Medical Necessity']
- **Extraction Status**: `SUCCESS`

---

### Uhc: surgery-hip.pdf

- **Relative Path**: `uhc/surgery-hip.pdf`
- **Page Count**: 9
- **Policy Title**: Surgery of the Hip
- **Policy ID**: unknown
- **Effective Date**: March 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['27120', '27125', '27130', '27132', '27134', '27137', '27138', '27299', '29860', '29861', '29862', '29863', '29914', '29915', '29916', '29999']`
- **HCPCS Reference Codes**: `['S2118']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Definitions', 'Description', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Uhc: surgery-knee.pdf

- **Relative Path**: `uhc/surgery-knee.pdf`
- **Page Count**: 10
- **Policy Title**: Surgery of the Knee
- **Policy ID**: unknown
- **Effective Date**: June 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['27412', '27415', '27416', '27418', '27437', '27438', '27440', '27441', '27442', '27443', '27446', '27447', '27486', '27487', '27658', '27659', '27664', '27665', '29866', '29867', '29868', '29870', '29871', '29873', '29874', '29875', '29876', '29877', '29879', '29880', '29881', '29882', '29883', '29884', '29885', '29886', '29887', '29888', '29889']`
- **HCPCS Reference Codes**: `['G0428', 'J7330', 'S2112']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Definitions', 'Description', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---

### Uhc: surgery-shoulder.pdf

- **Relative Path**: `uhc/surgery-shoulder.pdf`
- **Page Count**: 6
- **Policy Title**: Surgery of the Shoulder
- **Policy ID**: unknown
- **Effective Date**: January 1, 2026
- **Revision Date**: unknown
- **CPT Reference Codes**: `['00392', '23470', '23472', '23473', '23474', '29805', '29806', '29807', '29819', '29820', '29821', '29822', '29823', '29824', '29825', '29826', '29827', '29828', '29999']`
- **HCPCS Reference Codes**: `['S1058']`
- **ICD Reference Codes**: `[]`
- **Sections Detected**: ['Description', 'Medical Necessity', 'References']
- **Extraction Status**: `SUCCESS`

---
