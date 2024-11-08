import Steganography as st

image_path = "encoded_image_2024-11-08-23.01.32.png"  # File hasil penyisipan pesan
key = "Kelompok6"  # Kunci untuk dekripsi

# Mengungkap pesan terenkripsi menggunakan kunci
pesan = st.reveal_message(image_path, key)
print("Pesan tersembunyi:", pesan)
