# ies_modifier
IES File Modifier Web Tool - User Guide
Overview
The IES File Modifier Web Tool is designed to process and modify IES photometric files based on:
Chip Efficiency Multiplier - Adjusts the light output (lumens) based on LED efficiency.
New Luminaire Length - Scales the light output and power consumption based on a user-defined length.
Refinement Option - Allows users to fine-tune lumens per metre and adjust power accordingly.
Key Features
✅ Upload and modify an IES file ✅ Adjust zonal lumens based on LED efficiency multiplier ✅ Scale power and light output for different luminaire lengths ✅ Compute and update lumens per metre & lumens per watt in the [TEST] field ✅ Fine-tune lumens per metre and auto-adjust power ✅ Download the updated IES file

How to Use the Tool
1. Upload an IES File
Click the "Upload IES File" button and select an IES file from your computer.
The tool assumes the uploaded IES file is for a 1-metre luminaire.
2. Adjust Light Output
Enter the Chip Efficiency Multiplier:
1.0 → No change
1.15 → Increases lumens by 15%
Enter the New Luminaire Length (in metres):
Example: 12.05 → Adjusts luminaire length to 12.05m
3. Download the Modified IES File
Click "Download Modified IES File" to save the updated file.
The following changes are applied:
Zonal lumens scaled based on length & efficiency multiplier.
Power scaled based on luminaire length.
[TEST] field updated with lumens per metre & lumens per watt.
Luminaire name updated with new power and length.
4. Refining the Output (Optional)
If the lumens per metre is too high or low, enter your desired lumens per metre.
Click "Refine and Download" to scale power and zonal lumens accordingly.

Example: Before & After Modifications
🔹 Original IES File (1m Luminaire)
[TEST]
[LUMINAIRE] Bline 858D 24.3W - 80CRI - 4000K
1 1 24.3
🔹 Modified IES File (12.05m Luminaire, 15% Efficiency Increase)
[TEST] 1.15/1754.8/108.3
[LUMINAIRE] Bline 858D 293.2W (12.05) 80+CRI 4000K
1 1 293.2

Technical Details
The [TEST] field now contains:
Chip Efficiency Multiplier (1.15 for 15%)
Lumens per metre (Total Lumens ÷ Length)
Lumens per Watt (Total Lumens ÷ Power)
Power is only scaled based on length, not efficiency increase.
The tool maintains the integrity of the IES format.

Troubleshooting
Issue: "File not modifying correctly" → Ensure the uploaded IES file is properly formatted.
Issue: "Unexpected values in TEST field" → Check input multipliers for accuracy.
Issue: "Download not working" → Refresh the page and try again.

Future Enhancements
🔹 Add batch processing for multiple IES files.
🔹 Deploy as a hosted web app that allows users to download corrected ies files based on their selections.
🔹 Include a 3D visualiser for beam distribution validation.

Developed for Internal Use - Evolt Manufacturing
This software is developed exclusively for the internal use of experienced and qualified lighting engineers at Evolt Manufacturing. This is Intellectual Property of Evolt and as such is proprietary and confidential.
Any unauthorised sharing, distribution, or disclosure of its contents is strictly prohibited.



