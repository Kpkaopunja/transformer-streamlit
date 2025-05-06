import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

# ใช้ css ตกแต่งเว็บเพิ่ม
st.markdown("""
<style>
    /* เพิ่มช่องว่างรอบขอบหน้าเว็บ */
    .css-18e3th9 {
        padding: 2rem 5rem;
    }
    
    /* เพิ่มเส้นใต้หัวข้อและเพิ่มระยะห่างข้อความกับเส้นใต้ */
    h1 {
        color: #003366;
        border-bottom: 2px solid #003366;
        padding-bottom: 1 !important; 
        margin-bottom: 0 !important;
        # display: inline-block;  # ทำให้เส้นยาวเท่าข้อความ
    }
    
    # /* วิธีเสริมเพื่อป้องกันผลกระทบกับส่วนอื่น */
    # .css-18e3th9 {
    #     padding-top: 1rem !important;
    # }
    
    /* ปุ่มอัปโหลดไฟล์ เปลี่ยนสีพื้นหลังเป็นเทาอ่อน ทำมุมโค้งมนและเพิ่มช่องว่าง */
    .st-eb {
        background-color: #f0f2f6;
        border-radius: 10px; /* ทำให้มุมโค้งมน */
        padding: 25px;
    }
    
</style>
""", unsafe_allow_html=True)

# SET ฟอนต์ภาษาไทย
def setup_thai_font():
    font_path = 'THSarabunNew.ttf'
    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()

# วาดกราฟวงกลม LBBSA
def plot_lbbsa(df):
    counts = df['LBBSA'].value_counts(dropna=False)
    labels = counts.index.fillna('ไม่มีข้อมูล')

    total = sum(counts.values)

    new_labels = []
    for label, count in zip(labels, counts.values):
        pct = count / total * 100
        new_labels.append(f'{label} - {count} เครื่อง ({pct:.1f}%)')

    fig, ax = plt.subplots(figsize=(12, 12))
    fig.patch.set_facecolor('#f5f5f5')  # สีพื้นหลังกราฟ

    ax.pie(
        counts.values,
        labels=new_labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Set3.colors,
        textprops={'fontsize': 19},
        labeldistance=1.1
    )

    ax.set_title('กราฟแสดงสถานะหม้อแปลง (LBBSA)',fontsize=25, color="#003366", fontweight='bold',x=0.5,y=0.9)
    ax.axis('equal')
    plt.tight_layout()
    return fig

