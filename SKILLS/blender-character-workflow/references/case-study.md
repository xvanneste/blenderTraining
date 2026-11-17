# Case study · from two guides to an animated character

The Blender Cinema Master Academy workspace contains a worked example under `PROPOSITIONS/RECONSTRUCTION_2_VUES`. When working in that workspace, use its README to find the current version. The workflow does not depend on access to that example.

| Stage | Useful technique | Check |
|---|---|---|
| Two orthographic guides | Generate both views on one aligned sheet and then extract the panels. Use common image rows and separate width/depth axes. | Compare crown, eyes, shoulder, knee and floor heights. A side view can hide limbs. Record where you estimated depth. |
| First geometry pass | Use a silhouette hull to check envelope only. For identity, start from a continuous, licensed anatomical mesh. The case used MakeHuman CC0 with matching vertex indices across morph target, UVs, skeleton and weights. | Compare jaw, nose, mouth, eye placement, neck and silhouette in clay. A watertight mesh can still be visually wrong. |
| Fit and finish | Retain the anatomical feet under the shoe; use clearance around the forefoot, ankle opening and heel. Retain the garment's UV and armature while changing the hem. For a smooth Blender Mask, convert signed distance (d) to weight (0.5 + d / span) and put the cut at threshold 0.5. Use a broad enough span that crossing edges do not clamp on both sides. | Inspect a cutaway and rendered close-ups of the neutral and bent ankle. Check that shape keys preserve the revised foot coordinates and that deform weights still sum to 1. |
| Walk | Move the rig along an explicit world trajectory and hold each IK target fixed in world space during its stance. Transform world targets back to the armature and then into each control bone's space. Give swing its own arc and test planted soles and the lowest point of the swing. | Stepping frames is useful even with exact input targets. Measure the evaluated ankle against its target, change in ankle position over each stance, and minimum evaluated sole Z. If the rig cannot reach, shorten the stride or lower the pelvis before weakening the test. |
| Export | Save the editable scene, then render an MP4 and check that decoding produces the intended duration and motion. For a short review, use an efficient renderer or resolution. | Compare beginning, middle and end and review a side or three-quarter angle. Distinguish an intentional short preview from film-ready animation. |

## Blender pitfalls demonstrated by the case

- In Blender, `object.animation_data_clear()` clears drivers as well as the action. To replace the walk on a rig that uses drivers for IK influence, detach `object.animation_data.action` and keep the animation data.
- Foot contact assertions should come from evaluated vertices including the Armature and Subdivision modifiers. Check the component that touches the ground, rather than the bone origin.
- Sizing a shoe while the body foot is masked can hide a bad fit. After restoring the foot, a front toe-ray test alone can miss a collision at the tongue and quarter. Measure the opening and review that region in both poses.
- Bake colour to a named UV map and pack the image if the file should open without external textures. Keep guide images separate from the presentation material.
