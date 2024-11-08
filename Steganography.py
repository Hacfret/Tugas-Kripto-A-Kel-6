from PIL import Image
import time

def hide_message(image_path, message, output_path, key):
    img = Image.open(image_path).convert("RGB")  # Mengubah gambar ke mode RGB
    encoded = img.copy()
    width, height = img.size
    
    # Ubah pesan dan kunci menjadi biner
    start_marker = "START"  # Penanda awal pesan
    end_marker = "1111111111111110"  # Penanda akhir pesan
    
    binary_message = ''.join([format(ord(i), "08b") for i in (start_marker + message)]) + end_marker
    binary_key = ''.join([format(ord(i), "08b") for i in key])
    
    # Enkripsi pesan dengan kunci menggunakan operasi XOR
    encrypted_message = ''.join(
        str(int(binary_message[i]) ^ int(binary_key[i % len(binary_key)])) for i in range(len(binary_message))
    )
    
    data_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            
            if data_index < len(encrypted_message):
                r = int(format(r, "08b")[:-1] + encrypted_message[data_index], 2)
                data_index += 1
            if data_index < len(encrypted_message):
                g = int(format(g, "08b")[:-1] + encrypted_message[data_index], 2)
                data_index += 1
            if data_index < len(encrypted_message):
                b = int(format(b, "08b")[:-1] + encrypted_message[data_index], 2)
                data_index += 1
            
            encoded.putpixel((x, y), (r, g, b))
            
            if data_index >= len(encrypted_message):
                encoded.save(output_path)
                return f"Pesan disisipkan ke dalam gambar dan disimpan sebagai {output_path}"

    return "Gagal menyisipkan pesan, gambar terlalu kecil."

def reveal_message(image_path, key):
    img = Image.open(image_path)
    binary_message = ""
    width, height = img.size
    
    # Loop untuk mengekstrak pesan terenkripsi biner dari gambar
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            binary_message += format(r, "08b")[-1]
            binary_message += format(g, "08b")[-1]
            binary_message += format(b, "08b")[-1]
            
            # Cek tanda akhir pesan lebih awal
            if "11111110" in binary_message[-24:]:  # Mengecek beberapa byte terakhir
                break
        else:
            continue
        break
    
    # Mendekripsi pesan dengan kunci menggunakan XOR
    binary_key = ''.join([format(ord(i), "08b") for i in key])
    decrypted_message = ''.join(
        str(int(binary_message[i]) ^ int(binary_key[i % len(binary_key)])) for i in range(len(binary_message))
    )
    
    # Mengonversi pesan biner terdekripsi menjadi karakter
    all_bytes = [decrypted_message[i:i+8] for i in range(0, len(decrypted_message), 8)]
    decoded_message = ""
    for byte in all_bytes:
        if byte == '11111110':  # Tanda akhir pesan
            break
        decoded_message += chr(int(byte, 2))
    
    # Verifikasi apakah pesan dimulai dengan penanda "START"
    if decoded_message.startswith("START"):
        return decoded_message[5:-1]  # Menghapus penanda "START" dan penanda akhir dari pesan
    else:
        return "Kunci salah"

if __name__ == "__main__":
    image_path = "buku.png"
    message = "pesan rahasia kelompok 6: Tes 12345"
    key = "Kelompok6"  # Kunci untuk enkripsi dan dekripsi
    timestamp = time.strftime("%Y-%m-%d-%H.%M.%S")
    output_path = f'encoded_image_{timestamp}.png'
    
    # Menyembunyikan pesan terenkripsi
    print(hide_message(image_path, message, output_path, key))