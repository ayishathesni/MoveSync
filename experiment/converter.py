import os
import numpy as np
import bvhsdk

# Define constants
FRAME_RATE = 30
INPUT_FILE = 'C:/Users/CHIDORA/Desktop/ROMP_Results/video_results.npz'
OUTPUT_FILE = 'C:/Users/CHIDORA/Desktop/bvh/output.bvh'

# Load data from npz file
npz_file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'ROMP_Results', INPUT_FILE)
with np.load(npz_file_path) as npz_file:
    joint_positions = npz_file['joints']

# Load joint hierarchy from a separate file (e.g., JSON)
joint_hierarchy_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'ROMP_Results', 'joint_hierarchy.json')
with open(joint_hierarchy_path, 'r') as f:
    joint_hierarchy = json.load(f)

# Create a new BVH file
bvh = bvhsdk.BVH()

# Add joints
for joint_name, joint_index in joint_hierarchy.items():
    bvh.add_joint(joint_name, joint_positions[0, :, joint_index])

# Set joint hierarchy
for parent, child in joint_hierarchy.items():
    bvh.add_child(parent, child)

# Set root motion
bvh.root_motion = 'Pelvis'

# Set motion data
for frame in range(joint_positions.shape[1]):
    motion_data = []
    for joint_position in joint_positions[:, frame]:
        motion_data.append(list(joint_position))
    bvh.motion.append(motion_data)

# Adjust frame rate
bvh.frame_rate = FRAME_RATE

# Save BVH file
output_file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'bvh', OUTPUT_FILE)
bvh.write(output_file_path)