import pandas as pd  # type: ignore

def get_data():
    print("="*60)
    print("📥 PILIH SUMBER DATA".center(60))
    print("="*60)
    print("1. File Lokal")
    print("2. Google Sheets (Online)")
    sumber = input("Masukkan pilihan (1/2): ")

    if sumber == '2':
        url = "https://docs.google.com/spreadsheets/d/17ru4XAU2NloE9Dfxr2PC1BVcsYkLLT5r7nPSsiOFlvQ/export?format=csv&gid=743838712"
        try:
            df_online = pd.read_csv(url)
            print("✅ Berhasil mengambil data dari Google Sheets.")
            return df_online
        except Exception as e:
            print(f"❌ Gagal mengakses Google Sheets: {e}")
            return None
    else:
        try:
            file_path = r"C:\Users\fawwa\Downloads\Struktur_Data_Dataset_Kelas_A_B_C (1).xlsx"
            df_local = pd.read_excel(file_path, engine='openpyxl')
            print("✅ Berhasil membaca data lokal.")
            return df_local
        except Exception as e:
            print(f"❌ Gagal membaca file lokal: {e}")
            return None

def linear_search(df, kolom, keyword):
    print("\n🔍 Sedang melakukan Linear Search...")
    hasil = df[df[kolom].astype(str).str.contains(keyword, case=False, na=False)]
    return hasil

def binary_search(df, kolom, keyword):
    df_sorted = df.sort_values(by=kolom).reset_index(drop=True)
    low = 0
    high = len(df_sorted) - 1
    results = []

    while low <= high:
        mid = (low + high) // 2
        mid_val = str(df_sorted.loc[mid, kolom])

        if keyword.lower() == mid_val.lower():
            i = mid
            while i >= 0 and str(df_sorted.loc[i, kolom]).lower() == keyword.lower():
                results.append(df_sorted.loc[i])
                i -= 1
            i = mid + 1
            while i < len(df_sorted) and str(df_sorted.loc[i, kolom]).lower() == keyword.lower():
                results.append(df_sorted.loc[i])
                i += 1
            break
        elif keyword.lower() < mid_val.lower():
            high = mid - 1
        else:
            low = mid + 1

    return pd.DataFrame(results)

def tampilkan_hasil_sederet(df):
    for _, row in df.iterrows():
        print(f"- Judul: {row['Judul Paper']} | Penulis: {row['Nama Penulis']} | Tahun: {row['Tahun Terbit']} | Link: {row['Link Paper']}")

def main():
    df = get_data()
    if df is None:
        return

    required_cols = ['Judul Paper', 'Nama Penulis', 'Tahun Terbit', 'Link Paper']
    for col in required_cols:
        if col not in df.columns:
            print(f"⚠️  Kolom '{col}' tidak ditemukan dalam data.")
            return

    while True:
        print("\n" + "="*60)
        print("🔍 MENU PENCARIAN".center(60))
        print("="*60)
        print("1. Linear Search")
        print("2. Binary Search")
        print("3. Keluar")
        pilihan = input("Masukkan pilihan (1/2/3): ")

        if pilihan == '3':
            print("\n👋 Terima kasih telah menggunakan program!")
            break
        if pilihan not in ['1', '2']:
            print("⚠️  Pilihan tidak valid.")
            continue

        print("\n📚 Cari berdasarkan:")
        print("1. Judul Paper")
        print("2. Nama Penulis")
        print("3. Tahun Terbit")
        kolom_pilihan = input("Masukkan pilihan kolom (1/2/3): ")

        kolom_dict = {
            '1': 'Judul Paper',
            '2': 'Nama Penulis',
            '3': 'Tahun Terbit'
        }

        if kolom_pilihan not in kolom_dict:
            print("⚠️  Pilihan kolom tidak valid.")
            continue

        kolom = kolom_dict[kolom_pilihan]
        keyword = input(f"✏️  Masukkan kata kunci untuk '{kolom}': ")

        if pilihan == '1':
            hasil = linear_search(df, kolom, keyword)
        else:
            if kolom != 'Tahun Terbit':
                print("⚠️  Binary Search lebih cocok untuk pencarian exact match.")
            hasil = binary_search(df, kolom, keyword)

        print("\n" + "-"*60)
        if not hasil.empty:
            print("✅ Hasil pencarian:")
            tampilkan_hasil_sederet(hasil)
        else:
            print("❌ Data tidak ditemukan.")
        print("-"*60)

if __name__ == "__main__":
    main()
