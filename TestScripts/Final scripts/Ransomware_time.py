import os
import time
import base64

class OptimizedEncryptionBenchmark:
    """ Benchmark encryption performance with PyPy-friendly optimizations. """

    def __init__(self, root_path, iterations=10_000, chunk_size=64 * 1024):
        self.root_path = root_path
        self.iterations = iterations
        self.chunk_size = chunk_size
        self.key = b"SuperSecureKey!"  # 16-byte key for XOR

    def xor_encrypt(self, data):
        """ XOR encryption with a key + bitwise rotation for better JIT optimization. """
        rotated_key = self.key[-1:] + self.key[:-1]  # Bitwise key rotation
        return bytes((b ^ rotated_key[i % len(rotated_key)]) for i, b in enumerate(data))

    def encode_data(self, data):
        """ Apply XOR + Base64 encoding for more CPU-heavy operations. """
        encrypted = self.xor_encrypt(data)
        return base64.b64encode(encrypted)

    def decode_data(self, data):
        """ Decode Base64 + XOR decryption. """
        decoded = base64.b64decode(data)
        return self.xor_encrypt(decoded)  # XOR decrypt

    def simulate_encryption(self, file_path):
        """ Simulate encryption without modifying files. """
        fake_data = os.urandom(self.chunk_size)  # Generate fake file data
        for _ in range(10):  # More work per file for JIT optimization
            encrypted = self.encode_data(fake_data)
        return encrypted  # Return to prevent optimizations removing unused work

    def simulate_decryption(self, encrypted_data):
        """ Simulate decryption without modifying files. """
        for _ in range(10):  # More work per file for JIT optimization
            decrypted = self.decode_data(encrypted_data)
        return decrypted

    def scan_files(self):
        """ Scan the entire filesystem and collect file paths. """
        file_list = []
        for root, _, files in os.walk(self.root_path):
            for file in files:
                if file.endswith(".py"):  # Exclude Python scripts
                    continue
                file_list.append(os.path.join(root, file))
        return file_list

    def benchmark(self):
        """ Benchmark encryption/decryption speed over a large dataset. """
        file_list = self.scan_files()
        total_files = len(file_list)
        print(f"Scanned {total_files} files.")

        if total_files == 0:
            print("No files found for benchmarking.")
            return

        # Pick a sample file (or generate fake data)
        sample_file = file_list[0] if file_list else None
        fake_encrypted_data = self.simulate_encryption(sample_file)

        # Encryption Benchmark
        start_enc = time.time()
        for _ in range(self.iterations):
            _ = self.simulate_encryption(sample_file)
        end_enc = time.time()
        avg_enc_time = (end_enc - start_enc) / self.iterations

        # Decryption Benchmark
        start_dec = time.time()
        for _ in range(self.iterations):
            _ = self.simulate_decryption(fake_encrypted_data)
        end_dec = time.time()
        avg_dec_time = (end_dec - start_dec) / self.iterations

        print("\nBenchmark Results:")
        print(f"Files Scanned: {total_files}")
        print(f"Average Encryption Time: {avg_enc_time:.6f} sec")
        print(f"Average Decryption Time: {avg_dec_time:.6f} sec")


if __name__ == "__main__":
    root_directory = "C:\\"  # Change to "/" for Linux/macOS
    benchmark = OptimizedEncryptionBenchmark(root_directory, iterations=10_000)
    benchmark.benchmark()
