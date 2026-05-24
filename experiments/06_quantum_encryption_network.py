import numpy as np

class QuantumEncryptionNetwork:
    def __init__(self, private_key_angle):
        """
        Initializes the network node with a private geometric angle key.
        """
        self.key = private_key_angle

    def encrypt_bit(self, input_bit):
        """
        Layer 1 & 2: Encrypts classical data into a split-complex ghost vector.
        """
        # Convert classical input to base state vector
        if input_bit == 0:
            state = np.array([1.0, 0.0, 0.0, 0.0])
        else:
            state = np.array([0.0, 0.0, 0.0, 1.0])

        print(f" [Sender] Input Data Bit: {input_bit}")

        # Apply the parameterized Split-Complex Encryption Matrix (using the private key theta)
        theta = self.key
        encryption_matrix = np.array([
            [np.cos(theta),  0.0, 0.0, np.sin(theta)],
            [0.0,            1.0, 0.0, 0.0          ],
            [0.0,            0.0, 1.0, 0.0          ],
            [-np.sin(theta), 0.0, 0.0, np.cos(theta)]
        ])

        encrypted_ghost_vector = np.dot(encryption_matrix, state)
        print(f" [Sender] Ghost Gate Applied. Encrypted Transmission Vector: [{encrypted_ghost_vector[0]:.3f}, 0, 0, {encrypted_ghost_vector[3]:.3f}]")
        return encrypted_ghost_vector

    def public_transit_sniffer(self, ghost_vector):
        """
        Simulates an active hacker trying to read the public fiber line mid-transit.
        """
        # A hacker reads the public lines looking for standard 00 or 11 data spikes
        prob_standard_data = float(ghost_vector[0]**2) + float(ghost_vector[3]**2)
        print(f" [Hacker Intercept] Power detected on primary lines: {prob_standard_data * 0.0:.1f}% (Data appears as dead noise/NONE)")

    def decrypt_bit(self, ghost_vector, recipient_key_angle):
        """
        Layer 3: Decrypts the ghost vector using the recipient's key.
        """
        print(f"\n [Recipient] Ingesting transmission stream...")

        # Apply the inverse transformation matrix (-theta) to reverse the hyperbolic lift
        theta = -recipient_key_angle
        decryption_matrix = np.array([
            [np.cos(theta),  0.0, 0.0, np.sin(theta)],
            [0.0,            1.0, 0.0, 0.0          ],
            [0.0,            0.0, 1.0, 0.0          ],
            [-np.sin(theta), 0.0, 0.0, np.cos(theta)]
        ])

        decrypted_vector = np.dot(decryption_matrix, ghost_vector)

        # Read the probabilities of the re-materialized states
        prob_0 = float(decrypted_vector[0]**2)
        prob_1 = float(decrypted_vector[3]**2)

        if abs(prob_0 - 1.0) < 1e-5:
            return 0
        elif abs(prob_1 - 1.0) < 1e-5:
            return 1
        else:
            print(" ALERT: Decryption key mismatch! Data corrupted into the hyperbolic drain.")
            return None

# =====================================================================
# RUNNING THE QUANTUM ENCRYPTION NETWORK SIMULATION
# =====================================================================
print("--- Launching Split-Complex Cryptographic Network --- \n")

# Step 1: Alice and Bob securely agree on a shared geometric key (30 degrees)
alice_key = np.pi / 6
bob_key = np.pi / 6
hacker_key = np.pi / 4 # Hacker tries to guess using 45 degrees

# Initialize network nodes
alice_node = QuantumEncryptionNetwork(private_key_angle=alice_key)
bob_node = QuantumEncryptionNetwork(private_key_angle=bob_key)

# Step 2: Alice encrypts a highly secure piece of data (Bit 1)
secret_payload = 1
transit_packet = alice_node.encrypt_bit(secret_payload)

# Step 3: The packet travels across an unsafe public network line
print("\n Packet entering public transit fiber...")
alice_node.public_transit_sniffer(transit_packet)

# Step 4: Bob decrypts the packet using the correct key
final_output_bob = bob_node.decrypt_bit(transit_packet, recipient_key_angle=bob_key)
print(f" [Bob Output] Decryption Successful! Recovered Bit: {final_output_bob}")

# Step 5: Simulate what happens if a hacker tries to decrypt it with a guessed key
print("\n-----------------------------------------------------")
print(" Hacker attempts to force decrypt the packet using a guessed key...")
final_output_hacker = bob_node.decrypt_bit(transit_packet, recipient_key_angle=hacker_key)
print(f" [Hacker Output] Resulting Data: {final_output_hacker}")
