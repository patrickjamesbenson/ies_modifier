import streamlit as st
import re
import io

def modify_ies_file(file_content, efficiency_multiplier, new_length, debug_mode=False):
    lines = file_content.split('\n')
    updated_lines = []
    
    power_line_index = None
    luminaire_line_index = None
    length_line_index = None
    zonal_data_start = None
    original_length = 1.0  # Assume all input files are 1 meter in length
    power = None
    total_lumens = 0

    # **Explicitly Define Angle Rows to Lock**
    ANGLE_LOCK_START = 14
    ANGLE_LOCK_END = 23  # Lock lines 14-23 exactly

    # Step 1: Identify Key Indexes
    for i, line in enumerate(lines):
        if "[LUMINAIRE]" in line:
            luminaire_line_index = i
        elif line.startswith("1 1 "):
            power = float(line.split()[2])
            power_line_index = i
        elif "TILT=NONE" in line:
            length_line_index = i + 1  # Length is right after TILT=NONE
        elif i == ANGLE_LOCK_END + 1:
            zonal_data_start = i  # **First row AFTER angles is zonal lumens**
            break  # Stop searching after this point
        updated_lines.append(line)

    # Step 2: Adjust Power for New Length
    new_power = round(power * (new_length / original_length), 1)
    if power_line_index is not None:
        updated_lines[power_line_index] = f"1 1 {new_power}"

    # Step 3: Update Luminaire Line (Add New Length Before Watts)
    if luminaire_line_index is not None:
        updated_lines[luminaire_line_index] = re.sub(r"(\d+\.\d+)W", f"{new_length:.3f}m {new_power}W", updated_lines[luminaire_line_index])

    # Step 4: Update Length in Line 12
    if length_line_index is not None and len(updated_lines) > length_line_index:
        parts = updated_lines[length_line_index].split()
        if len(parts) > 8:
            parts[8] = f"{new_length:.3f}"
            updated_lines[length_line_index] = " ".join(parts)

    # **Step 5: Lock Lines 14-23 Exactly**
    for i in range(ANGLE_LOCK_START, ANGLE_LOCK_END + 1):
        updated_lines[i] = lines[i]  # **Preserve angles 100% exactly**

    # **Step 6: Modify ONLY Zonal Lumens (Lines After Angles)**
    if zonal_data_start is not None:
        for i, line in enumerate(lines[zonal_data_start:], start=zonal_data_start):
            values = re.split(r'(\s+)', line)  # Preserve spacing
            modified = False

            for j in range(len(values)):
                if values[j].strip().replace('.', '', 1).isdigit():  # Modify only numerical lumen values
                    values[j] = f"{float(values[j]) * efficiency_multiplier * (new_length / original_length):.1f}"
                    modified = True

            if modified:
                total_lumens += sum(float(v) for v in values if v.strip().replace('.', '', 1).isdigit())
                updated_lines.append("".join(values))
            else:
                updated_lines.append(line)  # Preserve any non-numeric lines

    # **Step 7: Update [TEST] Field with Correct Data**
    test_field = f"{efficiency_multiplier:.3f}/{total_lumens:.1f}/{new_power:.1f}"
    if len(updated_lines) > 1:
        updated_lines[1] = f"[TEST] {test_field}"

    return "\n".join(updated_lines)

# Streamlit UI
st.title("IES File Modifier Web Tool")

uploaded_file = st.file_uploader("Upload IES File", type=["ies"])
efficiency_multiplier = st.number_input("Enter Chip Efficiency Multiplier", min_value=1.0, step=0.001, value=1.000)
new_length = st.number_input("Enter New Luminaire Length (m)", min_value=0.5, step=0.001, value=1.000)
debug_mode = st.checkbox("Enable Debug Mode (Show Detected Angles)")

if uploaded_file:
    file_name = uploaded_file.name.replace("1Meter", "").replace(".ies", f"_{new_length:.3f}m.ies")
    file_content = uploaded_file.read().decode("utf-8")
    modified_content = modify_ies_file(file_content, efficiency_multiplier, new_length, debug_mode)

    st.download_button(
        label="Download Modified IES File",
        data=io.BytesIO(modified_content.encode("utf-8")),
        file_name=file_name,
        mime="text/plain"
    )