# upload file
def load_data(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            st.error("รองรับแค่ไฟล์ CSV และ Excel เท่านั้น")
            return None
        
        # แก้ไขค่า NULL ให้เป็น NaN
        df[['LBBSA', 'รหัสผิดปกติ', 'คำอธิบาย', 'แบทซ์']] = df[['LBBSA', 'รหัสผิดปกติ', 'คำอธิบาย', 'แบทซ์']].replace(['', 'NULL'], pd.NA)
        return df
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดไฟล์: {e}")
        return None

# START
setup_thai_font()
st.markdown("""
<style>
/* ตั้งค่าฟอนต์หลัก */
* {
    font-family: 'TH Sarabun New', sans-serif !important;
}

/* หัวข้อหลัก */
.dashboard-title {
    font-size: 50px !important;
    font-weight: bold !important;
    color: #003366 !important;
    margin-bottom: 20px !important;
}

/* ปรับตาราง */
.stDataFrame, .dataframe {
    font-size: 24px !important;
    font-family: 'TH Sarabun New', sans-serif !important;
}

.stDataFrame td, .stDataFrame th {
    padding: 4px 8px !important;
    font-family: 'TH Sarabun New', sans-serif !important;
}

/* ปุ่มและองค์ประกอบอื่นๆ */
body, div, span, app, p, a, li, ul, ol,button, input, select, textarea {
    font-size: 24px !important;
    font-family: 'TH Sarabun New', sans-serif !important;
}           
</style>
""", unsafe_allow_html=True)


# เรียกใช้ฟังก์ชันตั้งค่าฟอนต์
font_prop = setup_thai_font()

# ส่วนแสดงหัวข้อ
st.markdown('<h1 class="dashboard-title">Transformer Data Dashboard</h1>', unsafe_allow_html=True)

#ตั้งให้สามารถอัปโหลดไฟล์ excel ได้ทั้ง .csv และ .xlsx
# st.write("") #เพิ่มช่องว่างนิดนึง
uploaded_file = st.file_uploader("อัปโหลดไฟล์ (.csv หรือ .xlsx)", type=["csv", "xlsx"])

# กราฟวงกลมแสดงข้อมูลที่เลือก
# ฟังก์ชันวาดกราฟวงกลม จากข้อมูลที่กรองแล้ว
def plot_lbbsa_filtered(filtered_df):
    counts = filtered_df['LBBSA'].value_counts(dropna=False)
    labels = counts.index.fillna('ไม่มีข้อมูล')

    total = sum(counts.values)
    new_labels = []
    for label, count in zip(labels, counts.values):
        pct = count / total * 100
        new_labels.append(f'{label} - {count} เครื่อง ({pct:.1f}%)')

    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor('#fefefe')  # สีพื้นหลังแบบอ่อนกว่าหน่อย

    ax.pie(
        counts.values,
        labels=new_labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Pastel1.colors,
        textprops={'fontsize': 18},
        labeldistance=1.1
    )
    ax.set_title('กราฟแสดงผลตามข้อมูลที่เลือก (LBBSA)', fontsize=20, color="#336699", fontweight='bold', x=0.5, y=0.9)
    ax.axis('equal')

    plt.tight_layout()
    return fig

# 🔘 ฟังก์ชันวาดกราฟวงกลมแบบไม่มี label ในวง พร้อม legend ทางขวา
def plot_pie_with_right_legend(filtered_df):
    counts = filtered_df['LBBSA'].value_counts(dropna=False)
    labels = counts.index.fillna('ไม่มีข้อมูล')
    values = counts.values

    # เตรียมข้อความใน legend
    total = sum(values)
    legend_labels = [
        f"{label} - {count} เครื่อง ({count/total:.1%})"
        for label, count in zip(labels, values)
    ]

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('#fafafa')

    wedges, _ = ax.pie(
        values,
        labels=None,
        colors=plt.cm.Pastel1.colors,
        startangle=90
    )

    # วาง legend ด้านขวา
    ax.legend(
        wedges,
        legend_labels,
        title="สถานะ",
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        fontsize=14,
        title_fontsize=15
    )

    ax.set_title("กราฟแสดงสถานะหม้อแปลง (LBBSA)", fontsize=20, color="#003366", fontweight='bold', x=0.5, y=0.9)
    ax.axis('equal')
    plt.tight_layout()
    return fig

# กราฟแท่งแนวนอนแสดงผลตามข้อมูลที่เลือก : เฉพาะรหัสผิดปกติ+จำนวน
# ฟังก์ชันกราฟแท่งแนวนอนตามข้อมูลที่เลือก
def plot_error_codes_bar(df, font_prop):
    if 'รหัสผิดปกติ' not in df.columns or 'คำอธิบาย' not in df.columns:
        st.warning("ไม่มีข้อมูลรหัสผิดปกติหรือคำอธิบาย")
        return
    
    #setค่าว่างให้เป็น ไม่มีข้อมมูล
    df['รหัสผิดปกติ'] = df['รหัสผิดปกติ'].fillna('ไม่มีข้อมูล')
    df['คำอธิบาย'] = df['คำอธิบาย'].fillna('ไม่มีข้อมูล')

    grouped = (
        df[['รหัสผิดปกติ', 'คำอธิบาย']]
        .dropna()
        .groupby(['รหัสผิดปกติ', 'คำอธิบาย'])
        .size()
        .reset_index(name='จำนวน')
        .sort_values(by='จำนวน', ascending=True)
    )
    if grouped.empty:
        st.info("ไม่มีข้อมูลเพียงพอสำหรับสร้างกราฟแท่ง")
        return
    def generate_label(row):
        if row['รหัสผิดปกติ'] == 'ไม่มีข้อมูล' and row['คำอธิบาย'] == 'ไม่มีข้อมูล':
            return 'ไม่มีข้อมูล'
        else:
            return f"{row['รหัสผิดปกติ']} : {row['คำอธิบาย']}"

    # ✅ ใช้เพื่อสร้าง label
    grouped['label'] = grouped.apply(generate_label, axis=1)

    labels = grouped['label']
    values = grouped['จำนวน']

    max_value = max(values)
    width_factor = 0.1 if max_value < 50 else 0.08  # ปรับตามจำนวน
    fig_width = min(10, max(10, int(max_value * width_factor)))  # จำกัดไม่ให้ยาวเกินไป
    fig, ax = plt.subplots(figsize=(fig_width, len(labels) * 0.6))

    bars = ax.barh(labels, values, color='mediumseagreen')

    # ปรับฟอนต์
    for label in ax.get_yticklabels():
        label.set_fontproperties(font_prop)
        label.set_fontsize(17)
    for label in ax.get_xticklabels():
        label.set_fontproperties(font_prop)
        label.set_fontsize(17)

    # แสดงจำนวนเครื่องแต่ละรหัสผิดปกติ
    for bar in bars:
        width = bar.get_width()
        x_pos = width + (max_value * 0.01)
        ax.text(x_pos, bar.get_y() + bar.get_height() / 2,
                f'{int(width)} ', va='center', fontsize=17, fontproperties=font_prop)

    ax.set_xlim([0, max_value * 1.2])
    ax.set_title('กราฟรหัสผิดปกติจากข้อมูลที่เลือก', fontproperties=font_prop, fontsize=20, color="#336699", fontweight='bold',y=1.05)
    ax.set_xlabel('จำนวนเครื่อง', fontproperties=font_prop, fontsize=17)
    ax.set_ylabel('รหัส : คำอธิบาย', fontproperties=font_prop, fontsize=17)

    st.pyplot(fig)

if uploaded_file is not None:
    df = load_data(uploaded_file)
    st.success(f"โหลดข้อมูลสำเร็จ ✅ พบหม้อแปลงทั้งหมด {len(df)} เครื่อง")
    if df is not None:
        with st.container():
            st.markdown("<h4 style='color:#333;'>📈 กราฟวงกลม แสดงสถานะหม้อแปลง LBBSA</h4>", unsafe_allow_html=True)
            with st.expander("คลิกเพื่อดูกราฟ"):
                fig_overall = plot_lbbsa(df)
                st.pyplot(fig_overall)

        st.subheader("📝 ตัวอย่างข้อมูล")
        st.write(df.head())


        filtered_df = df.copy()

        # เลือกโหมดการกรอกข้อมูล
        st.subheader("📝กรอกข้อมูล")
        filter_mode = st.radio("เลือกรูปแบบการกรอง", ["แบบธรรมดา", "แบบเจาะลึก"])

        if filter_mode == "แบบธรรมดา":
            st.markdown("🔹 กรองแบบธรรมดา ")
            # ตัด "คำอธิบาย" ออกจากตัวเลือก
            available_columns = [col for col in df.columns if col != "คำอธิบาย"]

            col_to_filter = st.selectbox("เลือกหัวข้อที่ต้องการ", available_columns)

            if col_to_filter == "รหัสผิดปกติ" and "คำอธิบาย" in df.columns:
                # รวมรหัสและคำอธิบาย
                combined = df[["รหัสผิดปกติ", "คำอธิบาย"]].dropna().drop_duplicates()
                options = [f"{row['รหัสผิดปกติ']} : {row['คำอธิบาย']}" for _, row in combined.iterrows()]
                selected_option = st.selectbox(f"เลือกข้อมูลของ {col_to_filter}", ["ทั้งหมด"] + options)

                if selected_option != "ทั้งหมด":
                    selected_code = selected_option.split(" : ")[0]
                    filtered_df = df[df["รหัสผิดปกติ"] == selected_code]
            else:
                unique_vals = df[col_to_filter].dropna().unique()
                selected_vals = st.multiselect(f"เลือกข้อมูลของ {col_to_filter}", list(unique_vals))

                if selected_vals:
                    filtered_df = df[df[col_to_filter].isin(selected_vals)]


        elif filter_mode == "แบบเจาะลึก":
            st.markdown("🔸 กรองแบบเจาะลึกทีละขั้น ")

            # ตัด "คำอธิบาย" ออกจากรายการตัวเลือก
            excluded_cols = ["คำอธิบาย"]
            available_cols = [col for col in filtered_df.columns if col not in excluded_cols]
            start_col = st.selectbox("เลือกหัวข้อเริ่มต้น", available_cols)

            try:
                start_index = available_cols.index(start_col)
                for col in available_cols[start_index:]:
                    #รวมรหัสผิดปกติและคำอธิบายเป็นตัวเลือกเดียวกัน
                    if col in filtered_df.columns and not filtered_df.empty:
                        if col == "รหัสผิดปกติ" and "คำอธิบาย" in filtered_df.columns:
                            combined = (
                                filtered_df[["รหัสผิดปกติ", "คำอธิบาย"]]
                                .dropna()
                                .drop_duplicates()
                            )
                            options = [f"{row['รหัสผิดปกติ']} : {row['คำอธิบาย']}" for _, row in combined.iterrows()]
                            selected = st.selectbox(f"เลือกข้อมูลใน \"{col}\"", ["ทั้งหมด"] + options)

                            if selected != "ทั้งหมด":
                                selected_code = selected.split(" : ")[0]
                                filtered_df = filtered_df[filtered_df["รหัสผิดปกติ"] == selected_code]
                        else:
                            values = filtered_df[col].dropna().unique()
                            
                            if col == "สถานะหม้อแปลง":
                                selected_values = st.multiselect(f"เลือกข้อมูลใน \"{col}\"", list(values))
                                if selected_values:
                                    filtered_df = filtered_df[filtered_df[col].isin(selected_values)]
                            selected_vals = st.multiselect(f"เลือกข้อมูลใน \"{col}\"", list(values))
                            if selected_vals:
                                filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]


            except Exception as e:
                st.warning(f"เกิดข้อผิดพลาดในการเจาะลึก: {e}")

        # จำนวนที่หม้อแปลงที่กรองข้อมูลได้
        st.subheader("🧮 จำนวนหม้อแปลง : {} เครื่อง".format(len(filtered_df)))

        st.subheader("📋 ข้อมูลที่คุณต้องการ")
        st.write(filtered_df)
        
        # แสดงกราฟที่กรองข้อมูลตามข้อมูลที่เราเลือก
        # แสดงกราฟตามข้อมูลที่เลือก
        if not filtered_df.empty:
            st.subheader("📊 กราฟแสดงผลตามข้อมูลที่เลือก")

            font_prop = setup_thai_font()
            
            with st.expander("🔘 สถานะหม้อแปลง LBBSA"):
                fig_filtered = plot_pie_with_right_legend(filtered_df) 
                st.pyplot(fig_filtered)

            with st.expander("📉 รหัสผิดปกติ"):
                fig_bar = plot_error_codes_bar(filtered_df, font_prop)
                if fig_bar:
                    st.pyplot(fig_bar)

    else:
        st.warning("โปรดอัปโหลดไฟล์ที่ถูกต้อง")
else:
    st.write("รอการอัปโหลดไฟล์...")